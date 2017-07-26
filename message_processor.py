import slack_utils
from hi_detector import HiDetector
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
            print("Got incoming message :", event.text)
            if HiDetector.is_greeting(event.text):
                self.add_event_to_queue(event)

    @staticmethod
    def add_event_to_queue(event):
        print("Added to processing :", event.text)
        t = Timer(1.0,
                  slack_utils.send_message,
                  [event.sender, "Hi! How do you like <http://www.nohello.com|that>?"])
        t.start()
