from slacker import Slacker
from slacker import Error

slacker = Slacker("API KEY HERE")


def send_message(user_id, text):
    try:
        # slacker.chat.post_message(user_id, #uncomment once we debug everything
        slacker.chat.post_message("USLACKBOT",
                                  text,
                                  as_user=True)
        user_info = get_slack_user_by_id(user_id)
        print("Sent response to %s" % user_info.get("real_name"))
    except Error:
        print("Unable to send message to user by ID: %s" % user_id)


def get_slack_user_by_id(user_id):
    return slacker.users.info(user_id).body['user']
