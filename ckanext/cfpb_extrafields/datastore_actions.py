import ckan.plugins.toolkit as tk

#snl code review: too much duplication. A decorator would fix a lot of this
# should use duck-typing and not rely on datadict/generic functions.
# will delete these comments before pull request as they are addressed.

def create_datadict(rid, record=[{"i":1,"j":"xyz"}],pkey=''):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {
    "force": "true",
    "resource_id": rid,
    "primary_key": ["name"],
    "fields": [{"id": "name"},{"id": "jtable", "type": "json"}],
    "records": [ {"name": "datadict", "jtable": record} ]
    }
    try:
        ds = tk.get_action('datastore_create')(context, data)
        return 'created datadict!'
    except tk.ValidationError, err:
        return err.error_dict['info']
def create_generic_json(rid, pkey='name',new_table='other' ):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {
    "force": "true",
    "resource_id": rid,
    "primary_key": [pkey],
    "fields": [{"id": pkey},{"id": "jtable", "type": "json"}],
    "records": [ {pkey: new_table, "jtable": [{"i":1111,"j":"zyx"}]} ]
    }
    try:
        ds = tk.get_action('datastore_create')(context, data)
        return 'created generic datastore!'
    except tk.ValidationError, err:
        return err.error_dict['info']

def _find_json_in_ds(ds,name='datadict'):
    recs = ds.get('records',[{}])
    datadict=[{}]
    for rec in recs:
        if rec.get('name','0')==name:
            print "rec.get('jtable','')",rec.get('jtable','')
            datadict = rec.get('jtable','')
    return datadict
def get_datadict(rid):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {"resource_id" : rid,     
    "filters": {"name":"datadict"}
    }
    try:
        ds = tk.get_action('datastore_search')(context, data)
        _table = _find_json_in_ds(ds,name="datadict")
        return 'found the datadict!<br>'+str(ds)+'=====record: '+str(_table)
    except tk.ObjectNotFound, err:
        return str(err)
def get_datastore(rid):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {"resource_id" : rid,}
    try:
        ds = tk.get_action('datastore_search')(context, data)
        _table=_find_json_in_ds(ds,name="other")
        return 'found a datastore!'+str(ds)+'=====record other: '+str(_table)
    except tk.ObjectNotFound, err:
        return str(err) 

def get_datadict_json(rid):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {"resource_id" : rid,     
    "filters": {"name":"datadict"}
    }
    try:
        ds = tk.get_action('datastore_search')(context, data)
        return _find_json_in_ds(ds,name="datadict")
    except tk.ObjectNotFound, err:
        print str(err)
        return None 

def update_datadict(rid):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {
    "force": "true",
    "resource_id": rid,
    "method":"update",
    "records": [ {"name": "other", "jtable": [{"i":4444,"j":1111}] } ]
    }
    try:
        ds = tk.get_action('datastore_upsert')(context, data)
        return 'update datadict specifically!'
    except tk.ObjectNotFound, err:
        return err.error_dict['info']

def delete_datadict(rid):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {
    "resource_id": rid,
    "force": "true", 
    "filters": {"name":"datadict"}
    }
    try:
        ds = tk.get_action('datastore_delete')(context, data)
        return 'deleted datadict!'
    except tk.ObjectNotFound, err:
        return str(err)
def delete_datastore(rid):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {"resource_id" : rid,"force": "true",}
    try:
        ds = tk.get_action('datastore_delete')(context, data)
        return 'deleted datastore'
    except tk.ObjectNotFound, err:
        return str(err)
