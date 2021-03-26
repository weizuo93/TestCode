import os
import time

while True:
    localtime = time.strftime("%Y-%m-%d.%H:%M:%S", time.localtime())
    print(localtime)

    cmd = "pprof --text --seconds=30 http://localhost:8040/pprof/heap > mem." + str(localtime)
    os.system(cmd)

    time.sleep(5)
    