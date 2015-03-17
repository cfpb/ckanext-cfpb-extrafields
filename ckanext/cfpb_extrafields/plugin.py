import ckan.plugins as p
import ckan.plugins.toolkit as tk
import pprint
import re

PRA_CONTROL_NUM_REGEX = re.compile('^\d{4}-\d{4}$') 

class ExampleIDatasetFormPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)

    def pra_control_num_validator(self, value):
	if value and not PRA_CONTROL_NUM_REGEX.match(value):
	    raise tk.Invalid("Must be in the format XXXX-XXXX")
	return value

    def _modify_package_schema(self, schema):
        schema.update({
            'sensitivity_level': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'has_pii': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
            'type_of_entries': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')],
	    'pra_control_num': [tk.get_validator('ignore_missing'),
			self.pra_control_num_validator,
                        tk.get_converter('convert_to_extras')],
        })
	pprint.pprint(schema)
        return schema
    
    def create_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(ExampleIDatasetFormPlugin, self).create_package_schema()
        #our custom field
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).update_package_schema()
        #our custom field
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).show_package_schema()
        schema.update({
            'sensitivity_level': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'has_pii': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
            'type_of_entries': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')],
	    'pra_control_num': [tk.get_converter('convert_from_extras'),
			self.pra_control_num_validator,
                        tk.get_validator('ignore_missing')],
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
