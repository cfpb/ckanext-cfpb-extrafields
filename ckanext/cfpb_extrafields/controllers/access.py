from ckan.plugins.toolkit import BaseController, get_action, render, c as context

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
        return
