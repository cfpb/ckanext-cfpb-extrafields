"""Export all datasets to excel-compatible csv.

Currently only exports public datasets, but once CKAN is upgraded to v2.4+,
the code can be updated to support private datasets.
"""
import json

from ckan.plugins.toolkit import BaseController, NotAuthorized, ObjectNotFound, abort, c, config, check_access, get_action, h, render, request
from ckanext.ldap.controllers.user import _get_ldap_connection
import ldap
import ldap.filter

import logging
logging = logging.getLogger(__name__)#VK

class GroupNotFound(Exception):
    __import__('logging').warning(u'VK{}'.format('1'))
#VK
    with _get_ldap_connection() as connection:
    	user_id= get_user(username, connection)
    __import__('logging').warning(u'ldapsearch.GroupNotFoundVK{}'.format(user_id))
#VK
    pass

def context():
    return {"user": c.user}

def get_datasource(source_id):
    __import__('logging').warning(u'VK{}'.format('2'))
    response = get_action("package_show")({}, {"id": source_id})
    return response

def make_roles(cns):
    #get the roles
    __import__('logging').warning(u'VK{}'.format('3'))
    data_dict = {
        "query": "resource_type:",
        "limit": 9999,
    }
    response = get_action("resource_search")({}, data_dict)

    results = response["results"]

    logging.warning(u"LdapSearch.make_roles_resultsVK= {}".format(repr(results))) #VK

    # Map each cn to a list of resource/role combos that it matches
    role_dict = dict([(cn, []) for cn in cns])
    for resource in results:
        datasource = None # We only get the source if we actually need it in the code below
        roles = json.loads(resource.get("db_roles") or "[]")
        for role_cn, role_desc in roles:
            __import__('logging').warning(u'VK{}'.format('4'))
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

    logging.warning(u"LdapSearch.make_roles_role_dictVK= {}".format(repr(role_dict))) #VK

    return role_dict

def get_user(username, connection):
    __import__('logging').warning(u'VK{}'.format('5'))
    base_dn = config["ckanext.ldap.base_dn"]
    search_filter = config["ckanext.ldap.search.filter"]
    results = connection.search_s(
        base_dn,
        ldap.SCOPE_SUBTREE,
        filterstr=search_filter.format(login=ldap.filter.escape_filter_chars(username))
    )

    logging.warning(u"LdapSearch.get_user_filterstrVK= {}".format(repr(filterstr))) #VK
    logging.warning(u"LdapSearch.get_user_resultsVK= {}".format(repr(results))) #VK

    return results[0]

def find_groups(base_dns, cn, connection):
    __import__('logging').warning(u'VK{}'.format('6'))
    for base_dn in base_dns:
        for result in connection.search_s(base_dn, ldap.SCOPE_SUBTREE, filterstr="CN="+ldap.filter.escape_filter_chars(cn)):

            logging.warning(u"LdapSearch.find_groups_resultVK= {}".format(repr(result))) #VK

            yield result

def get_group_full_name(base_dns, cn, connection):
    __import__('logging').warning(u'VK{}'.format('7'))
    try:
        return next(find_groups(base_dns, cn, connection))[0]
    except StopIteration:
        raise GroupNotFound()

def get_usernames_in_group(base_dns, cn, connection):
    __import__('logging').warning(u'VK{}'.format('8'))
    full_name = get_group_full_name(base_dns, cn, connection)
    results = connection.search_s(config['ckanext.ldap.base_dn'], ldap.SCOPE_SUBTREE, filterstr="memberOf="+full_name, attrlist=["sAMAccountName"])

    logging.warning(u"LdapSearch.get_usernames_in_groups_resultsVK= {}".format(repr([res[1]["sAMAccountName"][0] for res in results] ))) #VK

    return [res[1]["sAMAccountName"][0] for res in results]

def get_user_group_cns(username, base_dns, connection):
    __import__('logging').warning(u'VK{}'.format('9'))
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

    logging.warning(u"LdapSearch.get_user_group_cnsVK= {}".format(repr(cns)))

    return sorted(cns)

def check_editor_access(orgs):
    __import__('logging').warning(u'VK{}'.format('10'))
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
        __import__('logging').warning(u'VK{}'.format('11'))
        base_dn_string = request.params.get("dns") or config["ckanext.cfpb_ldap_query.base_dns"]
        base_dns = base_dn_string.split("|")
        cn = request.params.get("cn")
        roles = make_roles([cn])

        logging.warning(u"LdapSearch.ldap_search_rolesVK= {}".format(repr(roles))) #VK`

        # If you're not a sysadmin, you must be an editor of one of the orgs associate with this group in order to view it
        owner_orgs = set((role["owner_org"] for role in roles.values()[0]))
        try:
            check_access("sysadmin", context())

            logging.warning(u"LdapSearch.ldap_search_accessVK= {}".format(repr(context())))

        except NotAuthorized:
            try: 
                check_editor_access(owner_orgs)

                logging.warning(u"LdapSearch.ldap_search_editor_accessVK= {}".format(repr(check_editor_access(owner_orgs))) ) #VK`

            except NotAuthorized:
                abort(403, "You must be a sysadmin or the have the 'Editor' permission on an org with a resource that uses this group in order to view this page.")

        extra = {
            "dns": base_dns,
            "cn": cn,
            "roles": roles,
            "error_message": "",
        }
        try:
            with _get_ldap_connection() as connection:
                extra["usernames"] = get_usernames_in_group(base_dns, cn, connection)

            logging.warning(u"LdapSearch._extra_usernamesVK= {}".format(repr(extra["usernames"])) ) #VK`

        except GroupNotFound:
            extra["error_message"] = "Group Not Found"
        except:
            extra["error_message"] = "Something went wrong while querying for users. This may be becasue the group has more users than AD's query size limit."

        __import__('logging').warning(u'VK{}'.format('12'))
        return render('ckanext/cfpb-extrafields/ldap_search.html', extra_vars=extra)

    def user_ldap_groups(self, username):
        """"""
        __import__('logging').warning(u'VK{}'.format('13'))
        c.is_sysadmin = False
        if c.user.lower() != username.lower():
            try:
                check_access("sysadmin", context())

                logging.warning(u"LdapSearch.user_ldap_groups_accessVK= {}".format(repr(check_access["sysadmin"])) ) #VK`

                c.is_sysadmin = True
            except NotAuthorized:
                abort(403, "You can only view your own user page unless you're a sysadmin")
        base_dns = config.get("ckanext.cfpb_ldap_query.base_dns").split("|")
        with _get_ldap_connection() as connection:
            cns = get_user_group_cns(username, base_dns, connection)
        roles = make_roles(cns)

        try:
            user_dict = get_action("user_show")(context(), {
                "id": username,
                 "user_obj": c.userobj,
                 "include_datasets": True,
                 "include_num_followers": True})

            logging.warning(u"LdapSearch.user_ldap_groups_user_dictVK= {}".format(repr(user_dict))) #VK`

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
        __import__('logging').warning(u'VK{}'.format('14'))
        return render('ckanext/cfpb-extrafields/ldap_user.html', extra_vars=extra)
