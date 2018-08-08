"""Export all datasets to excel-compatible csv.

Currently only exports public datasets, but once CKAN is upgraded to v2.4+,
the code can be updated to support private datasets.
"""
import json

from ckan.plugins.toolkit import BaseController, NotAuthorized, ObjectNotFound, abort, c, config, check_access, get_action, h, render, request
from ckanext.ldap.controllers.user import _get_ldap_connection, _find_ldap_user, _get_or_create_ldap_user
import ldap
import ldap.filter

import logging

class GroupNotFound(Exception):
    pass

def context():
    return {"user": c.user}

def get_datasource(source_id):
    response = get_action("package_show")({}, {"id": source_id})
    return response

def make_roles(cns):
    # Get the roles
    data_dict = {
        "query": "resource_type:",
        "limit": 9999,
    }
    response = get_action("resource_search")({}, data_dict)
    results = response["results"]
    # Map each cn to a list of resource/role combos that it matches
    role_dict = dict([(cn, []) for cn in cns])
    for resource in results:
        datasource = None # We only get the source if we actually need it in the code below
        roles = json.loads(resource.get("db_roles") or "[]")
        for role_cn, role_desc in roles:
            if role_cn in role_dict:
                if datasource is None:
                    try:
                        datasource = get_datasource(resource["package_id"])
                    except:
                        logging.error(u"ERROR while getting datasource for resource {}".format(repr(resource)))
                        continue
                role_dict[role_cn].append({
                    "source_id": resource["package_id"],
                    "resource_id": resource["id"],
                    "resource_name": resource["name"],
                    "source_name": datasource["title"],
                    "owner_org": datasource["owner_org"],
                    "source_url": "/dataset/"+datasource["name"],
                    "description": role_desc,
                })
    return role_dict

def get_user(username, connection):
    base_dn = config["ckanext.ldap.base_dn"]
    search_filter = config["ckanext.ldap.search.filter"]
    results = connection.search_s(
        base_dn,
        ldap.SCOPE_SUBTREE,
        filterstr=search_filter.format(login=ldap.filter.escape_filter_chars(username))
    )
    return results[0]

def find_groups(base_dns, cn, connection):
    for base_dn in base_dns:
        for result in connection.search_s(base_dn, ldap.SCOPE_SUBTREE, filterstr="CN="+ldap.filter.escape_filter_chars(cn)):
            yield result

def get_group_full_name(base_dns, cn, connection):
    try:
        return next(find_groups(base_dns, cn, connection))[0]
    except StopIteration:
        raise GroupNotFound()

def get_usernames_in_group(base_dns, cn, connection):
    full_name = get_group_full_name(base_dns, cn, connection)
    results = connection.search_s(config['ckanext.ldap.base_dn'], ldap.SCOPE_SUBTREE, filterstr="memberOf="+full_name, attrlist=["sAMAccountName"])
    return [res[1]["sAMAccountName"][0] for res in results]

def get_user_group_cns(username, base_dns, connection):
    user_id, _ = get_user(username, connection)
    cns = set()
    for base_dn in base_dns:
        cns |= set(
            res[1]["cn"][0] for res in
            connection.search_s(
                base_dn,
                ldap.SCOPE_SUBTREE,
                filterstr="member="+ldap.filter.escape_filter_chars(user_id),
                attrlist=["cn"],
            )
        )
    return sorted(cns)

def check_editor_access(orgs):
    allowed_orgs = 0
    for org in orgs:
        try:
            check_access("package_create", context(), {"owner_org": org})
            allowed_orgs += 1
        except NotAuthorized:
            pass
    if allowed_orgs > 0:
        return True
    else:
        raise NotAuthorized()


class LdapSearchController(BaseController):
    def ldap_search(self):
        """"""
        base_dn_string = request.params.get("dns") or config.get("ckanext.cfpb_ldap_query.base_dns", None)

        extra = {}

        if not base_dn_string:
            extra["error_message"] = "No base DN's to search against, please set ckanext.cfpb_ldap_query.base_dns"
        else:
            extra["dns"] = base_dn_string.split("|")
            extra["cn"] = request.params.get("cn")
            extra["roles"] = make_roles(extra["cn"])

            # If you're not a sysadmin, you must be an editor of one of the orgs associate with this group in order to view it
            owner_orgs = set((role["owner_org"] for role in extra["roles"].values()[0]))
            try:
                check_access("sysadmin", context())
            except NotAuthorized:
                try:
                    check_editor_access(owner_orgs)
                except NotAuthorized:
                    abort(403, "You must be a sysadmin or the have the 'Editor' permission on an org with a resource that uses this group in order to view this page.")

            try:
                with _get_ldap_connection() as connection:
                    extra["usernames"] = get_usernames_in_group(extra['dns'], extra["cn"], connection)
            except GroupNotFound as e:
                extra["error_message"] = "Group Not Found: {}".format(e)
            except Exception as e:
                extra["error_message"] = "Something went wrong while querying for users: {}".format(e)

        return render('ckanext/cfpb-extrafields/ldap_search.html', extra_vars=extra)

    def user_ldap_groups(self, username):
        """Lookup a user and get their LDAP groups and the corresponding datasets"""
        c.is_sysadmin = False
        if c.user.lower() != username.lower():
            try:
                check_access("sysadmin", context())
                c.is_sysadmin = True
            except NotAuthorized:
                abort(403, "You can only view your own user page unless you're a sysadmin")
        base_dns = config.get("ckanext.cfpb_ldap_query.base_dns").split("|")
        with _get_ldap_connection() as connection:
            cns = get_user_group_cns(username, base_dns, connection)
        roles = make_roles(cns)

        #Make sure the ckan user exists
        ldap_user = _find_ldap_user(username)
        if not ldap_user:
            abort(404, "User not found in LDAP")
        try:
            _get_or_create_ldap_user(ldap_user)
        except:
            abort(500, "could not create CKAN user")

        try:
            user_dict = get_action("user_show")(context(), {
                "id": username,
                 "user_obj": c.userobj,
                 "include_datasets": True,
                 "include_num_followers": True})
        except ObjectNotFound:
            abort(404, "User not found")
        except NotAuthorized:
            abort(403, "Not authorized to see this page")

        c.is_myself = username == c.user
        c.user_dict = user_dict
        c.about_formatted = h["render_markdown"](user_dict["about"])

        extra = {
            "username": username,
            "cns": cns,
            "roles": roles,
        }
        return render('ckanext/cfpb-extrafields/ldap_user.html', extra_vars=extra)
