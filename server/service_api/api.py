"""
Microservice that exposes the fantasy baseball hitter and pitcher data over
a RESTful API.
"""

# Standard imports
import sys

# 3rd party imports
from flask import Flask, Response
from flask_restful import Api, Resource

# Local imports
sys.path.append('../../')
from helpers.constants import get_server_addr, get_server_port
from helpers.paths import up_path
from helpers.pubsub import MessageAnnouncer
from helpers.threads import PropagatingThread
from server.service_api.fetch import fetch_data


app = Flask(__name__)
api = Api(app)


def stream(announcer: MessageAnnouncer):
    """
    Generates messages for SSE event streams.

    :param announcer: The object that is announcing new messages as they arrive.
    """
    messages = announcer.listen()  # returns a queue.Queue
    is_stream_finished = False
    while not is_stream_finished:
        msg = messages.get()  # blocks until a new message arrives
        is_stream_finished = announcer.is_final_stream()
        yield msg
    GeneratorExit()


def get_resource(csv_path: str) -> Response:
    """
    Creates an event stream response and fetches the data requested by the client.

    :param csv_path: The absolute path of the csv file.
    :return: The streamed Flask Response.
    """
    announcer = MessageAnnouncer()

    # fetch the data using a separate thread
    thread = PropagatingThread(target=fetch_data, args=(announcer,csv_path,))
    thread.start()
    thread.join()

    return Response(stream(announcer), mimetype='text/event-stream')


class Hitters(Resource):
    """
    A resource representing MLB hitters.
    """
    def get(self, file: str) -> Response:
        """
        Retrieves the data from the specified file.

        :param file: The name of the csv file.
        :return: The streamed Flask Response.
        """
        # convert the requested resource into a file path
        csv_path = up_path(__file__, 2) + f'/data/hitter_projections/{file}.csv'
        return get_resource(csv_path)


class Pitchers(Resource):
    """
    A resource representing MLB pitchers.
    """
    def get(self, file: str):
        """
        Retrieves the data from the specified file.

        :param file: The name of the csv file.
        :return: The streamed Flask Response.
        """
        # convert the requested resource into a file path
        csv_path = up_path(__file__, 2) + f'/data/pitcher_projections/{file}.csv'
        return get_resource(csv_path)


api.add_resource(Hitters, '/mlb/hitters/<string:file>')
api.add_resource(Pitchers, '/mlb/pitchers/<string:file>')


if __name__ == '__main__':
    app.run(host=get_server_addr(), port=get_server_port(), debug=True)
