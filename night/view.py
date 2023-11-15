import asyncio
from pyscript import document, window
from datetime import datetime
from pyodide.http import pyfetch

def toLocalDate(utc_date_string):
    utc_datetime = datetime.strptime(utc_date_string, "%Y-%m-%d %H:%M:%S %Z")
    return utc_datetime.strftime("%d/%m/%Y")


def card(time, start_date, end_date, note, id):
    return f'''
        <div class="bg-gray-200 grid grid-cols-2 items-center gap-2 m-8 p-4 rounded-lg">
        <div>
          <p class="text-2xl">{time}</p>
          <p class="text-xs text-gray-500">
            {start_date} - {end_date}
          </p>
        </div>
        <button py-click="delete_remind" class="w-8 h-8 justify-self-end">
            <input id="id" type="hidden" value="{id}">
      ลบ
        </button>
        <div class="col-span-2 text-xs text-gray-400">
          {note}
        </div>
      </div>
    '''

async def fetch_remind():
    res = await pyfetch(url="http://3.234.92.219//api/collections/reminds/records/?filter=(type='night')&skipTotal=true", method="GET")
    body = await res.json()
    for item in body.get('items'):
        id = item['id']
        time = item['time_remind']
        start_date = toLocalDate(item['start_date'])
        end_date = toLocalDate(item['end_date'])
        note = item['note']
        document.querySelector("#output").innerHTML += card(time = time, start_date=start_date, end_date=end_date, note=note, id=id)

async def delete_remind(event):
    id = event.target.querySelector("#id").value
    url = "http://3.234.92.219//api/collections/reminds/records/" + id
    res = await pyfetch(url=url, method="DELETE")
    if res.status == 204:
         window.location.reload()

await fetch_remind()