"""
Microservice that exposes the fantasy baseball hitter and pitcher data over
a RESTful API.
"""

# Standard imports
import os
import sys
from threading import Thread

# 3rd party imports
from flask import Flask, Response
from flask_restful import Api, Resource
import pandas as pd

# Local imports
sys.path.append('../../')
from helpers.constants import get_server_addr, get_server_port
from helpers.paths import up_path
from helpers.pubsub import MessageAnnouncer, format_sse
from server.service_api.http_abort import abort_cannot_read_csv, abort_file_not_found
from server.service_download.download import test


app = Flask(__name__)
api = Api(app)


def stream(announcer: MessageAnnouncer):
        messages = announcer.listen()  # returns a queue.Queue
        n = 0
        while n <= 3:
            msg = messages.get()  # blocks until a new message arrives
            n += 1
            yield msg
        return


class Hitters(Resource):
    """
    A resource representing MLB hitters.
    """
    def get(self, file: str):
        """
        Retrieves the data from the specified file.

        :param file: The name of the csv file
        :return: The data as a dict along with the http status code
        """
        # convert the requested resource into a file path
        csv_path = up_path(__file__, 2) + f'/data/hitter_projections/{file}.csv'
        if not os.path.exists(csv_path):
            abort_file_not_found(csv_path) 
        # attempt to read the csv file into a data frame
        try:
            announcer = MessageAnnouncer()
            
            thread = Thread(target=test, args=(announcer,))
            thread.start()

            return Response(stream(announcer), mimetype='text/event-stream')

            # df = pd.read_csv(csv_path)
            # return {'data': df.to_json()}, 200
        except:
            abort_cannot_read_csv(csv_path)


class Pitchers(Resource):
    """
    A resource representing MLB pitchers.
    """
    def get(self, file: str):
        """
        Retrieves the data from the specified file.

        :param file: The name of the csv file
        :return: The data as a dict along with the http status code
        """
        # convert the requested resource into a file path
        csv_path = up_path(__file__, 2) + f'/data/pitcher_projections/{file}.csv'
        if not os.path.exists(csv_path):
            abort_file_not_found(csv_path) 
        # attempt to read the csv file into a data frame
        try:
            df = pd.read_csv(csv_path)
            return {'data': df.to_json()}, 200
        except:
            abort_cannot_read_csv(csv_path)


api.add_resource(Hitters, '/mlb/hitters/<string:file>')
api.add_resource(Pitchers, '/mlb/pitchers/<string:file>')


if __name__ == '__main__':
    app.run(host=get_server_addr(), port=get_server_port(), debug=True)
