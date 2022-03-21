"""Fetches the fantasy baseball data for the microservice.
"""

# Standard modules
import json
import os
import sys
import time

# 3rd party modules
import pandas as pd

# Project modules
from helpers.pubsub import MessageAnnouncer, dict_sse, format_sse
from server.http_abort import abort_cannot_read_csv

# Constants
MAX_TIME_BETWEEN_REFRESH = 12  # hrs


def fetch_data(announcer: MessageAnnouncer, csv_path: str):
    """Fetches the csv data from the specified path and publishes the data once retrieved.
    Downloads from the internet if data is outdated.

    Parameters
    ----------
    announcer : pubsub.MessageAnnouncer
        The object used for publishing messages.
    
    csv_path : str
        The absolute path of the csv file.
    """
    # check if file has been modified in the last 12 hours
    mod_time = os.path.getmtime(csv_path)
    current_time = time.time()
    delta_s = current_time - mod_time
    delta_hr = delta_s / 60 / 60

    if delta_hr > MAX_TIME_BETWEEN_REFRESH:
        # retrieve latest results from internet
        test(announcer, csv_path)
    
    # read the data on disk
    read_csv(announcer, csv_path)
    
    return


def read_csv(announcer: MessageAnnouncer, csv_path: str):
    """Attempts to read the comma separated values data at the specified path.
    Publishes the data using the announcer if read successfully.

    Parameters
    ----------
    announcer : pubsub.MessageAnnouncer
        The object used for publishing messages.
    
    csv_path : str
        The absolute path of the csv file.
    """
    df = None
    try:
        # attempt to read the csv data
        df = pd.read_csv(csv_path)
    except:
        # TODO: send an error message thru stream
        abort_cannot_read_csv(csv_path)
    
    announcer.finalize_stream()
    
    # convert and format the dataframe into an event stream message
    d = dict_sse(data=df.to_json(), final_stream=True)
    msg = format_sse(data=json.dumps(d))
    
    # publish the message
    announcer.announce(msg=msg)
    return


def test(announcer: MessageAnnouncer, csv_path: str):
    """A function used to test the SSE stream.

    Parameters
    ----------
    announcer : pubsub.MessageAnnouncer
        The object used for publishing messages.
    
    csv_path : str
        The absolute path of the csv file.
    """
    n = 0
    while n <= 3:
        d = dict_sse(data=f'downloading...{n}', final_stream=announcer.is_final_stream())
        msg = format_sse(data=json.dumps(d))
        announcer.announce(msg=msg)
        n += 1
        time.sleep(1)
    return   
