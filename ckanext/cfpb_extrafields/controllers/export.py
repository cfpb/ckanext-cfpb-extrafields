try:
    from cStringIO import StringIO
except ImportError:
    from stringIO import StringIO
import csv
import json

from ckan.plugins.toolkit import BaseController, render, response
import ckanapi

FIELDS = [
    ("title", "Dataset Title"),
    ("private", "Visibility"),
    ("notes", "Description"),
    # ("i", "Subject Matter"),
    ("organization.name", "Organization"),
    ("also_known_as", "Also Known As"),
    ("data_source_names", "Data Sources"),
    ("content_temporal_range_start", "Content Start Date"),
    ("content_temporal_range_end", "Content End Date"),
    ("content_periodicity", "Content Periodicity"),
    ("content_spatial", "Content Spatial Coverage"),
    ("update_frequency", "Update Frequency"),
    ("wiki_link", "Wiki Link"),
    ("website_url", "Reference Website URL"),
    ("contact_primary_email", "Primary Contact"),
    ("contact_secondary_email", "Secondary Contact"),
    ("access_notes", "How to Get Access"),
    ("access_restrictions", "Access Restrictions"),
    ("usage_restrictions", "Usage Restrictions"),
    ("dataset_notes", "Dataset Notes"),
    # ("i", "Dataset Last Modified Date"),
    ("obfuscated_title", "Obfuscated Title"),
    ("transfer_details", "Transfer Details"),
    ("dig_id", "Transfer Initial Size (mb)"),
    ("transfer_initial_size", "Transfer Method"),
    ("transfer_method", "Sensitivity Level"),
    ("sensitivity_level", "Legal Authority for Collection"),
    ("legal_authority_for_collection", "Relevant Governing Documents"),
    ("relevant_governing_documents", "DIG ID"),
    ("initial_purpose_for_intake", "Initial Purpose for Intake"),
    ("pra_exclusion", "PRA Exclusion"),
    ("pra_omb_control_number", "PRA: OMB Control Number"),
    ("pra_omb_expiration_date", "PRA: OMB Expiration Date"),
    ("privacy_contains_pii", "Privacy: Contains PII?"),
    ("privacy_has_direct_identifiers", "Privacy: Has Direct Identifiers?"),
    ("privacy_has_privacy_act_statement", "Privacy: Has Privacy Act statement?"),
    ("privacy_pia_title", "Privacy: PIA title"),
    ("privacy_sorn_number", "Privacy: SORN number"),
    ("records_retention_schedule", "Records retention schedule"),
    ("procurement_document_id", "Procurement document ID"),
]

try:
    basestring
except NameError:
    basestring = str

def flatten(data, list_sep=","):
    result = {}
    for k, v in data.items():
        if isinstance(v, basestring):
            result[k] = v.encode("utf-8")
        elif hasattr(v, "items"):
            for ikey, ival in flatten(v).items():
                result[k + "." + ikey] = ival
        elif hasattr(v, "__iter__") and v:
            #assume it's a list
            if isinstance(v[0], basestring):
                result[k] = list_sep.join(map(str, v)).encode("utf-8")
            else:
                result[k] = json.dumps(v).encode("utf-8")
        else:
            #int?
            result[k] = v
    return result

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
    writer = csv.DictWriter(output, [f[0] for f in fields], extrasaction="ignore")
    writer.writerow(dict(FIELDS))
    for result in data["results"]:
        writer.writerow(flatten(result))
    return output.getvalue()

class ExportController(BaseController):
    def index(self):
        return render('ckanext/cfpb-extrafields/export_index.html')

    def csv(self):
        datasets = get_datasets()
        csvdata = to_csv(datasets, FIELDS)
        response.content_disposition = "attachment; filename=packages.csv"
        response.content_type = "text/csv"
        response.content_length = len(csvdata)

        return csvdata

# if __name__ == "__main__":
    # import fileinput
    # data = json.loads("\n".join(fileinput.input()))
    # result = to_csv(data["result"], FIELDS)
    # with open("results2.csv", "w") as f:
        # f.write(result)
