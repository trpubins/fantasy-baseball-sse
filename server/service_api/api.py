"""
Microservice that exposes the fantasy baseball hitter and pitcher data over
a RESTful API.
"""

# Standard imports
import json
import os
import sys
from threading import Thread
import time

# 3rd party imports
from flask import Flask, Response
from flask_restful import Api, Resource
import pandas as pd

# Local imports
sys.path.append('../../')
from helpers.constants import get_server_addr, get_server_port
from helpers.paths import up_path
from helpers.pubsub import MessageAnnouncer, dict_sse, format_sse
from server.service_api.http_abort import abort_cannot_read_csv, abort_file_not_found
from server.service_download.download import test


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


def read_csv(announcer: MessageAnnouncer, csv_path: str):
    """
    Attempts to read the comma separated values data at the specified path.
    Publishes the data using the announcer if read successfully.

    :param announcer: The object used for publishing messages.
    :param csv_path: The absolute path of the csv file.
    """
    df = pd.DataFrame()
    try:
        # attempt to read the csv data
        df = pd.read_csv(csv_path)
    except:
        abort_cannot_read_csv(csv_path)
    
    announcer.finalize_stream()
    
    # convert and format the dataframe into an event stream message
    d = dict_sse(data=df.to_json(), final_stream=True)
    msg = format_sse(data=json.dumps(d))
    
    # publish the message
    announcer.announce(msg=msg)
    return


def get_resource(csv_path: str) -> Response:
    """
    Retrieves the csv data from the specified path.

    :param csv_path: The absolute path of the csv file.
    :return: The streamed Flask Response.
    """
    # check that the requested resource exists
    if not os.path.exists(csv_path):
        abort_file_not_found(csv_path) 
    
    announcer = MessageAnnouncer()

    # check if file has been modified in the last 12 hours
    mod_time = os.path.getmtime(csv_path)
    current_time = time.time()
    delta_s = current_time - mod_time
    delta_hr = delta_s / 60 / 60

    if delta_hr > 12:
        # retrieve latest results from internet
        thread = Thread(target=test, args=(announcer,csv_path,))  # threading.Thread class needs an iterable of arguments as the args parameter
        thread.start()
    else:
        thread = Thread(target=read_csv, args=(announcer,csv_path,))  # threading.Thread class needs an iterable of arguments as the args parameter
        thread.start()

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
