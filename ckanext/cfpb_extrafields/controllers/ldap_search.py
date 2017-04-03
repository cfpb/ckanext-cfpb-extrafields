"""Export all datasets to excel-compatible csv.

Currently only exports public datasets, but once CKAN is upgraded to v2.4+,
the code can be updated to support private datasets.
"""
from ckan.plugins.toolkit import BaseController, config, render, request
from ckanext.ldap.controllers.user import _get_ldap_connection
import ldap
import ldap.filter

def get_user_stats(username, connection):
    results = connection.search_s(config['ckanext.ldap.base_dn'], ldap.SCOPE_SUBTREE, filterstr="sAMAccountName="+ldap.filter.escape_filter_chars(username))
    return results[0][1]

def find_groups(ou, cn, connection):
    results = connection.search_s("OU="+ldap.filter.escape_filter_chars(ou)+",DC=cfpb,DC=local", ldap.SCOPE_SUBTREE, filterstr="CN="+ldap.filter.escape_filter_chars(cn))
    return results

def get_group_full_name(ou, cn, connection):
    return find_groups(ou, cn, connection)[0][0]

def get_usernames_in_group(ou, cn, connection):
    full_name = get_group_full_name(ou, cn, connection)
    results = connection.search_s(config['ckanext.ldap.base_dn'], ldap.SCOPE_SUBTREE, filterstr="memberOf="+full_name, attrlist=["sAMAccountName"])
    return [res[1]["sAMAccountName"][0] for res in results]

class LdapSearchController(BaseController):
    def ldap_search(self):
        """"""
        ou = request.params.get("ou")
        cn = request.params.get("cn")
        with _get_ldap_connection() as connection:
            usernames = get_usernames_in_group(ou, cn, connection)
        extra = {
            "ou": ou,
            "cn": cn,
            "usernames": usernames,
        }
        return render('ckanext/cfpb-extrafields/ldap_search.html', extra_vars=extra)
