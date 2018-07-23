from ckan.plugins.toolkit import BaseController, get_action, render, c as context, flash_error
import requests

class AccessController(BaseController):
    def index(self, resource_id, cn):
        resource = get_action('resource_show')({}, data_dict={
            'id': resource_id
        })

        package = get_action('package_show')({}, data_dict={
            'id': resource['package_id']
        })

        return render('ckanext/cfpb-extrafields/access_index.html', {"resource": resource, "package": package, "cn": cn, "context": context})

    def submit(self, resource_id, cn):
        try:
            workflow_url = config['ckanext.access.workflow_url']
        except KeyError:
            flash_error("Please set ckanext.access.workflow_url in order to submit access requests.")
            redirect_to("request_access", resource_id=resource_id, package_id=package_id)

        resource = get_action('resource_show')({}, data_dict={
            'id': resource_id
        })

        package = get_action('package_show')({}, data_dict={
            'id': resource['package_id']
        })

        redirect_to("resource_read", id=resource.id)

        #response = requests.post(
#
#        )
