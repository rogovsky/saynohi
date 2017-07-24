"""Contains data samples for tests"""
import json


bad_request_json = json.loads('{"some_tag": 0}')

valid_handshake_json = json.loads('{\
        "token": "Jhj5dZrVaK7ZwHHjRyZWjbDl",\
        "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P",\
        "type": "url_verification"\
    }')

sender = 'USLACKBOT'
message = 'I searched for that on our Help Center. Perhaps this article will help: <https://get.slack.help/hc/en-us/articles/216951758-Customize-your-team-s-call-settings|Customize your team call settings>'
message_hi = 'Hi'
auth_user = 'U03GALK02'
MESSAGE_FORMAT = '{\
        "token": "Qw671KoWqDm3iv2ok3leR9Ko",\
        "team_id": "T03G61VPV",\
        "api_app_id": "A69BQ5S2Z",\
        "event": {\
            "type": "message",\
            "user": "%s",\
            "text": "%s",\
            "ts": "1500183396.097119",\
            "channel": "D03GALK0C",\
            "event_ts": "1500183396.097119"\
        },\
        "type": "event_callback",\
        "authed_users": [\
            "%s"\
        ],\
        "event_id": "Ev69GLSSGM",\
        "event_time": 1500183396\
    }'

valid_message_event_json = json.loads(MESSAGE_FORMAT % (sender, message, auth_user))
hi_message_event_json = json.loads(MESSAGE_FORMAT % (sender, message_hi, auth_user))

valid_auth_response = b'{"ok":true,' \
                      b'"access_token":"xoxp-some_numbers_be_here",' \
                      b'"scope":"identify,im:history,chat:write:bot",' \
                      b'"user_id":"U03GALK02",' \
                      b'"team_name":"Distillery",' \
                      b'"team_id":"T03G61VPV"}'