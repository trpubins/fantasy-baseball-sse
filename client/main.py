"""Client application for a fantasy baseball auction values generator.
"""

# Standard modules
import json
import os
import sys

# 3rd party modules
import pandas as pd
import requests
from sseclient import SSEClient

# Project modules
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import baseball
from helpers.constants import get_server_addr, get_server_port
from helpers.log import get_logger

# Configure logging
LOG = get_logger(__name__)


def main():
    """Driver function."""
    dataframes = {
        'hitters': dict(),
        # 'pitchers': dict()
    }
    for player_type in dataframes.keys():
        dataframes[player_type] = get_mlb_data(player_type)
    return None
    

def get_mlb_data(player_type: str) -> dict:
    """Retrieves all data from the server for the associated player type.

    Parameters
    ----------
    player_type : str
        The type of mlb player.
    
    Returns
    -------
    dict
        A dictionary of dataframes where the keys are the filename sources.
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
            LOG.error(exception)
            try:
                # display the HTTPError message if one exists
                text = json.loads(exception.response.text)
                key = 'message'
                if key in text.keys():
                    LOG.error(text[key])
            except:
                pass
            continue
    return dfs


def handle_sse(url: str) -> pd.DataFrame:
    """Handles a Server Sent Events (SSE) connection stream between
    a client and a server.

    Parameters
    ----------
    url : str
        The server resource to connect.
    
    Returns
    -------
    pandas.DataFrame
        The data sent over the final stream as a dataframe.
    """
    df = None
    client = SSEClient(url)
    response = client.resp
    LOG.info(f'status_code={response.status_code}')
    for event in client:
        content = json.loads(event.data)
        data = content['data']
        if content['final_stream']:
            try:
                df = pd.read_json(data)
                LOG.info(f'\n{df}')
            except ValueError as exception:
                LOG.error(exception)

            # close the connection per 
            # https://github.com/btubbs/sseclient/issues/10#issuecomment-367886005
            response.close()
            break
        else:
            LOG.info(data)
    del(client)
    return df


if __name__ == '__main__':    
    main()
