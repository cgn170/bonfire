#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission

This plugin process documentation files in confluence format, upload all information into a confluence workspace
configuration

"""

import requests
import json
import datetime
from lib import SetupLogger

# Plugin information, useful to know what it does
plugin_description = "Plugin to upload confluence documentation, check documentation folder and passwords.yml " \
                     "examples file for more information"


# Get plugin description
def get_plugin_description():
    return plugin_description


# Query previous version of the page
def get_page_json(base_url, username, password, page_id, expand=False):

    if expand:
        suffix = "?expand=" + str(expand)
    else:
        suffix = ""

    url = base_url + "/wiki/rest/api/content/" + page_id + suffix
    try:
        response = requests.get(url, auth=(username, password))
    except Exception as e:
        SetupLogger.logger.error("Error querying confluence page: {}".format(e))
        return None

    response.encoding = "utf8"
    if response.status_code == 200:
        SetupLogger.logger.info("Query json page successfully")
        return json.loads(response.text)
    else:
        SetupLogger.logger.info("Error querying confluence page, Responde Code: {0}"
                                .format(response.status_code))
        return None


# Update title and content to the page
def set_page_json(base_url, username, password, page_id, json_content):
    headers = {
        'Content-Type': 'application/json',
    }
    try:
        response = requests.put(base_url + "/wiki/rest/api/content/" + page_id,
                                headers=headers,
                                data=json.dumps(json_content),
                                auth=(username, password))
    except Exception as e:
        SetupLogger.logger.error("Update page failed, Error: {}".format(e))
        return False

    if response.status_code == 200:
        SetupLogger.logger.info('Page updated successfully!')
        return True
    else:
        SetupLogger.logger.error("Update page failed: Code: {0}".format(response.status_code))
        return False


# Update a confluence page
def update_confluence_page(base_url, username, password, page_id, page_title, page_content):

    SetupLogger.logger.info('Starting update confluence page function')

    # Query previous version of the page
    previous_page_json_data = get_page_json(base_url, username, password, page_id)

    if previous_page_json_data:
        json_data = dict()
        json_data['id'] = previous_page_json_data['id']
        json_data['type'] = previous_page_json_data['type']
        # Update old title with new one
        json_data['title'] = page_title
        json_data['version'] = {"number": previous_page_json_data['version']['number'] + 1}
        if 'key' not in previous_page_json_data:
            json_data['key'] = previous_page_json_data['space']['key']
        else:
            json_data['key'] = previous_page_json_data['key']

        # Add update time
        content_date = "This page was automatically updated via Confluence Updater Script on {} UTC"\
            .format(datetime.datetime.utcnow())

        content_page = content_date + "\n" + page_content
        json_data['body'] = {'storage': {'value': content_page, 'representation': 'wiki'}}

        # Update page
        if not set_page_json(base_url, username, password, page_id, json_data):
            SetupLogger.logger.fatal('Update page failed')

    else:
        SetupLogger.logger.error("Can't load previous version of the page")

    SetupLogger.logger.info('Finished update confluence page function')

# Create a confluence page


# Create workspace plugin
def create_confluence_page(base_url, username, password, page_title, page_content):
    pass


# Deploy function, deploy all documentation template
def deploy(dry_run, plugin_configuration_variables, passwords):
    print("[plugin: Confluence] Doing something: {}".format(plugin_configuration_variables))


# Remove function, remove stacks deployed
def remove(dry_run, plugin_configuration_variables, passwords):
    print("[plugin: Confluence] Doing something")
