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
sys.path.append('../../')
import baseball
from helpers.constants import get_server_addr, get_server_port


def main():
    """
    Driver function.
    """
    dataframes = {
        'hitters': dict(),
        'pitchers': dict()
    }
    for player_type in dataframes.keys():
        dataframes[player_type] = get_mlb_data(player_type)
    

def get_mlb_data(player_type: str) -> dict:
    """
    Retrieves all data from the server for the associated player type.

    :param player_type: The type of mlb player.
    :return: A dictionary of dataframes where the keys are the filename sources.
    """
    dfs = dict()  # a dictionary of dataframes
    server_url = f'http://{get_server_addr()}:{get_server_port()}'
    for fname in baseball.fnames:
        url = f'{server_url}/mlb/{player_type}/{fname}'
        try:
            # handle the SSE stream
            df = handle_sse(url)
            dfs[fname] = df
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
    return dfs


def handle_sse(url: str) -> pd.DataFrame:
    """
    Handles a Server Sent Events (SSE) connection stream between a client and a server.

    :param url: The server resource to connect.
    :return: The data sent over the final stream as a pandas DataFrame.
    """
    df = None
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
    return df


if __name__ == '__main__':    
    main()
