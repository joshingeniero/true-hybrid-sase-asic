# Webex Bot
BOT_ID = 'BOT_ID'
BOT_TOKEN = 'BOT_TOKEN'
BOT_EMAIL = 'yoursasebot@webex.bot'

# Umbrella
UMBRELLA_REPORTING_KEY = 'REPORTING_KEY'
UMBRELLA_REPORTING_SECRET = 'REPORTING_SECRET'
UMBRELLA_ORG_ID = 'ORG_ID'

# Meraki
MERAKI_API_KEY = 'API_KEY'
MERAKI_NET_ID = 'NET_ID'
MERAKI_ORG_ID = 12345

# ThousandEyes
Authorization = 'Bearer BEARER_TOKEN_HERE'
ENT_AGENT = 123456


# Card Payload for Employees
CARD_PAYLOAD = """{
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.2",
    "body": [
        {
            "type": "TextBlock",
            "size": "Large",
            "weight": "Bolder",
            "text": "IT Self-Help Bot",
            "horizontalAlignment": "Center",
            "color": "Light"
        },
        {
            "type": "Input.Text",
            "placeholder": "Device Hostname",
            "style": "text",
            "maxLength": 0,
            "id": "hostnameVal"
        },
        {
            "type": "TextBlock",
            "size": "Medium",
            "weight": "Bolder",
            "text": "What's the Issue",
            "horizontalAlignment": "Center"
        },
        {
            "type": "TextBlock",
            "text": "Which applications are experiencing issue? (multiselect)"
        },
        {
            "type": "Input.ChoiceSet",
            "id": "IssueSelectVal",
            "isMultiSelect": true,
            "choices": [
                {
                    "title": "Office 365",
                    "value": "Office365"
                },
                {
                    "title": "Webex Audio",
                    "value": "WebexAudio"
                },
                {
                    "title": "Webex Video",
                    "value": "WebexVideo"
                },
                {
                    "title": "salesforce",
                    "value": "salesforce"
                },
                {
                    "title": "None of above",
                    "value": "Noneofabove"
                }
            ]
        },
        {
            "type": "Input.Text",
            "placeholder": "What's url of the application?",
            "style": "text",
            "maxLength": 0,
            "id": "CustomURLVal"
        },
        {
            "type": "Input.Toggle",
            "title": "I acknowledge that Bubble Team is the best tEaM",
            "valueOn": "true",
            "valueOff": "false",
            "id": "AcceptsTerms"
        }
    ],
    "actions": [
        {
            "type": "Action.Submit",
            "title": "Submit",
            "data": {
                "action": "newTest",
                "id": "inputTypesExample"
            }
        },
        {
            "type": "Action.ShowCard",
            "title": "Show Card",
            "card": {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "Input.Text",
                        "placeholder": "enter comment",
                        "style": "text",
                        "maxLength": 0,
                        "id": "CommentVal"
                    }
                ],
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "OK",
                        "data": {
                            "cardType": "input"
                        }
                    }
                ]
            }
        }
    ]
}
    }"""