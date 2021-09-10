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

__author__ = "Yi Ren <yire@cisco.com>"
__contributors__ = [
    "Josh Ingeniero <jingenie@cisco.com>",
    "Hemang Hitesh Shah <hhiteshs@cisco.com>"
]
__copyright__ = "Copyright (c) 2021 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

from flask import Flask, jsonify, Response, request, render_template, session, request, redirect, url_for
from webexteamssdk import WebexTeamsAPI
from DETAILS import *
import logging
import urllib3
import pprint
import json
import re
import test_creation
from generate_result import *
from enterprise_functions import *
from apscheduler.schedulers.background import BackgroundScheduler
from umbrella_connector import *
import requests

app = Flask(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
pp = pprint.PrettyPrinter(indent=2)
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
api = WebexTeamsAPI(access_token=BOT_TOKEN)
sender_store = BackgroundScheduler()
sender_store.start()


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'info': 'Hello from Lightsail!'})


@app.route('/', methods=['GET', 'POST'])
def webhook():
    payload = request.json
    if not payload['data']['personEmail'] == BOT_EMAIL:
        pp.pprint(payload)
        info = api.messages.get(payload['data']['id']).to_dict()
        pp.pprint(info)
        if re.search('help', info['text']):
            api.messages.create(toPersonId=payload['data']['personId'],
                                text='Let me help!',
                                attachments=[json.loads(CARD_PAYLOAD)])  # where to load the card

        elif re.search('top', info['text']):
            umbrella = Umbrella(UMBRELLA_REPORTING_KEY, UMBRELLA_REPORTING_SECRET, UMBRELLA_ORG_ID)
            print("`````````````````````````````````````````````````")
            print(UMBRELLA_REPORTING_KEY, UMBRELLA_REPORTING_SECRET, UMBRELLA_ORG_ID)
            dest_list = umbrella.get_top_destinations(limit=10)
            print(dest_list)
            card = generate_umbrella_card(dest_list)
            api.messages.create(toPersonId=payload['data']['personId'],
                                text='Let me help!',
                                attachments=[card])  # where to load the card
    return jsonify({'info': 'Hello from Kubernetes!'})


@app.route('/card', methods=['GET', 'POST'])
def card_webhook():
    payload = request.json
    pp.pprint(payload)
    info = api.attachment_actions.get(payload['data']['id']).to_dict()['inputs']
    if info['action'] == 'newTest':
        if info['hostnameVal'] != '':
            if info['IssueSelectVal'] != '' or info['CustomURLVal'] != '':
                api.messages.delete(messageId=payload['data']['messageId'])
                api.messages.create(toPersonId=payload['data']['personId'],
                                    text='We have gotten your issue. We will get back to you in 1 min')
                cardinfo = {'hostnameVal': info['hostnameVal'], 'IssueSelectVal': info['IssueSelectVal'],
                            'CustomURLVal': info['CustomURLVal']}
                pp.pprint(cardinfo)
                test_result = test_creation.find_endpoint_agent_id(cardinfo)
                print("================================================")
                print(test_result)
                print("================================================")  # test result returned nothing, fix later

                for result in test_result:
                    schedule_result(json.loads(result), payload['data']['personId'], sender_store, api)
                print("lol")

            else:
                api.messages.create(toPersonId=payload['data']['personId'],
                                    text='Please provide us your issue type')
        else:
            api.messages.create(toPersonId=payload['data']['personId'],
                                text='Please provide us your device hostname')
    elif info['action'] == 'destAction':
        print("doing ent agent here")
        print(info)

        test_result_ent = test_creation.custom_enterprise_test(ENT_AGENT, info['url'])
        print(test_result_ent)
        schedule_result(json.loads(test_result_ent), payload['data']['personId'], sender_store, api)
    elif info['action'] == 'priorityAction':
        print('increasing Meraki priority')
        add_meraki_traffic_shaping_rule(info['url'])
        api.messages.create(toPersonId=payload['data']['personId'],
                            text=f"{info['url']} is now high priority on Meraki MX!")
        print('add Meraki traffic shaping rules')
    return jsonify({'info': 'Hello from Kubernetes!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5060', debug=True)
