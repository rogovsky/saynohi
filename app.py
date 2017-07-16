#!/usr/bin/env python3

import os
import json

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

FIELD_TYPE = "type"
FIELD_TOKEN = "token"
FIELD_CHALLENGE = "challenge"
FIELD_EVENT = "event"

REQ_TYPE_URL_VERIFICATION = "url_verification"
REQ_TYPE_MESSAGE = "event_callback"

EVENT_TYPE_MESSAGE = "message"

class UnsupportedRequestException(BaseException):
    pass


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Got Request:")
    print(json.dumps(req, indent=4))

    response = None
    try:
        raw_response = json.dumps(process_request(req))
        print("Responding:", raw_response)
        response = make_response(raw_response)
        response.headers['Content-Type'] = 'application/json'
    except UnsupportedRequestException:
        print("UnsupportedRequestException:", req)
        response = make_response("Unsupported request %s" % req, 400)
    except Exception as exc:
        print("Exception", exc)
        response = make_response("Unknown error", 500)

    return response


def process_request(req):
    request_type = req.get(FIELD_TYPE)
    if request_type == REQ_TYPE_URL_VERIFICATION:
        return process_handshake_request(req)
    elif request_type == REQ_TYPE_MESSAGE:
        return process_event_request(req)
    else:
        raise UnsupportedRequestException


def process_event_request(req):
    event = req.get(FIELD_EVENT)
    if event.get(FIELD_TYPE) == EVENT_TYPE_MESSAGE:
        process_users_message(event)
    return {}


def process_users_message(message_event):
    sender = message_event.get("user")
    text = message_event.get("text")


def process_handshake_request(req):
    return {"challenge": req.get(FIELD_CHALLENGE)}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
