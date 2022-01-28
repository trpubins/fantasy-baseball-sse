"""
Fetches the fantasy baseball data for the microservice.
"""

# Standard imports
import json
import os
import sys
from threading import Thread
import time

# 3rd party imports
import pandas as pd

# Local imports
sys.path.append('../../')
from helpers.pubsub import MessageAnnouncer, dict_sse, format_sse
from server.service_api.http_abort import abort_cannot_read_csv, abort_file_not_found
from server.service_download.download import test


def fetch_data(announcer: MessageAnnouncer, csv_path: str):
    """
    Fetches the csv data from the specified path, and publishes the data once retrieved.

    :param announcer: The object used for publishing messages.
    :param csv_path: The absolute path of the csv file.
    """
    # check that the requested resource exists
    if not os.path.exists(csv_path):
        abort_file_not_found(csv_path)

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
    
    return
    

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
