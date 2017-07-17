from cached_property import cached_property

FIELD_TYPE = "type"
FIELD_EVENT = "event"
EVENT_TYPE_MESSAGE = "message"


class MessageEvent:
    """Represent message from Slack chat"""

    @staticmethod
    def is_message_event(event_json):
        event = event_json.get(FIELD_EVENT)
        return event.get(FIELD_TYPE) == EVENT_TYPE_MESSAGE

    def __init__(self, event_json):
        self.event_root = event_json
        self.event = event_json.get(FIELD_EVENT)

    @cached_property
    def sender(self):
        return self.event.get("user")

    @cached_property
    def text(self):
        return self.event.get("text")

    @cached_property
    def auth_user(self):
        return self.event_root.get("authed_users")[0]

    @cached_property
    def is_incoming(self):
        return self.sender != self.auth_user
