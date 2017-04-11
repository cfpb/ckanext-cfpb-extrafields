"""Export all datasets to excel-compatible csv.

Currently only exports public datasets, but once CKAN is upgraded to v2.4+,
the code can be updated to support private datasets.
"""
from ckan.plugins.toolkit import BaseController, config, render, request
from ckanext.ldap.controllers.user import _get_ldap_connection
import ldap
import ldap.filter

class GroupNotFound(Exception):
    pass

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



class LdapSearchController(BaseController):
    def ldap_search(self):
        """"""
        # ou = request.params.get("ou")
        base_dn_string = request.params.get("dns") or config["ckanext.cfpb_ldap_query.base_dns"]
        base_dns = base_dn_string.split("|")
        cn = request.params.get("cn")
        extra = {
            "dns": base_dns,
            "cn": cn,
            "error_message": "",
        }
        try:
            with _get_ldap_connection() as connection:
                extra["usernames"] = get_usernames_in_group(base_dns, cn, connection)
        except GroupNotFound:
            extra["error_message"] = "Group Not Found"

        return render('ckanext/cfpb-extrafields/ldap_search.html', extra_vars=extra)

    def user_groups(self):
        """"""
        username = request.params.get("username")
        base_dns = config.get("ckanext.cfpb_ldap_query.base_dns").split("|")
        with _get_ldap_connection() as connection:
            cns = get_user_group_cns(username, base_dns, connection)
        extra = {
            "username": username,
            "cns": cns,
        }
        return render('ckanext/cfpb-extrafields/ldap_user.html', extra_vars=extra)
