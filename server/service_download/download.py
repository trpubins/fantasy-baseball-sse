"""
Downloads fantasy baseball data from the internet.
"""

# Standard imports
import sys
import time

# 3rd party imports

# Local imports
sys.path.append('../../')
from helpers.pubsub import MessageAnnouncer, format_sse


def test(announcer: MessageAnnouncer):
    n = 0
    while n <= 3:
        msg = format_sse(data=f'downloading...{n}')  # threading.Thread class needs an iterable of arguments as the args parameter
        announcer.announce(msg=msg)
        n += 1
        time.sleep(1)
    return   
