import ckan.plugins as p
import ckan.plugins.toolkit as tk
import validators as v
import options as opts
import datastore_actions as ds
import collections

# if tag usage is going to be expanded, the following should be generalized.
def create_relevant_governing_documents():
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'relevant_governing_documents'}
        tk.get_action('vocabulary_show')(context, data)
    except tk.ObjectNotFound:
        data = {'name': 'relevant_governing_documents'}
        vocab = tk.get_action('vocabulary_create')(context, data)
        for tag in opts.relevant_governing_documents(): 
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            tk.get_action('tag_create')(context, data)
def tag_relevant_governing_documents():
    create_relevant_governing_documents()
    try:
        tag_list = tk.get_action('tag_list')
        tags = tag_list(data_dict={'vocabulary_id': 'relevant_governing_documents'})
        return tags
    except tk.ObjectNotFound:
        return None

# these go into a new popup module if there are more than a few fields
def popup_relevant_governing_documents():
    return "Insert purpose of relevant_governing_documents field."
def popup_data_source_names():
    return "Insert purpose of source names field."
def popup_usage_restrictions():
    return "Enter instructions for what users can and cannot do with the data."

class ExampleIDatasetFormPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):

    p.implements(p.IResourceController)
    def before_create(self, context, resource):
        return
    def after_create(self, context, resource):
        # must have changed['format'] when you created the resource
        tk.redirect_to(controller='package',action='resource_edit',
                       resource_id=resource['id'],id=resource['package_id'])
    def before_update(self, context, current, resource):
        # note keys that have changed
        self.changed_keys = ['format', 'privacy_contains_pii']
        self.changed = {}
        for i in self.changed_keys:
            self.changed[i] = False
            if current.get(i,'') != resource.get(i,''):
                print 'trigger a redirect in after_update: ', self.changed.get(i,'')
                self.changed[i] = True


        record = eval(resource.get('datadict',''))
        if record:
            ds.delete_datadict(resource['id']) 
            ds.create_datadict(resource['id'],record,'')
            print ds.get_datadict(resource['id'])
        resource.pop('datadict', None)


        return
    def _email_field_change(self, field):
        # if privacy fields have changed notify the relevant people
        if self.changed.get(field,False):
            print 'trigger email on change to '+field 
            # filter by dataset name?
            # could get dataset followers list;
            followers = tk.get_action('dataset_follower_list')(context,{'id': resource['package_id']})
            for f in followers:
                # filter by group
                # get emails 
                print tk.get_action('user_show')(context,{'id': f['id']})['email']
            # send a notification of change by email
    def after_update(self, context, resource):
        self._email_field_change('privacy_contains_pii')
        if self.changed.get('format',False):
            tk.redirect_to(controller='package',action='resource_edit',
                           resource_id=resource['id'],id=resource['package_id'])
        for i in self.changed_keys:
            self.changed[i] = False
        return
    def before_delete(self, context, resource, resources):
        return
    def after_delete(self, context, resources):
        return
    def before_show(self, resource_dict):
        return


    p.implements(p.ITemplateHelpers)
    def get_helpers(self):
        return {'clean_select_multi': v.clean_select_multi,
                'options_format': opts.format,
                'options_storage_location': opts.storage_location,
                'options_legal_authority_for_collection': opts.legal_authority_for_collection,
                'options_privacy_pia_title': opts.privacy_pia_title,
                'options_privacy_sorn_number': opts.privacy_sorn_number,
                'tag_relevant_governing_documents': tag_relevant_governing_documents, 
                'options_relevant_governing_documents': opts.relevant_governing_documents,
                'options_content_periodicity': opts.content_periodicity,
                'options_update_frequency': opts.update_frequency,
                'options_content_spatial': opts.content_spatial,
                'options_acquisition_method': opts.acquisition_method,
                'options_pra_exclusion': opts.pra_exclusion,
                'options_privacy_pia_notes': opts.privacy_pia_notes,
                'options_transfer_method': opts.transfer_method,
                'options_sensitivity_level': opts.sensitivity_level,
                'options_update_size': opts.update_size,
                'options_approximate_total_size': opts.approximate_total_size,
                'options_resource_type': opts.resource_type,

                'popup_relevant_governing_documents': popup_relevant_governing_documents,
                'popup_data_source_names': popup_data_source_names,
                'popup_usage_restrictions': popup_usage_restrictions,

                'create_datadict':ds.create_datadict,
                'create_generic_json':ds.create_generic_json,
                'get_datadict':ds.get_datadict,                
                'update_datadict':ds.update_datadict,
                'delete_datadict':ds.delete_datadict,

                'get_datastore':ds.get_datastore,
                'delete_datastore':ds.delete_datastore,

                'get_datadict_html':ds.get_datadict_html,
                
                }
    
    p.implements(p.IDatasetForm)
    def _modify_package_schema(self, schema):
        schema.update({
            # notes is the "Descriptions" built-in field.
            'notes': [tk.get_validator('not_empty')],
            'data_source_names': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'access_restrictions': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'contact_primary_name': [tk.get_converter('convert_to_extras'),
                                     tk.get_validator('not_empty')],
            'contact_primary_email': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'contact_secondary_name': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'contact_secondary_email': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'initial_purpose_for_intake': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'legal_authority_for_collection': [tk.get_validator('ignore_missing'),
                        v.input_value_validator,
                        tk.get_converter('convert_to_extras')],
            'pra_omb_control_number': [tk.get_validator('ignore_missing'),
                        v.pra_control_num_validator,
                        tk.get_converter('convert_to_extras')],
            'privacy_pia_title': [tk.get_validator('ignore_missing'),
                        v.input_value_validator,
                        tk.get_converter('convert_to_extras')],
            'privacy_sorn_number': [tk.get_validator('ignore_missing'),
                        v.input_value_validator,
                        tk.get_converter('convert_to_extras')],
            'dig_id': [tk.get_validator('ignore_missing'),
                        v.dig_id_validator,
                        tk.get_converter('convert_to_extras')],
            'usage_restrictions' : [ tk.get_validator('ignore_missing'),
                                     tk.get_converter('convert_to_extras')],
            'obfuscated_title': [tk.get_validator('ignore_missing'),
                                 tk.get_converter('convert_to_extras')],
            'transfer_details': [tk.get_validator('ignore_missing'),
                                 tk.get_converter('convert_to_extras')],
            'transfer_initial_size': [tk.get_validator('ignore_missing'),
                                      v.positive_number_validator,
                                      tk.get_converter('convert_to_extras')],
            'transfer_method': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'also_known_as': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'content_periodicity': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'content_spatial': [tk.get_validator('ignore_missing'),
                                v.input_value_validator,
                        tk.get_converter('convert_to_extras')],
            'update_frequency': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'website_name': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'website_url': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'wiki_link': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'dataset_notes': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'access_notes': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'acquisition_method': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'pra_exclusion': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'dataset_last_modified_date': [tk.get_validator('ignore_missing'),
                                           v.reasonable_date_validator,
                        tk.get_converter('convert_to_extras')],
            'pra_omb_expiration_date': [tk.get_validator('ignore_missing'),
                                           v.reasonable_date_validator,
                        tk.get_converter('convert_to_extras')],
            'privacy_has_privacy_act_statement': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'privacy_pia_notes': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'records_retention_schedule': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'procurement_document_id': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],

        })
        # this update is for special fields that become free tags AND normal fields.
        schema.update({'subject_matter': [tk.get_converter('tag_string_convert'),tk.get_converter('convert_to_extras'),]})
        # now modify tag fields and convert_to_tags
        schema.update({
            'relevant_governing_documents': [
                tk.get_validator('ignore_missing'),
                tk.get_converter('convert_to_tags')('relevant_governing_documents')]
        })
        schema['resources'].update({
                'approximate_total_size' : [tk.get_validator('ignore_missing'),],
                'content_temporal_range_end' : [v.end_after_start_validator, v.reasonable_date_validator, tk.get_validator('ignore_missing'),], 
                'content_temporal_range_start' : [v.end_after_start_validator, v.reasonable_date_validator, tk.get_validator('ignore_missing'),],
                'cleansing_rules_used' : [tk.get_validator('ignore_missing'),],
                'intake_date' : [v.reasonable_date_validator, tk.get_validator('ignore_missing'),],
                'privacy_contains_pii' : [tk.get_validator('ignore_missing'),],
                'privacy_has_direct_identifiers' : [tk.get_validator('ignore_missing'),],
                'resource_type' : [tk.get_validator('ignore_missing'),],
                'sensitivity_level' : [tk.get_validator('ignore_missing'),],
                'storage_location' : [tk.get_validator('ignore_missing'),],
                'storage_location_path' : [tk.get_validator('ignore_missing'),],
                'update_size' : [tk.get_validator('ignore_missing'),],
        })
        return schema
    def create_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema
    def update_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema
    def show_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).show_package_schema()
        schema.update({
            # notes is the "Descriptions" built-in field.
            'notes': [tk.get_validator('not_empty')],
            'data_source_names': [tk.get_converter('convert_from_extras'),],
            'access_restrictions': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'contact_primary_name': [tk.get_converter('convert_from_extras'),],
            'contact_primary_email': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'contact_secondary_email': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'contact_secondary_name': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'initial_purpose_for_intake': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'legal_authority_for_collection': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'pra_omb_control_number': [tk.get_converter('convert_from_extras'),
                                tk.get_validator('ignore_missing')],
            'obfuscated_title': [tk.get_converter('convert_from_extras'),
                                 tk.get_validator('ignore_missing')],
            'transfer_details': [tk.get_converter('convert_from_extras'),
                                 tk.get_validator('ignore_missing')],
            'transfer_initial_size': [tk.get_converter('convert_from_extras'),
                                      v.positive_number_validator,
                                      tk.get_validator('ignore_missing')],
            'transfer_method': [tk.get_converter('convert_from_extras'),
                                tk.get_validator('ignore_missing')],
            'also_known_as': [tk.get_converter('convert_from_extras'),
                              tk.get_validator('ignore_missing')],
            'content_periodicity': [tk.get_converter('convert_from_extras'),
                                    tk.get_validator('ignore_missing')],
            'content_spatial': [tk.get_converter('convert_from_extras'),
                                tk.get_validator('ignore_missing')],
            'update_frequency': [tk.get_converter('convert_from_extras'),
                                 tk.get_validator('ignore_missing')],
            'website_name': [tk.get_converter('convert_from_extras'),
                             tk.get_validator('ignore_missing')],
            'website_url': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'wiki_link': [tk.get_converter('convert_from_extras'),
                          tk.get_validator('ignore_missing')],
            'dataset_notes': [tk.get_converter('convert_from_extras'),
                             tk.get_validator('ignore_missing')],
            'access_notes': [tk.get_converter('convert_from_extras'),
                             tk.get_validator('ignore_missing')],
            'acquisition_method': [tk.get_converter('convert_from_extras'),
                                    tk.get_validator('ignore_missing')],
            'pra_exclusion': [tk.get_converter('convert_from_extras'),
                              tk.get_validator('ignore_missing')],
            'dataset_last_modified_date': [tk.get_converter('convert_from_extras'),
                                           v.reasonable_date_validator,
                                           tk.get_validator('ignore_missing')],
            'pra_omb_expiration_date': [tk.get_converter('convert_from_extras'),
                                        tk.get_validator('ignore_missing')],
            'privacy_has_privacy_act_statement': [tk.get_converter('convert_from_extras'),
                                                  tk.get_validator('ignore_missing')],
            'privacy_pia_notes': [tk.get_converter('convert_from_extras'),
                                  tk.get_validator('ignore_missing')],
            'records_retention_schedule': [tk.get_converter('convert_from_extras'),
                                           tk.get_validator('ignore_missing')],
            'procurement_document_id': [tk.get_converter('convert_from_extras'),
                                        tk.get_validator('ignore_missing')],
            'privacy_pia_title': [tk.get_converter('convert_from_extras'),
                                  tk.get_validator('ignore_missing')],
            'privacy_sorn_number': [tk.get_converter('convert_from_extras'),
                                    tk.get_validator('ignore_missing')],
            'dig_id': [tk.get_converter('convert_from_extras'),
                       tk.get_validator('ignore_missing')],
            'usage_restrictions' : [tk.get_converter('convert_from_extras'),
                                    tk.get_validator('ignore_missing')],
        })
        schema['resources'].update({
                'approximate_total_size' : [ tk.get_validator('ignore_missing'),],
                'cleansing_rules_used' : [tk.get_validator('ignore_missing'),],
                'content_temporal_range_end' : [tk.get_validator('ignore_missing'),],
                'content_temporal_range_start' : [tk.get_validator('ignore_missing'),],
                'intake_date' : [tk.get_validator('ignore_missing'),],
                'privacy_contains_pii' : [ tk.get_validator('ignore_missing'),],
                'privacy_has_direct_identifiers' : [ tk.get_validator('ignore_missing'),],
                'resource_type' : [ tk.get_validator('ignore_missing'),],
                'sensitivity_level' : [ tk.get_validator('ignore_missing'),],
                'storage_location' : [ tk.get_validator('ignore_missing'),],
                'storage_location_path' : [ tk.get_validator('ignore_missing'),],  
                'update_size' : [ tk.get_validator('ignore_missing'),],
        })
        # this update is for special fields that become free tags AND normal fields.
        schema.update({'subject_matter': [tk.get_converter('convert_from_extras'),]})
        # this prevents vocabulary tags from polluting the free tag namespace somehow
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))
        # now show tag fields and convert_from_tags
        schema.update({
            'relevant_governing_documents': [
                tk.get_converter('convert_from_tags')('relevant_governing_documents'),
                tk.get_validator('ignore_missing')]
            })
        return schema
    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True
    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
    
    p.implements(p.IConfigurer)
    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')
        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        tk.add_public_directory(config, 'public')
        # Register this plugin's fanstatic directory with CKAN.
        # Here, 'fanstatic' is the path to the fanstatic directory
        # (relative to this plugin.py file), and 'example_theme' is the name
        # that we'll use to refer to this fanstatic directory from CKAN
        # templates.
        tk.add_resource('fanstatic','cfpb_extrafields')

    p.implements(p.IFacets)
    def _change_facets(self, facets_dict):
        dummy_facets = facets_dict
        facets_dict = collections.OrderedDict()
        # example facet added
        facets_dict['acquisition_method'] = p.toolkit._('Acquisition Method')
        for key in dummy_facets.keys():
            facets_dict[key] = dummy_facets[key]
        # hide License facet because it is not used by cfpb
        facets_dict.pop('license_id', None)
        return facets_dict
    def dataset_facets(self, facets_dict, package_type):
        return self._change_facets(facets_dict)
    def group_facets(self, facets_dict, group_type, package_type):
        return self._change_facets(facets_dict)
    def organization_facets(self, facets_dict, organization_type, package_type):
        return self._change_facets(facets_dict)
