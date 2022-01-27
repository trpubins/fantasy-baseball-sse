"""
A module that conforms to the Publish-Subscribe (pubsub) pattern.
"""

# Standard imports
import queue  # this module is thread-safe


class MessageAnnouncer:
    """
    Class that implements the pubsub pattern so messages are not directly sent to listeners. 
    Instead, this class relays messages to the listeners. The advantage is that the message emitter doesn't have to check that the message gets dispatched correctly. 
    This class is delegated for such purpose.
    See https://maxhalford.github.io/blog/flask-sse-no-deps/
    """

    def __init__(self):
        self.listeners = []
        self.final_stream = False


    def listen(self) -> queue.Queue:
        """
        Allows a client to start listening on an HTTP stream.

        :return: A queue where new messages will be delivered.
        """
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q


    def announce(self, msg: str):
        """
        Dispatches the specified message to every listener. Additionally, it removes listeners that don't "seem" to be listening anymore.
        We assume that if a message queue is full, then it's because the queue is not being read from anymore.

        :param msg: The message to be relayed (announced) to the listeners.
        """
        for i in reversed(range(len(self.listeners))):
            try:
                q = self.listeners[i]
                q.put_nowait(msg)
            except queue.Full:
                del self.listeners[i]


    def finalize_stream(self):
        """
        Finalizes the stream by indicating there is one final message to send over the event stream.
        """
        self.final_stream = True


    def is_final_stream(self) -> bool:
        """
        Retrieve the status of the final event stream.

        :return: True if this is the final event stream, False otherwise.
        """
        return self.final_stream


def dict_sse(data: str, final_stream: bool) -> dict:
    """
    A simple dictionary generator to ensure consistency when packing data to send over an event stream.
    
    :param data: The data to be sent over the stream.
    :param final_stream: Describes if the data is part of the server's final event stream.
    :return: A dictionary object.
    """
    d = dict()
    d['data'] = data
    d['final_stream'] = final_stream
    return d


def format_sse(data: str, event=None) -> str:
    """
    Formats a message to be used in an event stream as documented here:
    https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format

    :param data: The data field for the message.
    :param event: A string identifying the type of event described. 
    If this is specified, an event will be dispatched on the browser to the listener for the specified event name.
    :return: The (formatted) event stream message.
    """
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg
