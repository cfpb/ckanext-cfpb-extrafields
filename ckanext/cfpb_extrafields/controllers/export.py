try:
    from cStringIO import StringIO
except ImportError:
    from stringIO import StringIO
import csv
import json

from ckan.plugins.toolkit import BaseController, render, response
import ckanapi

FIELDS = [
    'access_notes',
    'access_restrictions',
    'also_known_as',
    'author',
    'author_email',
    'contact_primary_email',
    'contact_primary_name',
    'contact_secondary_email',
    'contact_secondary_name',
    'content_periodicity',
    'content_spatial',
    'content_temporal_range_end',
    'content_temporal_range_start',
    'creator_user_id',
    'data_source_names',
    'dataset_notes',
    'dig_id',
    'groups',
    'id',
    'initial_purpose_for_intake',
    'isopen',
    'legal_authority_for_collection',
    'license_id',
    'license_title',
    'maintainer',
    'maintainer_email',
    'metadata_created',
    'metadata_modified',
    'name',
    'notes',
    'num_resources',
    'num_tags',
    'obfuscated_title',
    'organization.approval_status',
    'organization.created',
    'organization.description',
    'organization.id',
    'organization.image_url',
    'organization.is_organization',
    'organization.name',
    'organization.revision_id',
    'organization.state',
    'organization.title',
    'organization.type',
    'owner_org',
    'pra_exclusion',
    'pra_omb_control_number',
    'privacy_contains_pii',
    'privacy_has_direct_identifiers',
    'privacy_has_privacy_act_statement',
    'privacy_pia_notes',
    'privacy_pia_title',
    'privacy_sorn_number',
    'private',
    'procurement_document_id',
    'records_retention_schedule',
    'relationships_as_object',
    'relationships_as_subject',
    'relevant_governing_documents',
    'resources',
    'revision_id',
    'sensitivity_level',
    'state',
    'tags',
    'title',
    'tracking_summary.recent',
    'tracking_summary.total',
    'transfer_details',
    'transfer_initial_size',
    'transfer_method',
    'type',
    'update_frequency',
    'url',
    'usage_restrictions',
    'version',
    'website_name',
    'website_url',
    'wiki_link'
]

def flatten(data, list_sep=","):
    result = {}
    for k, v in data.items():
        if isinstance(v, "".__class__):
            result[k] = v
        elif hasattr(v, "items"):
            for ikey, ival in flatten(v).items():
                result[k + "." + ikey] = ival
        elif hasattr(v, "__iter__") and v:
            #assume it's a list
            if isinstance(v[0], "".__class__):
                result[k] = list_sep.join(map(str, v))
            else:
                result[k] = json.dumps(v)
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
    writer = csv.DictWriter(output, fields, extrasaction="ignore")
    writer.writeheader()
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
