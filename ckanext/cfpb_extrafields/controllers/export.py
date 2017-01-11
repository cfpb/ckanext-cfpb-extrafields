"""Export all datasets to excel-compatible csv.

Currently only exports public datasets, but once CKAN is upgraded to v2.4+,
the code can be updated to support private datasets.
"""
try:
    from cStringIO import StringIO
except ImportError:
    from stringIO import StringIO
import csv
import json

from ckan.plugins.toolkit import BaseController, check_ckan_version, get_action, render, response

from ckanext.cfpb_extrafields.exportutils import to_csv, FIELDS

def get_datasets(rows=10000):
    """Get datasets (packages) from CKAN"""
    data_dict = {
        "q": "",
        "rows": rows,
    }
    if check_ckan_version('2.6'):
        data_dict["include_private"] = True

    result = get_action("package_search")({}, data_dict)
    return result

class ExportController(BaseController):
    def index(self):
        """Basic page with a button for exporting data"""
        return render('ckanext/cfpb-extrafields/export_index.html')

    def csv(self):
        """Returns a download with csv of all datasets"""
        datasets = get_datasets()
        csvdata = to_csv(datasets["results"], FIELDS)
        response.content_disposition = "attachment; filename=datasets.csv"
        response.content_type = "text/csv"
        response.content_length = len(csvdata)

        return csvdata
