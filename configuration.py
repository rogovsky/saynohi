
import json
import os

CONFIG_FILE_PATH = "./env/config.txt"

SLACK_PERSONAL_API_KEY = "SLACK_PERSONAL_API_KEY"
SLACK_APP_API_KEY = "SLACK_APP_API_KEY"
SLACK_CLIENT_ID = "SLACK_CLIENT_ID"
SLACK_CLIENT_SECRET = "SLACK_CLIENT_SECRET"
SLACK_VERIFICATION_TOKEN = "SLACK_VERIFICATION_TOKEN"

slack_personal_api_key = None
slack_app_api_key = None
slack_client_id = None
slack_client_secret = None
slack_verification_token = None


def load(config_file_path=CONFIG_FILE_PATH):
    """Load configuration.

    Try to load from ENV, the from ./env/config.json file if present.
    """
    global slack_personal_api_key
    global slack_app_api_key
    global slack_client_id
    global slack_client_secret
    global slack_verification_token

    slack_personal_api_key = __load_by_name(SLACK_PERSONAL_API_KEY, config_file_path)
    slack_app_api_key = __load_by_name(SLACK_APP_API_KEY, config_file_path)
    slack_client_id = __load_by_name(SLACK_CLIENT_ID, config_file_path)
    slack_client_secret = __load_by_name(SLACK_CLIENT_SECRET, config_file_path)
    slack_verification_token = __load_by_name(SLACK_VERIFICATION_TOKEN, config_file_path)


def __load_by_name(var_name, config_file_path):
    result = os.getenv(var_name, None)
    if result is None:
        json_config = __get_json_config(config_file_path)
        result = json_config.get(var_name)
    return result


def __get_json_config(config_file_path, json_config={}):  # use default value as caching here
    if len(json_config) == 0 and os.path.exists(config_file_path):
        try:
            with open(config_file_path, 'r') as f:
                json_config.update(json.load(f))
        except (json.JSONDecodeError, IOError):
            pass
    return json_config
