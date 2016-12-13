try:
    from cStringIO import StringIO
except ImportError:
    from stringIO import StringIO

from ckan.plugins.toolkit import BaseController, render, response
import ckanapi

def get_datasets(rows=10000):
    api = ckanapi.LocalCKAN()
    result = api.call_action(
        "package_search",
        {
            "q": "",
            "rows": rows,
        }
    )
    return result

def to_csv(data, fields):
    output = StringIO()
    writer = csv.DictWriter(output, fields)
    writer.writeheader()
    for result in data["results"]:
        writer.writerow(result)
    return output.getvalue()

class ExportController(BaseController):
    def index(self):
        return render('ckanext/cfpb-extrafields/export_index.html')

    def csv(self):
        datasets = get_datasets()
        csvdata = to_csv(datasets, ["id", "description"])
        response.content_disposition = "attachment; filename=packages.csv"
        response.content_type = "text/csv"
        response.content_length = len(csvdata)

        return csvdata
