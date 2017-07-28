"""Contains data samples for tests"""
import json


MESSAGE_FORMAT = '{\
        "token": "Qw671KoWqDm3iv2ok3leR9Ko",\
        "team_id": "T03G61VPV",\
        "api_app_id": "A69BQ5S2Z",\
        "event": {\
            "type": "message",\
            "user": "%s",\
            "text": "%s",\
            "ts": "1500183396.097119",\
            "channel": "%s",\
            "event_ts": "1500183396.097119"\
        },\
        "type": "event_callback",\
        "authed_users": [\
            "U03GALK02"\
        ],\
        "event_id": "Ev69GLSSGM",\
        "event_time": 1500183396\
    }'

bad_request_json = json.loads('{"some_tag": 0}')

valid_handshake_json = json.loads('{\
        "token": "Jhj5dZrVaK7ZwHHjRyZWjbDl",\
        "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P",\
        "type": "url_verification"\
    }')

channel_std = 'D03GALK0C'
sender_std = 'USLACKBOT'
message_std = 'I searched for that. Perhaps this can help: <https://get.slack.help/|Customize your call settings>'
standard_message_event_json = json.loads(MESSAGE_FORMAT % (sender_std, message_std, channel_std))

channel_hi = 'D03GALK0D'
sender_hi = 'U03GALK02'
message_hi = 'Hi'
hi_message_event_json = json.loads(MESSAGE_FORMAT % (sender_hi, message_hi, channel_hi))

message_edited_event_json = json.loads('{"token":"Qw671KoWqDm3iv2ok3leR9Ko","team_id":"T03G61VPV",\
           "api_app_id":"A69BQ5S2Z","event":{"type":"message","message":{"type":"message","user":"U03GALK02",\
           "text":"Hi","edited":{"user":"U03GALK02","ts":"1501039832.000000"},"ts":"1501039808.189255"},\
           "subtype":"message_changed","hidden":true,"channel":"D03GALK0C","previous_message":{"type":"message",\
           "user":"U03GALK02","text":"Hi!","ts":"1501039808.189255"},"event_ts":"1501039832.193701",\
           "ts":"1501039832.193701"},"type":"event_callback","authed_users":["U03GALK02"],"event_id":"Ev6DJTMBAP",\
           "event_time":1501039832}')

valid_auth_response = b'{"ok":true,' \
                      b'"access_token":"xoxp-some_numbers_be_here",' \
                      b'"scope":"identify,im:history,chat:write:bot",' \
                      b'"user_id":"U03GALK02",' \
                      b'"team_name":"Distillery",' \
                      b'"team_id":"T03G61VPV"}'