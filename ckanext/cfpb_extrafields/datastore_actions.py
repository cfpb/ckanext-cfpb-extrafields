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
    # WARNING: when create table is called, it must know all of the colnames and their order.
    # Changing the field names WILL BREAK front end access to resources with the old names
    # (adding new fields will not cause this problem).
    title_colname = 'record_title' #title crosses wires with something in CKAN
    subtitle_colname = 'record_subtitle'
    datetime_colname = 'datetime'
    response_colname = 'response'
    response_timems_colname = 'response_timems'
    json_colname = 'json_record'
    all_fields =[{'id':title_colname,'type':'text'},
                 {'id':subtitle_colname,'type':'text'},
                 {'id':datetime_colname,'type':'timestamp'},
                 {'id':response_colname,'type':'bool'},
                 {'id':response_timems_colname,'type':'int'},
                 {'id':json_colname,'type':'json'},]
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {'resource_id': rid}
    defaults_tuple = collections.namedtuple('defaults_tuple', 'context data \
    title_colname subtitle_colname json_colname datetime_colname response_colname \
    response_timems_colname all_fields')
    return defaults_tuple(context, data,
                          title_colname, subtitle_colname, json_colname,
                          datetime_colname, response_colname,
                          response_timems_colname, all_fields)


# JSON related (for datadict):
def create_datastore(rid, json_title=None, json_record=None):
    ''' create a new datastore json element with title_colname and record '''
    defaults = default_datastore(rid)
    data = defaults.data
    records = []
    if json_title :
        records.append({defaults.title_colname: json_title, defaults.json_colname: json_record})
    data.update({
        'force':'true',
        'fields': defaults.all_fields,
        'records': records,
    })
    ds = tk.get_action('datastore_create')(defaults.context, data)


def get_all_datastore_jsons(rid, json_title):
    defaults = default_datastore(rid)
    data = defaults.data
    if json_title:
        data.update({'filters': {defaults.title_colname: json_title},})
    try:
        ds = tk.get_action('datastore_search')(defaults.context, data)
    except tk.ValidationError, err:
        # don't fail if the filter is bad! (e.g., defaults.title_colname doesn't exist)
        return
    except tk.ObjectNotFound, err:
        return
    else:
        recs = ds.get('records',[{}])
        json_list = [rec[defaults.json_colname] for rec in recs]
        return json_list


def get_unique_datastore_json(rid, json_title):
    ''' For json_title, you're asserting that what you want is unique. '''
    jsons = get_all_datastore_jsons(rid, json_title)
    if not jsons:
        return
    elif len(jsons) > 1:
        raise IndexError
    else:
        return jsons[0]


def delete_datastore_json(rid, json_title):
    defaults = default_datastore(rid)
    data = defaults.data
    data.update({
        'force':'true',
        'filters': {defaults.title_colname: json_title},
    })
    ds = tk.get_action('datastore_delete')(defaults.context, data)
