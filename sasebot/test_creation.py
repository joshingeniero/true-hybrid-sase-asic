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

__author__ = "Hemang Hitesh Shah <hhiteshs@cisco.com>"
__copyright__ = "Copyright (c) 2021 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import requests
import json

from DETAILS import *

""""     Test URLs       """

WebExProductivityToolsURL = "https://cisco.webex.com/WBXService/XMLService"
PrimaryCBServerURL = "https://ed1sgcb191.webex.com"
SecondaryCBServerURL = "https://epycb16302.webex.com"
WebExPrimaryAudioURL = "msg2mcs136.webex.com"
WebExSecondaryAudioURL = "gmjp2mcs192.webex.com"
WebExPrimaryVideoURL = "msg2mcs136.webex.com"
WebExSecondaryVideoURL = "gmjp2mcs192.webex.com"
SalesforceURL = "https://ciscosales.my.salesforce.com/"
O365URL = "https://login.microsoftonline.com"


def custom_enterprise_test(agent_id, custom_url):
    url = "https://api.thousandeyes.com/v6/instant/http-server.json"

    payload = json.dumps({
      "agents": [
          {
              "agentId": agent_id
          }
      ],
      "testName": "Custom URL Enterprise Instant Test",
      "url": custom_url
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': Authorization
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text


def find_endpoint_agent_id(webex_card_data):
    computer_name = webex_card_data["hostnameVal"]

    url = "https://api.thousandeyes.com/v6/endpoint-agents.json?computerName=" + computer_name
    print(url)
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': Authorization
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    response_json = json.loads(response.text)
    agentId = (response_json["endpointAgents"][0]["agentId"])
    print(agentId)
    result_array = create_endpoint_agent_label(webex_card_data, agentId)
    print("findendpointagentid")
    print(result_array)
    return result_array


def create_endpoint_agent_label(webex_card_data, endpoint_agent_id):
    url = "https://api.thousandeyes.com/v6/groups/endpoint-agents/new.json"
    endpoint_agents_array = [{"agentId": endpoint_agent_id}]
    print('1111111111111111')
    print(endpoint_agents_array)
    print('1111111111111111')
    payload = json.dumps({
        "name": "MY NEW5 Label",
        "endpointAgents": endpoint_agents_array
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': Authorization
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print('222222222222222222')
    print(response.text)
    print('222222222222222222')
    response_json = json.loads(response.text)
    groupId = (response_json["groups"][0]["groupId"])
    print(groupId)
    resultArray = test_selector(groupId, webex_card_data)
    print("create label ")
    print(resultArray)
    return resultArray


def test_selector(group_id, webex_card_data):
    issueArray = webex_card_data["IssueSelectVal"].split(",")
    print(issueArray)
    resultArray = []
    for issue in issueArray:
        print(issue)
        if issue == "WebexAudio":
            resultArray.append(webex_primary_audio(group_id))
            resultArray.append(webex_secondary_audio(group_id))
            resultArray.append(webex_primary_cb_server(group_id))
            resultArray.append(webex_secondary_cb_server(group_id))
        elif issue == "WebexVideo":
            resultArray.append(webex_primary_video(group_id))
            resultArray.append(webex_secondary_video(group_id))
            resultArray.append(webex_primary_cb_server(group_id))
            resultArray.append(webex_secondary_cb_server(group_id))
        elif issue == "salesforce":
            resultArray.append(salesforce(group_id))
        elif issue == "Noneofabove":
            CustomURL = webex_card_data["CustomURLVal"]
            resultArray.append(custom_endpoint_test(group_id, CustomURL))
        elif issue == "Webexproductivitytools":
            resultArray.append(webex_productivity_tools(group_id))
        elif issue == "Office365":
            resultArray.append(o365_test(group_id))
    delete_label(group_id)
    print("test selector")
    print(resultArray)
    return resultArray


def webex_productivity_tools(group_id):
    url = "https://api.thousandeyes.com/v6/endpoint-instant/http-server.json"
    payload = json.dumps({
        "authType": "NONE",
        "flagPing": True,
        "flagTraceroute": True,
        "groupId": group_id,
        "httpTimeLimit": 5000,
        "maxMachines": 5,
        "sslVersion": 0,
        "targetResponseTime": 5000,
        "testName": "WebEx Productivity Tools Instant HTTP test",
        "url": WebExProductivityToolsURL,
        "verifyCertHostname": True
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': Authorization,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def webex_primary_cb_server(group_id):
    url = "https://api.thousandeyes.com/v6/endpoint-instant/http-server.json"
    payload = json.dumps({
        "authType": "NONE",
        "flagPing": True,
        "flagTraceroute": True,
        "groupId": group_id,
        "httpTimeLimit": 5000,
        "maxMachines": 5,
        "sslVersion": 0,
        "targetResponseTime": 1000,
        "testName": "WebEx Primary CB Server Instant HTTP test",
        "url": PrimaryCBServerURL,
        "verifyCertHostname": True
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': Authorization,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def webex_secondary_cb_server(group_id):
    url = "https://api.thousandeyes.com/v6/endpoint-instant/http-server.json"
    payload = json.dumps({
        "authType": "NONE",
        "flagPing": True,
        "flagTraceroute": True,
        "groupId": group_id,
        "httpTimeLimit": 5000,
        "maxMachines": 5,
        "sslVersion": 0,
        "targetResponseTime": 1000,
        "testName": "WebEx Secondary CB Server Instant HTTP test",
        "url": SecondaryCBServerURL,
        "verifyCertHostname": True
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': Authorization,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def webex_primary_audio(group_id):
    url = "https://api.thousandeyes.com/v6/endpoint-instant/agent-to-server.json"
    payload = json.dumps({
        "flagPing": True,
        "flagTraceroute": True,
        "groupId": group_id,
        "maxMachines": 5,
        "testName": "Webex Primary Audio Test",
        "serverName": WebExPrimaryAudioURL,
        "port": 5004
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': Authorization,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def webex_secondary_audio(group_id):
    url = "https://api.thousandeyes.com/v6/endpoint-instant/agent-to-server.json"
    payload = json.dumps({
        "flagPing": True,
        "flagTraceroute": True,
        "groupId": group_id,
        "maxMachines": 5,
        "testName": "Webex Secondary Audio Test",
        "serverName": WebExSecondaryAudioURL,
        "port": 5004
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': Authorization,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def webex_primary_video(group_id):
    url = "https://api.thousandeyes.com/v6/endpoint-instant/agent-to-server.json"
    payload = json.dumps({
        "flagPing": True,
        "flagTraceroute": True,
        "groupId": group_id,
        "maxMachines": 5,
        "testName": "Webex Primary Video Test",
        "serverName": WebExPrimaryVideoURL,
        "port": 5004
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': Authorization,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def webex_secondary_video(group_id):
    url = "https://api.thousandeyes.com/v6/endpoint-instant/agent-to-server.json"
    payload = json.dumps({
        "flagPing": True,
        "flagTraceroute": True,
        "groupId": group_id,
        "maxMachines": 5,
        "testName": "Webex Secondary Video Test",
        "serverName": WebExSecondaryVideoURL,
        "port": 5004
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': Authorization,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def salesforce(group_id):
    url = "https://api.thousandeyes.com/v6/endpoint-instant/http-server.json"
    payload = json.dumps({
        "authType": "NONE",
        "flagPing": True,
        "flagTraceroute": True,
        "groupId": group_id,
        "httpTimeLimit": 5000,
        "maxMachines": 5,
        "sslVersion": 0,
        "targetResponseTime": 5000,
        "testName": "Salesforce Instant HTTP test",
        "url": SalesforceURL,
        "verifyCertHostname": True
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': Authorization,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def custom_endpoint_test(group_id, custom_url):
    url = "https://api.thousandeyes.com/v6/endpoint-instant/http-server.json"
    payload = json.dumps({
        "authType": "NONE",
        "flagPing": True,
        "flagTraceroute": True,
        "groupId": group_id,
        "httpTimeLimit": 5000,
        "maxMachines": 5,
        "sslVersion": 0,
        "targetResponseTime": 5000,
        "testName": "Custom URL Instant HTTP test",
        "url": custom_url,
        "verifyCertHostname": True
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': Authorization,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def o365_test(group_id):
    url = "https://api.thousandeyes.com/v6/endpoint-instant/http-server.json"
    payload = json.dumps({
        "authType": "NONE",
        "flagPing": True,
        "flagTraceroute": True,
        "groupId": group_id,
        "httpTimeLimit": 5000,
        "maxMachines": 5,
        "sslVersion": 0,
        "targetResponseTime": 1000,
        "testName": "O365 Instant HTTP test",
        "url": O365URL,
        "verifyCertHostname": True
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': Authorization,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def delete_label(group_id):
    url = "https://api.thousandeyes.com/v6/groups/" + str(group_id) + "/delete.json"
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': Authorization
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
