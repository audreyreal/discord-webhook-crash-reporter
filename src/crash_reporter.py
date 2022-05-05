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
