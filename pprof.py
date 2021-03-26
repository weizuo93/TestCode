import os
import time
import _thread


def pprof(machine, ip):
    while True:
        localtime = time.strftime("%Y-%m-%d.%H:%M:%S", time.localtime())
        cmd = "pprof --text --seconds=30 http://" + ip + ":8040/pprof/heap > data_" + machine + "/" + machine + ".mem." + str(localtime)
        os.system(cmd)


if __name__ == '__main__':
    host = dict()
    host["sgp2_be01"] = ""
    host["sgp2_be02"] = ""
    host["sgp2_be03"] = ""
    host["sgp2_be05"] = ""
    host["sgp2_be10"] = ""
    host["sgp2_be11"] = ""
    host["sgp2_be12"] = ""
    host["sgp2_be13"] = ""
    host["sgp2_be14"] = ""
    host["sgp2_be15"] = ""
    host["sgp2_be16"] = ""
    host["sgp2_be17"] = ""
    host["sgp2_be18"] = ""
    host["sgp2_be19"] = ""
    host["sgp2_be20"] = ""
    host["sgp3_be12"] = ""
    host["sgp3_be13"] = ""
    host["sgp3_be14"] = ""

    try:
        # _thread.start_new_thread(pprof, ("sgp2_be01", host["sgp2_be01"],))
        # _thread.start_new_thread(pprof, ("sgp2_be02", host["sgp2_be02"],))
        # _thread.start_new_thread(pprof, ("sgp2_be03", host["sgp2_be03"],))
        # _thread.start_new_thread(pprof, ("sgp2_be05", host["sgp2_be05"],))
        # _thread.start_new_thread(pprof, ("sgp2_be10", host["sgp2_be10"],))
        # _thread.start_new_thread(pprof, ("sgp2_be11", host["sgp2_be11"],))
        # _thread.start_new_thread(pprof, ("sgp2_be12", host["sgp2_be12"],))
        # _thread.start_new_thread(pprof, ("sgp2_be13", host["sgp2_be13"],))
        # _thread.start_new_thread(pprof, ("sgp2_be14", host["sgp2_be14"],))
        # _thread.start_new_thread(pprof, ("sgp2_be15", host["sgp2_be15"],))
        _thread.start_new_thread(pprof, ("sgp2_be16", host["sgp2_be16"],))
        _thread.start_new_thread(pprof, ("sgp2_be17", host["sgp2_be17"],))
        _thread.start_new_thread(pprof, ("sgp2_be18", host["sgp2_be18"],))
        _thread.start_new_thread(pprof, ("sgp2_be19", host["sgp2_be19"],))
        _thread.start_new_thread(pprof, ("sgp2_be20", host["sgp2_be20"],))
        _thread.start_new_thread(pprof, ("sgp3_be12", host["sgp3_be12"],))
        _thread.start_new_thread(pprof, ("sgp3_be13", host["sgp3_be13"],))
        _thread.start_new_thread(pprof, ("sgp3_be14", host["sgp3_be14"],))
    except:
        print()

    while True:
        pass
