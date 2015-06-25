import ckan.plugins.toolkit as tk

#snl code review: too much duplication. A decorator would fix a lot of this
# should use duck-typing and not rely on datadict/generic functions.
# will delete these comments before pull request as they are addressed.

def create_datadict(rid, pkey=''):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {
    "force": "true",
    "resource_id": rid,
    "primary_key": ["name"],
    "fields": [{"id": "name"},{"id": "jtable", "type": "json"}],
    "records": [ {"name": "datadict", "jtable": [{"i":1,"j":"xyz"}]} ]
    }
    try:
        ds = tk.get_action('datastore_create')(context, data)
        return 'created!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    except tk.ValidationError, err:
        return err.error_dict['info']
    return 'fell through create_datadict****************'
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
        return 'created generic!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    except tk.ValidationError, err:
        return err.error_dict['info']
    return 'fell through create_generic_json****************'

def get_datadict(rid):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {"resource_id" : rid,}
    try:
        ds = tk.get_action('datastore_search')(context, data)
        return 'found!!!!!!!!!!!!!'+str(ds)
    except tk.ObjectNotFound, err:
#        return err.error_dict['info']
        return str(err) 
    return 'fell through get_datadict****************'
def get_datastore(rid):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {"resource_id" : rid,}
    try:
        ds = tk.get_action('datastore_search')(context, data)
        return 'found!!!!!!!!!!!!!'+str(ds)
    except tk.ObjectNotFound, err:
#        return err.error_dict['info']
        return str(err) 

def	update_datadict(rid):
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
        return 'update datadict specifically!!!!!!!!!!!!!!!!!'
    except tk.ObjectNotFound:
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
        return 'deleted datadict specifically!!!!!!!!!!!!!!!!!'
    except tk.ObjectNotFound:
        return err.error_dict['info']
def delete_datastore(rid):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    data = {"resource_id" : rid,"force": "true",}
    try:
        ds = tk.get_action('datastore_delete')(context, data)
        return 'deleted!!!!!!!!!!!!!!!!!'
    except tk.ObjectNotFound:
        return err.error_dict['info']