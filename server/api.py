"""Microservice that exposes the fantasy baseball hitter and pitcher
data over a RESTful API.
"""

# Standard modules
import os
import sys

# 3rd party modules
from flask import Flask, Response
from flask_restful import Api, Resource

# Project modules
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from helpers.constants import get_server_addr, get_server_port
from helpers.paths import up_path
from helpers.pubsub import MessageAnnouncer
from helpers.threads import PropagatingThread
from server.fetch import fetch_data
from server.http_abort import abort_file_not_found


app = Flask(__name__)
api = Api(app)


def stream(announcer: MessageAnnouncer):
    """Generates messages for SSE event streams.

    Parameters
    ----------
    announcer : pubsub.MessageAnnouncer
        The object that is announcing new messages as they arrive.
    """
    messages = announcer.listen()  # returns a queue.Queue
    is_stream_finished = False
    while not is_stream_finished:
        msg = messages.get()  # blocks until a new message arrives
        is_stream_finished = announcer.is_final_stream()
        yield msg
    GeneratorExit()


def get_resource(csv_path: str) -> Response:
    """Creates an event stream response and fetches the data
    requested by the client using threading.

    Parameters
    ----------
    csv_path : str
        The absolute path of the csv file.

    Returns
    -------
    flask.Response
        The streamed Flask Response.
    """
    # check that the requested resource exists
    if not os.path.exists(csv_path):
        abort_file_not_found(csv_path)
    
    # initialize a shared announcer
    announcer = MessageAnnouncer()

    # fetch the data with a separate thread
    thread = PropagatingThread(target=fetch_data,
                               args=(announcer,csv_path,))  # threading.Thread class needs an iterable of arguments as the args parameter
    thread.start()

    return Response(stream(announcer), mimetype='text/event-stream')


class Hitters(Resource):
    """A resource representing MLB hitters."""
    
    def get(self, file: str) -> Response:
        """Retrieves the data from the specified file.

        Parameters
        ----------
        file : str
            The name of the csv file.
        
        Returns
        -------
        flask.Response
            The streamed Flask Response.
        """
        # convert the requested resource into a file path
        csv_path = up_path(__file__, 1) + f'/data/hitter_projections/{file}.csv'
        return get_resource(csv_path)


class Pitchers(Resource):
    """A resource representing MLB pitchers."""
    
    def get(self, file: str):
        """Retrieves the data from the specified file.

        Parameters
        ----------
        file : str
            The name of the csv file.
        
        Returns
        -------
        flask.Response
            The streamed Flask Response.
        """
        # convert the requested resource into a file path
        csv_path = up_path(__file__, 1) + f'/data/pitcher_projections/{file}.csv'
        return get_resource(csv_path)


# register the api endpoints
api.add_resource(Hitters, '/mlb/hitters/<string:file>')
api.add_resource(Pitchers, '/mlb/pitchers/<string:file>')


if __name__ == '__main__':
    app.run(host=get_server_addr(), port=get_server_port(), debug=True)
