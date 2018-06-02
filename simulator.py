import requests as r
import time
import json
import datetime
from pprint import pprint

url = "http://layer7.kr:4567"

base = {1: datetime.datetime(2018, 6, 2, 22, 30, 00),
        2: datetime.datetime(2018, 6, 2, 23, 49, 57)}

source = [{"id" :1,
           "latitude": 37.415833,
           "longitude": 127.1016,
           "control": [{"t": 38, "now": 0, "red": False, "yellow": False, "green": False, "left": True},
                       {"t": 16, "now": 0, "red": True, "yellow": False, "green": False, "left": False},
                       {"t": 146, "now": 0, "red": False, "yellow": False, "green": True, "left": False},
                       {"t":  0, "now": 0, "red": True, "yellow": True, "green": False, "left": False}]},
          {"id": 2,
           "latitude": 37.41974,
           "longitude": 127.102486,
           "control": [{"t": 10, "now": 0, "red": False, "yellow": False, "green": False, "left": True},
                       {"t": 48, "now": 0, "red": True, "yellow": False, "green": False, "left": False},
                       {"t": 142, "now": 0, "red": False, "yellow": False, "green": True, "left": False},
                       {"t": 0, "now": 0, "red": True, "yellow": True, "green": False, "left": False}]},
         ]
"""
 {"id": 3,
           "latitude": 37.412903,
           "longitude": 127.09995,
           "control": [{"t": 35, "now": 0, "red": True, "yellow": False, "green": False, "left": True},
                       {"t": 20, "now": 0, "red": True, "yellow": False, "green": False, "left": False},
                       {"t": 135, "now": 0, "red": False, "yellow": False, "green": True, "left": False},
                       {"t":  5, "now": 0, "red": True, "yellow": True, "green": False, "left": False}]}
"""

def custom_sleep(s, ms):
    startTime = datetime.datetime.now()

    while True:
        endTime = datetime.datetime.now()
        gap = endTime - startTime
        if gap.seconds >= s and gap.microseconds >= ms:
            break

def process(item, pm):
    send_object = {"id": item["id"], "latitude": item["latitude"], "longitude": item["longitude"]}
    if len(list(filter(lambda x: x["now"] < x["t"], item["control"]))) == 0:
        for control in item["control"]:
            control["now"] = 0
    for control in item["control"]:
        if control["now"] < control["t"]:
            send_object["red"] = control["red"]
            send_object["yellow"] = control["yellow"]
            send_object["green"] = control["green"]
            send_object["left"] = control["left"]
            send_object["lefttime"] = control["t"] - control["now"]
            control["now"] += pm
            break
    return send_object

now = datetime.datetime.now()

for k in base.keys():
    to  = (now - base[k]).seconds
    s = list(filter(lambda x: x["id"] == k, source))[0]
    for i in range(to):
        process(s, 1)

while True:
    result = []
    nowDate = datetime.datetime.now()
    for item in source:
        send_object = process(item, 5)
        result.append(send_object)

    data = json.dumps(result)
    print(data)
    a = r.post(url + "/traffic-control/control", json=result)
    nowDate2 = datetime.datetime.now()
    gap = datetime.timedelta(seconds=5) - (nowDate2 - nowDate)
    print(gap)
    # print(a.content)
    # print("SEND!")
    custom_sleep(gap.seconds, gap.microseconds)
