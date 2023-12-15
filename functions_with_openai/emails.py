import datetime as dt
import logging

import pythoncom
import win32com.client
from azure.functions import Blueprint, TimerRequest

import utils

email_app = Blueprint()


@email_app.timer_trigger(schedule="0 */30 * * * *", arg_name="mytimer",
                         run_on_startup=False,
                         use_monitor=False)
def upload_mails_to_cosmos(mytimer: TimerRequest):
    pythoncom.CoInitialize()
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace(
        "MAPI")
    inbox = outlook.GetDefaultFolder(6)
    messages = inbox.Items
    
    # Gets message from the previous week
    lastWeekDateTime = dt.datetime.now() - dt.timedelta(days=7)
    lastWeekDateTime = lastWeekDateTime.strftime(
        '%m/%d/%Y %H:%M %p')  # <-- This format compatible with "Restrict"

    messages = messages.Restrict("[ReceivedTime] >= '" + lastWeekDateTime + "'")

    logging.info(f"Total number of emails: {len(messages)}")

    utils.transform_and_update_to_cosmos(messages)

