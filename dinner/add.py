import asyncio
from pyscript import document
from datetime import datetime, timezone
from pyodide.http import pyfetch
import json

def toUTC(date_string):
    date_object = datetime.strptime(date_string, '%m/%d/%Y')
    date_utc = date_object.replace(tzinfo=timezone.utc)

    return date_utc.strftime('%Y-%m-%d %H:%M:%S UTC')

async def add_remind(event):
    time_remind = document.querySelector("#time_remind").value
    start_date = document.querySelector("#start_date").value
    end_date = document.querySelector("#end_date").value
    note = document.querySelector("#note").value

    if not time_remind or not start_date or not end_date or not note:
        return None

    url = 'http://127.0.0.1:8090/api/collections/reminds/records'

    remind_body = {
        'time_remind': time_remind,
        'start_date': toUTC(start_date),
        'end_date': toUTC(end_date),
        'note': note,
        'type': 'dinner'
    }
 
    headers = {'Content-Type': 'application/json'}
    res = await pyfetch(url=url, method="POST", body=json.dumps(remind_body), headers=headers)
    if res.status == 200:
        document.location.href = "/dinner/view.html"

