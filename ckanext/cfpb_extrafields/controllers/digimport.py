try:
    from cStringIO import StringIO
except ImportError:
    from stringIO import StringIO
import json
import re
import urllib

from ckan.plugins.toolkit import BaseController, redirect_to, render, request, response
import ckanapi

from ckanext.cfpb_extrafields.digutils import make_rec

def make_name(title):
    return re.sub(r"[^a-zA-Z0-9]*", "-", title).lower()

def upload_rec(rec):
    api = ckanapi.LocalCKAN()
    result = api.call_action(
        "package_create",
        rec
    )
    return result

class ImportController(BaseController):
    def index(self, group):
        errors = request.params.get("errors", [])
        if errors:
            try:
                errors = json.loads(errors)
            except json.JSONDecodeError:
                errors = ["Unknown errors detected"]
        return render('ckanext/cfpb-extrafields/import_index.html', {"errors": errors, "group": group})

    def upload(self):
        dig = request.POST["file"].file
        group = request.POST["group"]
        rec, errors = make_rec(dig)
        if errors:
            redirect_to("import_page", errors=json.dumps(errors), group=group)
        else:
            rec["owner_org"] = group
            rec["name"] = make_name(rec["title"])
            rec["notes"] = "Automatically import from DIG"
            upload_rec(rec)
            import logging;logging.error(repr(rec))
        return json.dumps(rec)
