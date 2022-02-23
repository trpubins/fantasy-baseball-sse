"""
Client application for a fantasy baseball auction values generator.
"""

# Standard imports
import json
import sys

# 3rd party imports
import pandas as pd
import requests
from sseclient import SSEClient

# Local imports
from baseball import *
sys.path.append('../../')
from helpers.constants import get_server_addr, get_server_port


def handle_sse(url: str):
    """
    Handles a Server Sent Events (SSE) connection stream between a client and a server.

    :param url: The server resource to connect.
    """
    client = SSEClient(url)
    response = client.resp
    print(f'\nstatus_code={response.status_code}')
    for event in client:
        content = json.loads(event.data)
        data = content['data']
        if content['final_stream']:
            try:
                df = pd.read_json(data)
                print(df)
            except ValueError as exception:
                print(data)

            # close the connection per https://github.com/btubbs/sseclient/issues/10#issuecomment-367886005
            response.close()
            break
        else:
            print(data)
    del(client)


if __name__ == '__main__':    
    server_url = f'http://{get_server_addr()}:{get_server_port()}'
    for fname in fnames:
        url = f'{server_url}/mlb/hitters/{fname}'
        try:
            # handle the SSE stream
            handle_sse(url)
        except requests.HTTPError as exception:
            # handle non OK statuses gracefully
            print(exception)
            try:
                # display the HTTPError message if one exists
                text = json.loads(exception.response.text)
                key = 'message'
                if key in text.keys():
                    print(text[key])
            except:
                pass
            continue
