try:
    from cStringIO import StringIO
except ImportError:
    from stringIO import StringIO
import json
import urllib

from ckan.plugins.toolkit import BaseController, redirect_to, render, request, response
import ckanapi

from ckanext.cfpb_extrafields.digutils import make_rec

# def get_datasets(rows=10000):
    # api = ckanapi.LocalCKAN()
    # result = api.call_action(
        # "package_search",
        # {
            # "q": "",
            # "rows": rows,
        # }
    # )
    # return result

class ImportController(BaseController):
    def index(self):
        errors = request.params.get("errors", [])
        if errors:
            try:
                errors = json.loads(errors)
            except json.JSONDecodeError:
                errors = ["Unknown errors detected"]
        return render('ckanext/cfpb-extrafields/import_index.html', {"errors": errors})

    def upload(self):
        dig = request.POST["file"].file
        rec, errors = make_rec(dig)
        if errors:
            redirect_to("import_page", errors=json.dumps(errors))
        return json.dumps(rec)
