class Ticket:
    def __init__(self, key, event_time):
        self.key = key
        self.event_time = event_time

    @staticmethod
    def of_event(event):
        key = Ticket._create_event_key(event)
        return Ticket(key, event.time)

    @staticmethod
    def _create_event_key(event):
        return event.channel
