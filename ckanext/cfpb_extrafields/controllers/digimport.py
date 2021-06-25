try:
    from cStringIO import StringIO
except ImportError:
    from stringIO import StringIO
import json
import re
import urllib

from ckan.plugins.toolkit import BaseController, get_action, redirect_to, render, request, response, ValidationError

from ckanext.cfpb_extrafields.digutils import make_rec

def make_name(title):
    return re.sub(r"[^a-zA-Z0-9]+", "-", title).lower()

def upload_rec(rec):
    result = get_action("package_create")({}, rec)
    return result

class ImportController(BaseController):
    def index(self, group):
        errors = request.params.get("errors", [])
        if errors:
            try:
                errors = json.loads(errors)
            except (ValueError, json.JSONDecodeError) as err:
                errors = ["Error while decododing json for the 'error' parameter: {}".format(err.message)]
        return render('ckanext/cfpb-extrafields/import_index.html', {"errors": errors, "group": group})

    def upload(self):
        dig = request.POST["file"].file
        group = request.POST["group"]
        rec, errors = make_rec(dig)

        # The following takes DIG processing "errors" fields impeding intake
        # per CDO we are allowing all DIG values through "as is" and letting
        # CKAN do the error processing/reporting.
        if False: #errors:
            redirect_to("import_page", errors=json.dumps(errors), group=group)
        else:
            rec["owner_org"] = group
            rec["name"] = make_name(request.POST.get("name") or rec.get("title",""))
            rec["notes"] = rec.get("notes","") or "Record automatcially created from DIG file"
            try:
                upload_rec(rec)
            except ValidationError as err:
                errors = ['CKAN validation error for field "{}": {}'.format(field, ";".join(errs)) for field, errs in err.error_dict.items()]
                redirect_to("import_page", errors=json.dumps(errors), group=group)

        redirect_to("dataset_read", id=rec["name"])
