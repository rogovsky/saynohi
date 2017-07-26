from cached_property import cached_property

FIELD_EVENT = "event"

EVENT_FIELD_TYPE = "type"
EVENT_TYPE_MESSAGE = "message"

EVENT_FIELD_TEXT = "text"
EVENT_FIELD_USER = "user"
EVENT_FIELD_SUBTYPE = "subtype"


class MessageEvent:
    """Represent message from Slack chat"""

    @staticmethod
    def is_message_event(event_json):
        event = event_json.get(FIELD_EVENT)
        return (event
                and event.get(EVENT_FIELD_TYPE) == EVENT_TYPE_MESSAGE
                and EVENT_FIELD_TEXT in event
                and EVENT_FIELD_SUBTYPE not in event)  # no subtype means it not messages edited/deleted event

    def __init__(self, event_json):
        self.event_root = event_json
        self.event = event_json.get(FIELD_EVENT)

    @cached_property
    def sender(self):
        return self.event.get(EVENT_FIELD_USER)

    @cached_property
    def text(self):
        return self.event.get(EVENT_FIELD_TEXT)

    @cached_property
    def auth_user(self):
        return self.event_root.get("authed_users")[0]

    @cached_property
    def is_incoming(self):
        return self.sender != self.auth_user
