import csv
import json
import linecache
import sys
import time

import requests

try:
    s = open("debugging", 'w')
    DO_DOWNLOAD = False
    ###Debugging Statement - remove in final testing
    sys.argv.append("2000")
    ###Data Collection from the Server
    s.write(str(sys.argv))
    sys.argv.remove(sys.argv[0])
    hours = int(sys.argv[0]) / 10
    DO_DOWNLOAD = int(sys.argv[0]) % 2
    # print("opening")
    data = None
    if DO_DOWNLOAD:
        data = open("data.csv", "w", newline='')
    else:
        data = open('data.csv', 'r')
    s.write("start")
    f = open("downloaded.csv", "w", newline='')
    # print("opened")
    res = 1
    res = []
    if DO_DOWNLOAD:
        res = requests.get(url="https://completewemosproject.mybluemix.net/testing")
        # data.write(res.text)
    else:
        doneWonce = 0
        for d in data.readlines():
            mydict = {"timestamp": d.split(",")[0], "t": d.split(",")[1], "h": d.split(",")[2], "l": d.split(",")[3]}
            res.append(mydict)
            if (doneWonce < 10):
                print(mydict)
            doneWonce = doneWonce + 1
    w = csv.writer(f)
    outputList = []
    # print("requested")
    # startTime = int(sys.argv[0])
    currTime = int(round(time.time() * 1000))
    startTime = currTime - hours * 3600000
    # print('timing')
    if DO_DOWNLOAD and str(res) == "<Response [200]>":
        wr = csv.writer(data)
        res = json.loads(res.text)
        # print(res)
        for d in res:
            wr.writerow(
                [d["timestamp"]] + [d["payload"]["d"]["t"]] + [d["payload"]["d"]["h"]] + [d["payload"]["d"]["l"]])
            if d["timestamp"] > startTime:
                d["timestamp"] = hours - (((currTime - d["timestamp"]) / 3600000))
                w.writerow(
                    [d["timestamp"]] + [d["payload"]["d"]["t"]] + [d["payload"]["d"]["h"]] + [d["payload"]["d"]["l"]])
    elif not DO_DOWNLOAD:
        doneWonce = 0
        for d in res:
            if int(d["timestamp"]) > startTime:
                w.writerow(
                    [hours - (((currTime - int(d["timestamp"])) / 3600000))] + [d["t"]] + [d["h"]] + [d["l"].strip()])
                if (doneWonce < 10):
                    print([d["timestamp"]] + [d["t"]] + [d["h"]] + [d["l"].strip()])
                doneWonce += 1
    else:
        # print(res)
        s.write("res")
        exit()

    # Formatting/interpretting data
    # print(len(d))
    s.write("done")
except:
    s.write(str(sys.exc_info()))
    exc_type, exc_obj, tb = sys.exc_info()
    ls = tb.tb_frame
    lineno = tb.tb_lineno
    filename = ls.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, ls.f_globals)
    s.write("\n")
    s.write('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    s.write("\n")
    s.write(str(res))
    s.close()
    data.close()
    f.close()
finally:
    s.close()
    f.close()
    data.close()
