# MIT License
#
# Copyright (c) 2022 sweeze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import getlogin
from datetime import datetime
import requests


def anonymize_traceback(traceback: str, new_user: str) -> str:
    """Takes a traceback and removes the username from it

    Args:
        traceback (str): The original traceback with username
        new_user (str): The username to replace the old one in the traceback with

    Returns:
        str: The new traceback with the username replaced with new_user
    """
    universal_traceback: str = traceback.replace("\\", "/")
    return universal_traceback.replace(f"/{getlogin()}", f"/{new_user}")


def upload(webhook_url: str, traceback: str) -> int:
    """Sends a traceback string to a discord webhook for sake of crash reporting

    Args:
        webhook_url (str): Link to the discord webhook
        traceback (str): Traceback string, will attempt to anonymize if not already

    Returns:
        int: Status code of the response
    """
    if f"/{getlogin()}" in traceback.replace("\\", "/"):
        traceback = anonymize_traceback(traceback, "RemovedForAnonymization")

    data: dict = {
        "content": f"''{traceback}''",
        "username": str(datetime.today()),
    }

    headers: dict = {"User-Agent": "Crash reporter"}

    response: requests.Response = requests.post(webhook_url, headers=headers, json=data)
    return response.status_code
