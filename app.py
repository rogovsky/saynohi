#!/usr/bin/env python3

import os
import json
from urllib.parse import urlencode

from flask import Flask
from flask import request
from flask import make_response
import httplib2

import configuration
import slack_utils
from message_processor import MessageProcessor

EVENT_API_FIELD_TYPE = "type"
EVENT_API_FIELD_TOKEN = "token"
EVENT_API_FIELD_CHALLENGE = "challenge"

EVENT_API_REQ_TYPE_URL_VERIFICATION = "url_verification"
EVENT_API_REQ_TYPE_EVENT = "event_callback"

AUTH_API_ARG_CODE = "code"
AUTH_API_ARG_STATE = "state"

message_processor = MessageProcessor()
http_client = httplib2.Http(".cache")
app = Flask(__name__)  # Flask app should start in global layout


class UnsupportedRequestException(BaseException):
    pass


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Got WebHook Request:", json.dumps(req, indent=4))
    return process_event_api_request(req)


def error_handling_processor(func):
    """Decorator for functions that take single request argument and return dict response."""

    def error_handling_wrapper(req):
        try:
            # main call performed here
            response_body_json = func(req)

            response_body = json.dumps(response_body_json)
            print("Responding:", response_body)
            response = make_response(response_body)
            response.headers['Content-Type'] = 'application/json'
        except UnsupportedRequestException:
            print("UnsupportedRequestException:", req)
            response = make_response("Unsupported request %s" % req, 400)
        except Exception as exc:
            print("Exception", exc)
            response = make_response("Unknown error", 500)
        return response

    return error_handling_wrapper


@error_handling_processor
def process_event_api_request(req):
    request_type = req.get(EVENT_API_FIELD_TYPE)
    if request_type == EVENT_API_REQ_TYPE_URL_VERIFICATION:
        return process_handshake_request(req)
    elif request_type == EVENT_API_REQ_TYPE_EVENT:
        return process_event_request(req)
    else:
        raise UnsupportedRequestException


def process_event_request(req):
    message_processor.process(req)
    return {}


def process_handshake_request(req):
    return {"challenge": req.get(EVENT_API_FIELD_CHALLENGE)}


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    args = request.args
    print("Got Auth Args: %s" % args)
    return process_auth_request(args)


@error_handling_processor
def process_auth_request(args):
    code = args.get(AUTH_API_ARG_CODE)

    auth_response, response_content = make_auth_request(code)
    parse_auth_response(auth_response, response_content)
    return {}


def make_auth_request(code):
    if code is None:
        raise UnsupportedRequestException
    answer_args = urlencode({
        "client_id": configuration.slack_client_id,
        "client_secret": configuration.slack_client_secret,
        "code": code
    })
    return http_client.request("https://slack.com/api/oauth.access" + "?" + answer_args)


def parse_auth_response(auth_response, response_content):
    if auth_response.status == 200:
        response = json.loads(response_content.decode())
        if response.get("ok"):
            access_token = response.get("access_token")
            team_id = response.get("team_id")
            user_id = response.get("user_id")
            team_name = response.get("team_name")
            print("Authenticated user %s with token: ***%s in team: %s/%s" % (
                user_id, access_token[:4], team_id, team_name))
        else:
            print("Auth request error. Get: ", response_content)
    else:
        print("Auth request error. Bad response: ", auth_response, response_content)


if __name__ == '__main__':
    configuration.load()
    print("Slack API: ***%s" % configuration.slack_personal_api_key[:4])
    slack_utils.init(configuration.slack_personal_api_key)

    port = int(os.getenv('PORT', 5000))
    print("Starting app on port: %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
