from slacker import Slacker
from slacker import Error

slack_client = None


def init(api_key):
    global slack_client
    slack_client = Slacker(api_key)


def send_message(user_id, text):
    try:
        slack_client.chat.post_message(user_id,
                                       text,
                                       as_user=False)
        user_name = get_slack_name_by_id(user_id)
        print("Sent response to %s" % user_name)
    except Error as exc:
        print("Unable to send message to user by ID: %s. Reason: %s" % (user_id, exc))


def get_slack_name_by_id(user_id):
    try:
        return get_slack_user_by_id(user_id).get("real_name")
    except Error:
        return user_id


def get_slack_user_by_id(user_id):
    return slack_client.users.info(user_id).body['user']
