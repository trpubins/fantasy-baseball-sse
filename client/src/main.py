"""
Client application for a fantasy baseball auction values generator.
"""

# Standard imports
import sys

# 3rd party imports
import pandas as pd
import requests
from sseclient import SSEClient

# Local imports
from baseball import *
sys.path.append('../../')
from helpers.constants import HttpStatus, get_server_addr, get_server_port


if __name__ == '__main__':    
    server_url = f'http://{get_server_addr()}:{get_server_port()}'
    # for fname in fnames:
    #     response = requests.get(server_url + f'/mlb/hitters/{fname}')
    #     content = response.json()
    #     print(f'status code: {response.status_code}')
    #     if response.status_code != HttpStatus.OK:
    #         if 'message' in content:
    #             print(content['message'])
    #         continue
    #     data = content['data']
    #     df = pd.read_json(data)
    #     print(df)
    url = f'{server_url}/mlb/hitters/ATC'
    messages = SSEClient(url)

    for msg in messages:
        print(msg)
