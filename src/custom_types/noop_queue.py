""" Placeholder no-operation Queue Module """

from queue import Queue


class NoopQueue(Queue):
    """ A no-operation (no-op) implementation of the Queue class.

    This class inherits from the Queue class and overrides the `put` and `get` methods to provide a
    behavior where items are not actually added or retrieved from the queue. Instead, any items added are
    discarded, and any attempt to retrieve items will always yield None. The `empty` method always returns True.

    This class can be used in scenarios where you need a placeholder or a dummy queue that maintains the interface
    of the Queue class but does not perform any actual queuing operations.
    """

    def put(self, *args):
        """ Discard the provided items without adding them to the queue."""
        return

    def get(self, *args):
        """ Return None without retrieving any items from the queue."""
        return None
