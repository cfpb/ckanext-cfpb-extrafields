import ckan.plugins.toolkit as tk
import collections
 
def default_datastore(rid):
    ''' provide default datastore parameter values and reduce duplication '''
    defaults_tuple = collections.namedtuple('defaults_tuple', 'context data json_colname')
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {'resource_id': rid, 'force': 'true',}
    json_colname = 'jtable'
    return defaults_tuple(context=context, data=data, json_colname=json_colname)

def create_datastore_json(rid, json_record, title_colname, json_title): # title_colname='name' json_title='datadict'
    ''' create a new datastore json element with primary key element of title and record '''
    defaults = default_datastore(rid)
    context = defaults.context
    data = defaults.data
    json_colname = defaults.json_colname
    data.update({ 
    'primary_key': [title_colname],
    'fields': [{'id': title_colname},{'id': json_colname, 'type': 'json'}],
    'records': [ {title_colname: json_title, json_colname: json_record} ]
    })
    try:
        ds = tk.get_action('datastore_create')(context, data)
        return 'created datadict!'
    except tk.ValidationError, err:
        return err.error_dict['info']

def _find_json_in_datastore(ds, json_title, json_colname):
    recs = ds.get('records',[{}])
    js=[{}]
    for rec in recs:
        if rec.get('name','0')==json_title:
            print "datastore: rec.get(json_colname,'')",rec.get(json_colname,'')
            js = rec.get(json_colname,'')
    return js
def print_datastore_json(rid, title_colname, json_title):
    defaults = default_datastore(rid)
    context = defaults.context
    data = defaults.data
    json_colname = defaults.json_colname
    if json_title:
        data.update({'filters': {title_colname: json_title}, })
    del data['force']
    try:
        ds = tk.get_action('datastore_search')(context, data)
        json_record = _find_json_in_datastore(ds, json_title, json_colname)
        return 'datastore: found the json!<br>'+str(ds)+'=====record'+json_title+': '+str(json_record)
    except tk.ObjectNotFound, err:
        return str(err)
def get_datastore_json(rid, title_colname, json_title): #title_colname='name'; json_title='datadict'
    defaults = default_datastore(rid)
    context = defaults.context
    data = defaults.data
    json_colname = defaults.json_colname
    data.update({'filters': {title_colname: json_title},})
    del data['force']
    try:
        ds = tk.get_action('datastore_search')(context, data)
        return _find_json_in_datastore(ds, json_title, json_colname)
    except tk.ObjectNotFound, err:
        print str(err)
        return None 

def update_datastore_json(rid, title_colname, json_title, update_record): #='name' ='datadict' =[{'i':4444,'j':1111}]
    defaults = default_datastore(rid)
    context = defaults.context
    data = defaults.data
    data.update({
        'method':'update',
        'records': [ {title_colname: json_title, json_colname: update_record} ]
    })
    try:
        ds = tk.get_action('datastore_upsert')(context, data)
        return 'datastore: update table: '+json_title
    except tk.ObjectNotFound, err:
        return err.error_dict['info']

def delete_datastore_json(rid, title_colname, json_title):
    defaults = default_datastore(rid)
    context = defaults.context
    data = defaults.data
    data.update({'filters': {title_colname: json_title},})
    try:
        ds = tk.get_action('datastore_delete')(context, data)
        return 'datastore: deleted table: '+json_title
    except tk.ObjectNotFound, err:
        return str(err)
