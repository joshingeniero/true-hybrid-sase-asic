#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from __future__ import absolute_import, division, print_function

__author__ = "Josh Ingeniero <jingenie@cisco.com>"
__copyright__ = "Copyright (c) 2021 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


import json
import meraki
import re

from DETAILS import *


API_KEY = MERAKI_API_KEY
NETWORK_ID = MERAKI_NET_ID
ORG_ID = MERAKI_ORG_ID


dashboard = meraki.DashboardAPI(api_key=API_KEY, suppress_logging=True)

CARD_BASE = """{
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {}
    }"""

UMBRELLA_CARD = """{
    "type": "AdaptiveCard",
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.2",
    "body": [
        {
            "type": "TextBlock",
            "text": "Umbrella Top Destinations",
            "wrap": true,
            "size": "Medium",
            "weight": "Bolder"
        },
        {
            "type": "TextBlock",
            "text": "Your organisation's top 10 destinations. Click on a destination to generate an enterprise agent test and create a rule on Meraki MX.",
            "wrap": true
        }
    ]
}"""

DEST_ACTION = {
                "type": "ActionSet",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "google.com",
                        "data": {
                            "action": "destAction",
                            "url": "google.com"
                        }
                    }
                ]
            }


def add_meraki_traffic_shaping_rule(url):
    '''
    Adds the url to the high priority rule for Meraki MX Traffic Shaping rules
    :argument url - domain to add

    :returns result or None - depends on the status message

    RULESCHEMA
    {
    "defaultRulesEnabled": true,
    "rules": [
        {
            "definitions": [
                {
                    "type": "host",
                    "value": "apple.com"
                }
            ],
            "perClientBandwidthLimits": {
                "settings": "network default"
            },
            "dscpTagValue": null,
            "priority": "high"
        }
    ]
}
    '''
    url2 = re.compile(r"https?://(www.)?")
    url = url2.sub('', url).strip().strip('/')
    current_rules = dashboard.appliance.getNetworkApplianceTrafficShapingRules(NETWORK_ID)
    if current_rules['rules']:  # Current rules exist
        definition = {
                    "type": "host",
                    "value": url
                }
        rule = current_rules['rules'][0]
        rule['definitions'].append(definition)
        defaultRules = current_rules['defaultRulesEnabled']
        result = dashboard.appliance.updateNetworkApplianceTrafficShapingRules(NETWORK_ID,
                                                                               defaultRulesEnabled=defaultRules,
                                                                               rules=[rule])
    else:  # Empty ruleset
        rule = {
            "definitions": [
                {
                    "type": "host",
                    "value": url
                }
            ],
            "perClientBandwidthLimits": {
                "settings": "network default"
            },
            "dscpTagValue": None,
            "priority": "high"
        }
        result = dashboard.appliance.updateNetworkApplianceTrafficShapingRules(NETWORK_ID, defaultRulesEnabled=True,
                                                                               rules=[rule])
    return result


def generate_umbrella_card(destinations_list):
    '''
    Returns a JSON-formatted card for Webex Cards from Umbrella top Destinations
    :argument destinations_list - Umbrella destination list result

    :returns card formatted for Webex
    '''
    destinations = [item['domain'] for item in destinations_list]
    umbrella_card = json.loads(UMBRELLA_CARD)
    base_card = json.loads(CARD_BASE)
    for destination in destinations:
        temp_action = {
            "type": "ActionSet",
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "google.com",
                    "data": {
                        "action": "destAction",
                        "url": "google.com"
                    }
                }
            ]
        }
        temp_action['actions'][0]['title'] = destination
        temp_action['actions'][0]['data']['url'] = destination
        umbrella_card['body'].append(temp_action)
    base_card['content'] = umbrella_card
    return base_card
