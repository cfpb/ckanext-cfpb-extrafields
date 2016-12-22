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

from ckan.plugins.toolkit import BaseController, render, response
import ckanapi

from ckanext.cfpb_extrafields.exportutils import to_csv, FIELDS

def get_datasets(rows=10000):
    """Get datasets (packages) from CKAN"""
    api = ckanapi.LocalCKAN()
    result = api.call_action(
        "package_search",
        {
            "q": "",
            "rows": rows,
        }
    )
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
