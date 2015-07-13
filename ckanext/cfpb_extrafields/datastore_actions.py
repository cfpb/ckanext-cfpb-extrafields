import ckan.plugins.toolkit as tk
import collections
 
def default_datastore(rid):
    ''' provide default datastore parameter values and reduce duplication '''
    defaults_tuple = collections.namedtuple('context', 'data', 'json_label')
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {'resource_id': rid, 'force': 'true',}
    json_label = 'jtable'
    return defaults_tuple(context=context, data=data, json_label=json_label)

def create_datatstore_json(rid, record=[{'i':1,'j':'xyz'}], pkey='name', new_table='datadict'):
    defaults = default_datastore(rid)
    context = defaults.context
    data = defaults.data
    json_label = defaults.json_label
    data.update({ 
    'primary_key': [pkey],
    'fields': [{'id': pkey},{'id': json_label, 'type': 'json'}],
    'records': [ {pkey: new_table, json_label: record} ]
    })
    try:
        ds = tk.get_action('datastore_create')(context, data)
        return 'created datadict!'
    except tk.ValidationError, err:
        return err.error_dict['info']

def _find_json_in_datastore(ds,name='datadict', json_label):
    recs = ds.get('records',[{}])
    datadict=[{}]
    for rec in recs:
        if rec.get('name','0')==name:
            print "datastore: rec.get(json_label,'')",rec.get(json_label,'')
            datadict = rec.get(json_label,'')
    return datadict
def print_datastore_table(rid, filter_key='name', filter_table='datadict'):
    defaults = default_datastore(rid)
    context = defaults.context
    data = defaults.data
    json_label = defaults.json_label
    data.update({'filters': {filter_key, filter_table}})
    try:
        ds = tk.get_action('datastore_search')(context, data)
        _table = _find_json_in_datastore(ds, name=filter_table, json_label)
        return 'datastore: found the datadict!<br>'+str(ds)+'=====record'+filter_table+': '+str(_table)
    except tk.ObjectNotFound, err:
        return str(err)
def get_datastore_table(rid, filter_key='name', filter_table='datadict'):
    defaults = default_datastore(rid)
    context = defaults.context
    data = defaults.data
    json_label = defaults.json_label
    data.update({
    'filters': {filter_key: filter_table}
    })
    try:
        ds = tk.get_action('datastore_search')(context, data)
        return _find_json_in_datastore(ds,name=filter_table, json_label)
    except tk.ObjectNotFound, err:
        print str(err)
        return None 

def update_datastore_table(rid, filter_key='name', filter_table='datadict', uprec=[{'i':4444,'j':1111}]):
    defaults = default_datastore(rid)
    context = defaults.context
    data = defaults.data
    data.update({
        'method':'update',
        'records': [ {filter_key: filter_table, json_label: uprec} ]
    })
    try:
        ds = tk.get_action('datastore_upsert')(context, data)
        return 'datastore: update table: '+filter_table
    except tk.ObjectNotFound, err:
        return err.error_dict['info']

def delete_datastore_table(rid, filter_key='name', filter_table='datadict'):
    defaults = default_datastore(rid)
    context = defaults.context
    data = defaults.data
    data.update({
        'filters': {filter_key, filter_table},
    })
    try:
        ds = tk.get_action('datastore_delete')(context, data)
        return 'datastore: deleted table: '+filter_table
    except tk.ObjectNotFound, err:
        return str(err)
