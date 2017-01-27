"""Update CKAN Resources

usage: CKAN_API_KEY=<ckan_api_key> CKAN_URL=<ckan_url> [CKAN_DATE_FIELD=<date_field>] python update_resource.py <resource_id> [<timestamp>]

    CKAN_API_KEY: the API key on the bottom left of your ckan user settings page
    CKAN_URL: url to the data catalog, i.e. http://catalog.data.cfpb.local
    CKAN_DATE_FIELD: the field on the resource metadata to update. defaults to update_date
    resource_id: the unique ID of a ckan resource
    timestamp: ISO timestamp to use as the new update time. Defaults to now.
"""
from __future__ import print_function
import datetime as dt
import json
import os
import sys

import requests

import logging
logging.basicConfig(level=logging.DEBUG)

API_KEY = os.environ["CKAN_API_KEY"]
CKAN_URL = os.environ["CKAN_URL"]
DATE_FIELD = os.environ.get("CKAN_DATE_FIELD", "update_date")

def do_action(action, data, ckan_url=CKAN_URL, api_key=API_KEY):
    response = requests.post(
        ckan_url + "/api/3/action/" + action,
        json=data,
        headers={"Authorization": api_key},
    )
    response.raise_for_status()
    return response

def get_resource(resource_id, ckan_url=CKAN_URL, api_key=API_KEY):
    response = do_action("resource_show", {"id": resource_id}, ckan_url, api_key)
    return response.json()["result"]

def update_resource(resource, ckan_url=CKAN_URL, api_key=API_KEY):
    do_action("resource_update", resource, ckan_url, api_key)

def main(args):
    if len(args) < 2 or args[1] in ["help", "-h", "--help"]:
        print(__doc__)
    else:
        resource_id = args[1]

        if len(args) > 2:
            timestamp = args[2]
        else:
            timestamp = dt.datetime.now().isoformat()

        resource = get_resource(resource_id)
        resource[DATE_FIELD] = timestamp
        update_resource(resource)


if __name__ == "__main__":
    main(sys.argv)

