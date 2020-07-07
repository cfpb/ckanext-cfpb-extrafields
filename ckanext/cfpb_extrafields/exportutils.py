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


FIELDS = [
    ("dig_id", "DIG ID"),
    ("title", "Dataset title"),
    ("notes", "Description"),
    ("private", "Visibility"),
    ("organization.name", "Organization"),
    ("also_known_as", "Also known as"),
    ("data_source_names", "Data sources"),
    ("source_categories", "Source Categories"),
    ("content_temporal_range_start", "Content start date"),
    ("content_temporal_range_end", "Content end date"),
    ("content_periodicity", "Content periodicity"),
    ("content_spatial", "Content spatial coverage"),
    ("update_frequency", "Update frequency"),
    ("wiki_link", "Wiki link"),
    ("website_url", "Reference website URL"),
    ("contact_primary_name", "Primary contact name"),
    ("contact_primary_email", "Primary contact email"),
    ("contact_secondary_name", "Secondary contact name"),
    ("contact_secondary_email", "Secondary contact email"),
    ("access_restrictions", "Access restrictions"),
    ("access_notes", "How to get access"),
    ("usage_restrictions", "Usage restrictions"),
    ("dataset_notes", "Dataset notes"),
    ("obfuscated_title", "Obfuscated title"),
    ("transfer_details", "Transfer details"),
    ("transfer_initial_size", "Transfer initial size (MB)"),
    ("transfer_method", "Transfer method"),
    ("sensitivity_level", "Sensitivity level"),
    ("legal_authority_for_collection", "Legal authority for collection"),
    ("relevant_governing_documents", "Relevant governing documents"),
    ("initial_purpose_for_intake", "Initial purpose for intake"),
    ("pra_exclusion", "PRA exemption"),
    ("pra_omb_control_number", "PRA: OMB control number"),
    ("pra_omb_expiration_date", "PRA: OMB expiration date"),
    ("privacy_contains_pii", "Privacy: contains PII?"),
    ("privacy_contains_ssn", "Privacy: contains SSN?"),
    ("privacy_has_direct_identifiers", "Privacy: has direct identifiers?"),
    ("privacy_pia_title", "Privacy: PIA title"),
    ("privacy_pia_notes", "Privacy: PIA notes"),
    ("privacy_sorn_number", "Privacy: SORN number"),
    ("records_retention_schedule", "Records retention schedule"),
    ("procurement_document_id", "Procurement document ID"),
    ("obligation", "Obligation"),
    ("transfer_date", "Transfer: Date"),
    ("data_governance_notes", "Data Governance: Notes"),
    ("legal_notes","Legal: Notes"),
    ("pra_notes","PRA: Notes"),
    ("privacy_notes","Privacy: Notes"),
    # New
    ("website_name", "Reference Website Name"),
    ("cleansing_rules_used", "cleansing rules used"),
    ("dataset_last_modified_date", "Dataset Last Modified Date"),
    ("foia_exemptions", "FOIA: Exemptions"),
    ("foia_exemptions_notes", "FOIA Exemption Notes"),
    ("opendata_indicator", "Open Data: open data indicator"),
    ("opendata_priority_indicator", "Open Data: priority indicator"),
    ("opendata_public_location", "Open Data: public location"),

]

try:
    basestring
except NameError:
    basestring = str

def flatten(data, list_sep=","):
    """Convert a nested dictionary to a flat data structure
    flattened keys are separated by dots
    Value encodings:
    * lists of strings are joined by list_sep if it's present
    * all other lists are json-encoded
    * dicts are recursively flattened
    * all other values are included verbatim

    Example:
        {"child":{"name": "Bob", "fav_foods": ["apples", "bananas"],
            "parents": [{"name": "John"}, {"name": "Sue"}]}}
        ->
        {"child.name": "Bob", "child.fav_foods": "apples,bananas", "parents": "<json encoded list>"}
    """
    result = {}
    for key, val in data.items():
        if isinstance(val, basestring):
            result[key] = val.encode("utf-8")
        elif hasattr(val, "items"):
            for ikey, ival in flatten(val, list_sep=list_sep).items():
                result[key + "." + ikey] = ival
        elif hasattr(val, "__iter__") and val:
            #assume it's a list
            if isinstance(val[0], basestring) and list_sep:
                result[key] = list_sep.join(map(str, val)).encode("utf-8")
            else:
                result[key] = json.dumps(val).encode("utf-8")
        else:
            #int?
            result[key] = val
    return result

def to_csv(data, fields, fieldmap=tuple(FIELDS)):
    """Convert data to an excel-style csv

    :param data: list of dictionaries of data (each dict is 1 row)
    :param fields: which fields (keys in the dict) to write
    :param fieldmap: dict mapping keys in the dict to human-readable names
        which will appear as the first line of the csv
    """
    output = StringIO()
    writer = csv.DictWriter(output, [f[0] for f in fields], extrasaction="ignore")
    writer.writerow(dict(fieldmap))
    for result in data:
        row = flatten(result)
        #If blank, default to "no"
        row["privacy_contains_ssn"] = row.get("privacy_contains_ssn") or "no"
        writer.writerow(row)
    return output.getvalue()
