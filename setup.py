from setuptools import setup, find_packages

version = '1.2.0'

setup(
    name='ckanext-cfpb-extrafields',
    version=version,
    description="A CKAN plugin with various customizations for the CFPB Data Catalog",
    long_description='''This plugin customizes various aspects of CKAN:
    * Added fields for datasets/resources
    * Modified templates
    * CSV export
    * CSV import
    * Single Sign-on
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Daniel Davis',
    author_email='daniel.davis@cfpb.gov',
    url='github.com/cfpb/ckanext-cfpb-extrafields',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.cfpb_extrafields'],
    include_package_data=True,
    zip_safe=False,
    entry_points='''
        [ckan.plugins]
        ckanext_cfpb_extrafields=ckanext.cfpb_extrafields.plugin:ExampleIDatasetFormPlugin
        ckanext_cfpb_sso=ckanext.cfpb_extrafields.plugin:SSOPlugin
        ckanext_cfpb_export=ckanext.cfpb_extrafields.plugin:ExportPlugin
        ckanext_cfpb_import=ckanext.cfpb_extrafields.plugin:DigImportPlugin
        ckanext_cfpb_ldap_query=ckanext.cfpb_extrafields.plugin:LdapQueryPlugin
        ckanext_cfpb_access=ckanext.cfpb_extrafields.plugin:AccessPlugin
    ''',
)
