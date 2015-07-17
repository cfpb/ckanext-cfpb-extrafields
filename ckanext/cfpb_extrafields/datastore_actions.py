import ckan.plugins.toolkit as tk
import collections

# the datastore looks like this:
#  ... | title_colname | json_colname | ...
# --------------------------------------------
#  ... |    ...        |   ...        | ...
#  ... | json_title    | json_record  | ...
#  ... |    ...        |   ...        | ...

def default_datastore(rid):
    ''' provide default datastore parameter values and reduce duplication '''
    defaults_tuple = collections.namedtuple('defaults_tuple', 'json_colname context data')
    json_colname = 'jtable'
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {'resource_id': rid}
    return defaults_tuple(json_colname=json_colname, context=context, data=data)
def create_datastore_json(rid, json_record, title_colname, json_title): 
    ''' create a new datastore json element with primary key element of title_colname and record '''
    defaults = default_datastore(rid)
    json_colname = defaults.json_colname
    context = defaults.context
    data = defaults.data
    data.update({
    'force':'true',
     # If the table already exists with different fields this will fail! Datastore fields must be global!
    'fields': [{'id': title_colname},{'id': json_colname, 'type': 'json'}],
    'records': [ {title_colname: json_title, json_colname: json_record} ]
    })
    ds = tk.get_action('datastore_create')(context, data)
def get_all_datastore_jsons(rid, title_colname, json_title): 
    defaults = default_datastore(rid)
    json_colname = defaults.json_colname
    context = defaults.context
    data = defaults.data
    if json_title:
        data.update({'filters': {title_colname: json_title},})
    try:
        ds = tk.get_action('datastore_search')(context, data)
    except tk.ValidationError, err:
        # don't fail if the filter is bad! (e.g., title_colname doesn't exist)
        return 
    except tk.ObjectNotFound, err:
        return 
    else:
        recs = ds.get('records',[{}])
        json_list = [rec[json_colname] for rec in recs]
        return json_list
def get_unique_datastore_json(rid, title_colname, json_title):
    ''' For json_title, you're asserting that what you want is unique. '''
    jsons = get_all_datastore_jsons(rid, title_colname, json_title)
    if not jsons: 
        return
    elif len(jsons) > 1:
        raise IndexError 
    else:
        return jsons[0]

def delete_datastore_json(rid, title_colname, json_title):
    defaults = default_datastore(rid)
    context = defaults.context
    data = defaults.data
    data.update({'force':'true', 'filters': {title_colname: json_title},})
    ds = tk.get_action('datastore_delete')(context, data)
