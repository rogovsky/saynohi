from queue import Full
from queue import Queue


class QueueManager:
    """Manages queue of tickets related to Hi! messages.
    For each detected hi message there is a ticket in the queue once time to process it comes queue can be queried
    if ticket still have to be processed. Each ticket can be voided but not removed from queue. We assume that tickets
    should be added in chronological order."""
    def __init__(self):
        self._tickets = Queue()
        """Queue of channels where hi message was detected"""
        self._events_map = {}
        """Contains all Hi events that need to be processed, events may be voided and removed from this map
         by appropriate message in same channel during the tolerance interval"""

    def add(self, ticket, event):
        """Add event and ticket associated to it"""
        try:
            self._tickets.put_nowait(ticket)
            self._events_map[ticket.key] = event
            print("Added to queue :", event.text, str(event.time))
        except Full:
            print("Failed to add event to queue. Queue is full")

    def get_next_ticket(self):
        """Get next ticket from queue"""
        return self._tickets.get()

    def void(self, ticket):
        """Erase event
        Keeps ticket in the queue but void the event itself"""
        try:
            del(self._events_map[ticket.key])
        except KeyError:
            pass

    def pop_item(self, ticket):
        """Pop item by ticket, returns None if event was voided"""
        return self._events_map.pop(ticket.key, None)

    def get_item(self, ticket):
        """Get item by ticket, returns None if event was voided"""
        return self._events_map.get(ticket.key, None)
