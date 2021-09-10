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
import requests
import datetime
from DETAILS import *


CARD_BASE = """{
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {}
    }"""

RESULT_CARD = """{
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.2",
    "body": [
        {
            "type": "TextBlock",
            "text": "ThousandEyes Test Result",
            "weight": "Bolder",
            "size": "Medium"
        },
        {
            "type": "TextBlock",
            "text": "www.google.com",
            "weight": "Bolder",
            "wrap": true
        },
        {
            "type": "TextBlock",
            "spacing": "None",
            "text": "Created {{DATE(2020-02-14T06:08:39Z, SHORT)}}",
            "isSubtle": true,
            "wrap": true
        },
        {
            "type": "TextBlock",
            "text": "Everything seems normal!",
            "wrap": true
        },
        {
            "type": "FactSet",
            "facts": [
                {
                    "title": "Response:",
                    "value": "200 Okay"
                },
                {
                    "title": "Total Response Time:",
                    "value": "252ms"
                },
                {
                    "title": "Loss:",
                    "value": "1%"
                },
                {
                    "title": "Average Latency:",
                    "value": "251ms"
                },
                {
                    "title": "Jitter:",
                    "value": "10ms"
                }
                ,
                {
                    "title": "Average CPU Usage:",
                    "value": "10ms"
                }
            ]
        }
    ]
}"""


def call_url(url):
    '''
    Returns the data from the url
    :argument url - ThousandEyes apiLink
    '''
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': Authorization
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response


def generate_result(result):
    '''
    Returns a JSON-formatted card for Webex Cards from ThousandEyes Test results
    :argument result - ThousandEyes response for creating tests

    :return card - formatted for Webex or None if apiLinks do not exist
    '''
    if 'endpointTest' in result.keys():
        web = 'endpointWeb'
        test = 'endpointTest'
        net = 'endpointNet'

        if 'metrics' not in result[test][0]['apiLinks'][1]['href']:  # both exist = http-server test
            http_link = result[test][0]['apiLinks'][1]['href']
            metrics_link = result[test][0]['apiLinks'][2]['href']
            http = call_url(http_link).json()
            metrics = call_url(metrics_link).json()
            code = http[web]['httpServer'][0]['responseCode']
            if code == 200:
                status = 'Everything seems normal!'
                total = http[web]['httpServer'][0]['totalTime']
                cpu = http[web]['httpServer'][0]['systemMetrics']['cpuUtilization']['mean'] * 100
                cpu = round(cpu, 2)
                date = http[web][test]['createdDate']
            else:
                status = "Something's wrong!"
                total = 'N/A'
                cpu = http[web]['httpServer'][0]['systemMetrics']['cpuUtilization']['mean'] * 100
                cpu = round(cpu, 2)
                date = 'N/A'
            url = http[web][test]['server']
        else:  # only metrics = agent-server
            metrics_link = result[test][0]['apiLinks'][1]['href']
            metrics = call_url(metrics_link).json()
            date = metrics[net][test]['createdDate']
            cpu = metrics[net]['metrics'][0]['systemMetrics']['cpuUtilization']['mean'] * 100
            cpu = round(cpu, 2)
            url = metrics[net][test]['server']
            status = 'Agent-to-server'
            code = 'N/A'
            total = 'N/A'
    else:
        web = 'web'
        test = 'test'
        net = 'net'

        if 'metrics' not in result[test][0]['apiLinks'][1]['href']:  # both exist = http-server test
            http_link = result[test][0]['apiLinks'][1]['href']
            metrics_link = result[test][0]['apiLinks'][2]['href']
            http = call_url(http_link).json()
            metrics = call_url(metrics_link).json()
            code = http[web]['httpServer'][0]['responseCode']
            if code == 200:
                status = 'Everything seems normal!'
                total = http[web]['httpServer'][0]['totalTime']
                cpu = 'N/A'
                date = http[web][test]['createdDate']
            else:
                status = "Something's wrong!"
                total = 'N/A'
                cpu = 'N/A'
                date = http[web][test]['createdDate']
            url = http[web][test]['url']
        else:  # only metrics = agent-server
            metrics_link = result[test][0]['apiLinks'][1]['href']
            metrics = call_url(metrics_link).json()
            date = metrics[net][test]['createdDate']
            cpu = 'N/A'
            url = metrics[net][test]['server']
            status = 'Agent-to-server'
            code = 'N/A'
            total = 'N/A'
    if 'apiLinks' in result[test][0].keys():

        result_card = json.loads(RESULT_CARD)
        if 'loss' in metrics[net]['metrics'][0].keys():
            loss = metrics[net]['metrics'][0]['loss']
            if 'jitter' in metrics[net]['metrics'][0].keys():
                latency = metrics[net]['metrics'][0]['avgLatency']
                jitter = metrics[net]['metrics'][0]['jitter']
            else:
                latency = 'N/A'
                jitter = 'N/A'
        else:
            loss = 'N/A'
            latency = 'N/A'
            jitter = 'N/A'

        result_card['body'][1]['text'] = url  # url
        result_card['body'][2]['text'] = f"Created {date}"  # Date message
        result_card['body'][3]['text'] = status  # Status message
        result_card['body'][4]['facts'][0]['value'] = str(code)  # Response Code
        result_card['body'][4]['facts'][1]['value'] = f"{total} ms"  # Total Response Time
        result_card['body'][4]['facts'][2]['value'] = f"{loss} %"  # Loss
        result_card['body'][4]['facts'][3]['value'] = f"{latency} ms"  # Average Latency
        result_card['body'][4]['facts'][4]['value'] = f"{jitter} ms"  # Jitter
        result_card['body'][4]['facts'][5]['value'] = f"{cpu} %"  # CPU
        if 'endpointTest' not in result.keys():
            add_meraki = {
                "type": "ActionSet",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Set High Priority in Meraki MX",
                        "data": {
                            "action": "priorityAction",
                            "url": url
                        }
                    }
                ]
            }
            result_card['body'].append(add_meraki)
        return result_card

    else:
        return None


def send_result(result, sender, api_object):
    '''
    Scheduled job to send result cards at a specific time

    :argument result - ThousandEyes response for creating tests
    :argument sender - personId from Webex
    :argument api_object - webexteamssdk api instance
    '''
    card = generate_result(result)
    card_base = json.loads(CARD_BASE)
    card_base['content'] = card
    api_object.messages.create(toPersonId=sender,
                               text='Please enter your Webex Personal Meeting Room Link',
                               attachments=[card_base])


def schedule_result(result, sender, job_store, api_object):
    '''
    Scheduled job to schedule result cards at a specific time

    :argument result - ThousandEyes response for creating tests
    :argument sender - personId from Webex
    :argument job_store - apscheduler scheduler instance
    :argument api_object - webexteamssdk api instance
    '''
    now = datetime.datetime.now()
    if 'endpointTest' in result.keys():
        interval = int(result['endpointTest'][0]['interval']) + 10
    else:
        interval = 70
    delta = datetime.timedelta(0, interval)
    when = now + delta
    job_store.add_job(send_result, trigger='date', run_date=when, args=[result, sender, api_object])
