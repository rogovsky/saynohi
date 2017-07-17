import slack_utils
from message_event import MessageEvent
from threading import Timer


class MessageProcessor:
    """Process incoming message events and schedule response if required"""

    def process(self, event_json):
        """@:param message_event json representing slack message.im event"""
        if not MessageEvent.is_message_event(event_json):
            return

        event = MessageEvent(event_json)
        if event.is_incoming:
            print("Got it :", event.text)
            text = event.text.strip().lower()
            if text == "hi" or text == "hello" or text == "hi!" or text == "hello!" or text == "привет"\
                    or "".startswith("i searched for that on our help center"):
                self.add_event_to_queue(event)

    @staticmethod
    def add_event_to_queue(event):
        print("Added to processing")
        t = Timer(1.0,
                  slack_utils.send_message,
                  [event.sender, "Hi! How do you like that?"])
        t.start()
