"""
Downloads fantasy baseball data from the internet.
"""

# Standard imports
import json
import sys
import time

# 3rd party imports

# Local imports
sys.path.append('../../')
from helpers.pubsub import MessageAnnouncer, dict_sse, format_sse


def test(announcer: MessageAnnouncer, csv_path: str):
    """
    A function used to test the SSE stream.
    """
    n = 0
    while n <= 3:
        if n == 3:
            announcer.finalize_stream()
        d = dict_sse(data=f'downloading...{n}', final_stream=announcer.is_final_stream())
        msg = format_sse(data=json.dumps(d))
        announcer.announce(msg=msg)
        n += 1
        time.sleep(1)
    return   
