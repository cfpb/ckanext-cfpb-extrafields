from ckan.plugins.toolkit import BaseController, url_for, config, get_action, request, render, redirect_to, c as context
from ckan.lib.helpers import flash_error, flash_notice, get_site_protocol_and_host
import requests
from requests.auth import HTTPBasicAuth
import json

def get_role(roles, role_name):
    for role in roles:
        if role[0] == role_name:
            return {
                "role": role[0],
                "description": role[1]
            }

class AccessController(BaseController):
    def index(self, resource_id, cn):

        try:
            dns = config.get("ckanext.cfpb_ldap_query.base_dns").split('|')
        except ValueError:
            flash_error("At least one valid DN must be configured.")
            redirect_to("get_access_request", resource_id=resource_id, cn=cn)

        resource = get_action('resource_show')({}, data_dict={
            'id': resource_id
        })

        package = get_action('package_show')({}, data_dict={
            'id': resource['package_id']
        })

        role_description = get_role(json.loads(resource['db_roles']), cn)['description']

        return render(
            'ckanext/cfpb-extrafields/access_index.html',
            {
                "resource": resource, "package": package,
                "description": role_description,
                "cn": cn, "context": context, "dn": dns[0]
            }
        )

    def submit(self, resource_id, cn):
        try:
            workflow_url = config['ckanext.access.workflow_url']
        except KeyError:
            flash_error("Please set ckanext.access.workflow_url in order to submit access requests.")
            redirect_to("get_access_request", resource_id=resource_id, cn=cn)

        try:
            workflow_user = config['ckanext.access.workflow_user']
        except KeyError:
            flash_error("Please set ckanext.access.workflow_user in order to submit access requests.")
            redirect_to("get_access_request", resource_id=resource_id, cn=cn)

        try:
            workflow_pass = config['ckanext.access.workflow_pass']
        except KeyError:
            flash_error("Please set ckanext.access.workflow_pass in order to submit access requests.")
            redirect_to("get_access_request", resource_id=resource_id, cn=cn)

        try:
            dns = config.get("ckanext.cfpb_ldap_query.base_dns").split('|')
        except ValueError:
            flash_error("At least one valid DN must be configured.")
            redirect_to("get_access_request", resource_id=resource_id, cn=cn)

        resource = get_action('resource_show')({}, data_dict={
            'id': resource_id
        })

        package = get_action('package_show')({}, data_dict={
            'id': resource['package_id']
        })

        role_description = get_role(json.loads(resource['db_roles']), cn)['description']

        dataset_url = '://'.join(get_site_protocol_and_host()) + url_for(controller='package', action='read', id=package['name'])

        workflow_json = {
            "workflowArgs": {
                "datasetTitle": package['title'],
                "groupDN": "CN={},{}".format(cn, dns[0]),
                "sAMAccountName": request.POST['user'],
                "dataStewardEmail": package['contact_primary_email'],
                "dataStewardEmail2": package['contact_secondary_email'],
                "description": role_description,
                "usageRestriction": package['usage_restrictions'],
                "justification": request.POST['justification'],
                "accessRestriction": package['access_restrictions'],
                "url": dataset_url
            }
        }

        try:
            response = requests.post(
                workflow_url,
                json=workflow_json,
                auth=HTTPBasicAuth(workflow_user, workflow_pass),
                verify=True
            )
            flash_notice("Access request has been sent, you will recieve email updates on the status of the request as it is processed.")
        except Exception as e:
            flash_error("Error occurred submitting request: {} with content {}".format(e, workflow_json))
            redirect_to("get_access_request", resource_id=resource_id, cn=cn)
            return

        redirect_to("dataset_read", id=package['id'])
