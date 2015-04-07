import ckan.plugins as p
import ckan.plugins.toolkit as tk
import pprint
import validators as v
import options as opts

def clean_select_multi(a):
    ''' parses the results of an html form select multiple '''
    # convert to string if a list
    a = ''.join(a) 
    # convert back to comma separated array 
    a = a.split(',') 
    # kill special characters
    a = [item.strip('{}"') for item in a]
    return a

class ExampleIDatasetFormPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def get_helpers(self):
        return {'clean_select_multi': clean_select_multi,
                'options_format_cfpb': opts.format_cfpb,
                'options_storage_location': opts.storage_location,
                'options_legal_authority_for_collection': opts.legal_authority_for_collection,
                'options_privacy_pia_title': opts.privacy_pia_title,
                'options_privacy_sorn_number': opts.privacy_sorn_number,
                'options_relevant_governing_documents': opts.relevant_governing_documents,
                }

    def _modify_package_schema(self, schema):
        schema.update({
            'source_names': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'access_restrictions': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'contact_primary_name': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'contact_primary_email': [tk.get_validator('ignore_missing'),
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
            'relevant_governing_documents': [tk.get_validator('ignore_missing'),
                        v.input_value_validator,
                        tk.get_converter('convert_to_extras')],
            'dig_id': [tk.get_validator('ignore_missing'),
                        v.dig_id_validator,
                        tk.get_converter('convert_to_extras')],
            

            'privacy_has_direct_identifiers': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'privacy_has_privacy_act_statement': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],

            'transfer_initial_size': [tk.get_validator('ignore_missing'),
                           v.positive_number_validator,
                           tk.get_converter('convert_to_extras')],
            'time_period_start_date': [tk.get_validator('ignore_missing'),
                                       tk.get_converter('convert_to_extras')],
            'pia_url': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'custom_link_label': [tk.get_validator('ignore_missing'),
                                  v.check_all,
                                  tk.get_converter('convert_to_extras')],
            'custom_link_link': [tk.get_validator('ignore_missing'),
                                 tk.get_converter('convert_to_extras')],
        })
        schema['resources'].update({
                'content_temporal_range_end' : [ 
                    tk.get_validator('ignore_missing'),],
                'content_temporal_range_start ' : [ 
                    tk.get_validator('ignore_missing'),],
                'format_cfpb' : [ 
                    tk.get_validator('ignore_missing'), v.input_value_validator,],
                'storage_location' : [ 
                    tk.get_validator('ignore_missing'),],
                'storage_location_path' : [   
                    tk.get_validator('ignore_missing'),],# this can be any unicode input
                'sensitivity_level' : [ 
                    tk.get_validator('ignore_missing'),],
                'usage_restrictions' : [ 
                    tk.get_validator('ignore_missing'),],
                'privacy_contains_pii' : [ 
                    tk.get_validator('ignore_missing'),],
        })
#        pprint.pprint(schema)
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
            'source_names': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'access_restrictions': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'contact_primary_email': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'contact_primary_name': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'initial_purpose_for_intake': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'legal_authority_for_collection': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'pra_omb_control_number': [tk.get_converter('convert_from_extras'),
                                tk.get_validator('ignore_missing')],

            'privacy_pia_title': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'privacy_sorn_number': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'relevant_governing_documents': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'dig_id': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            

            'privacy_has_direct_identifiers': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'privacy_has_privacy_act_statement': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],


            'transfer_initial_size': [tk.get_converter('convert_from_extras'),
                           tk.get_validator('ignore_missing')],
            'time_period_start_date': [tk.get_converter('convert_from_extras'),
                                       tk.get_validator('ignore_missing')],
            'pia_url': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'custom_link_label': [tk.get_converter('convert_from_extras'),
                                  tk.get_validator('ignore_missing')],
            'custom_link_link': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
        })
        schema['resources'].update({
                'content_temporal_range_end' : [ tk.get_validator('ignore_missing'),],
                'content_temporal_range_start ' : [ tk.get_validator('ignore_missing'),],
                'format_cfpb' : [ tk.get_validator('ignore_missing'),],
                'storage_location' : [ tk.get_validator('ignore_missing'),],
                'storage_location_path': [ tk.get_validator('ignore_missing'),],
                'sensitivity_level' : [ tk.get_validator('ignore_missing'),],
                'usage_restrictions' : [ tk.get_validator('ignore_missing'),],
                'privacy_contains_pii' : [ tk.get_validator('ignore_missing'),],
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

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')

        # Register this plugin's fanstatic directory with CKAN.
        # Here, 'fanstatic' is the path to the fanstatic directory
        # (relative to this plugin.py file), and 'example_theme' is the name
        # that we'll use to refer to this fanstatic directory from CKAN
        # templates.
        #tk.add_resource('fanstatic', 'example_theme')
