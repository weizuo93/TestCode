import requests
import json
import copy
import uuid


def request_metrics(host, port):
    try:
        response = requests.get(url='http://' + host + ':' + port + '/metrics')
    except:
        print('Internet Error')
    else:
        return response.text


def parase_metrics(str):
    lines = str.split("\n")
    metrics = {}
    for line in lines:
        if line.startswith("#"):
            continue
        else:
            item = line.strip().split()
            if len(item) == 2:
                metrics[item[0]] = item[1]
    return metrics


def create_panel():
    panel = {}
    panel["aliasColors"] = {}
    panel["bars"] = False
    panel["dashLength"] = 10
    panel["dashes"] = False
    panel["datasource"] = "default"
    panel["description"] = ""
    panel["fill"] = 0
    panel["gridPos"] = {}
    panel["id"] = 0
    panel["legend"] = {"alignAsTable": True, "avg": False, "current": True, "max": False, "min": False,
                       "rightSide": False, "show": True, "total": False, "values": False}
    panel["lines"] = True
    panel["linewidth"] = 1
    panel["links"] = []
    panel["nullPointMode"] = None
    panel["percentage"] = False
    panel["pointradius"] = 5
    panel["points"] = False
    panel["renderer"] = "flot"
    panel["seriesOverrides"] = [{"alias": "Failed", "yaxis": 2}, {"alias": "Total", "yaxis": 2}]
    panel["spaceLength"] = 10
    panel["stack"] = False
    panel["steppedLine"] = False
    panel["target"] = []
    panel["thresholds"] = []
    panel["timeFrom"] = None
    panel["timeShift"] = None
    panel["title"] = ""
    panel["tooltip"] = {"shared": True, "sort": 0, "value_type": "individual"}
    panel["type"] = "graph"
    panel["xaxis"] = {"buckets": None, "mode": "time", "name": None, "show": None, "values": []}
    panel["yaxes"] = [{"decimals": None, "format": "short", "label": None, "logBase": 1, "max": None, "min": "0",
                       "show": True},
                      {"decimals": 0, "format": "short", "label": None, "logBase": 1, "max": None, "min": None,
                       "show": True}]
    panel["yaxis"] = {"align": False, "alignLevel": None}
    return panel


def parase_grafana_json_file(file_name, metrics):
    with open(file_name, "r") as file:
        dashboard = json.load(file)
        # print(json_str)
        dashboard["title"] = "generate-dashboard-test"
        dashboard["uid"] = str(uuid.uuid1())
        rows = dashboard["panels"]
        # for row in rows:
        #     print(row["title"])

        row = {}
        row["collapsed"] = True
        row["datasource"] = None
        row["id"] = 76
        gridPos = {}
        gridPos["h"] = 1
        gridPos["w"] = 24
        gridPos["x"] = 0
        gridPos["y"] = 29
        row["gridPos"] = gridPos
        row["title"] = "New Metrics Panel"
        row["type"] = "row"
        row["panels"] = []
        i = 0
        for key in metrics:
            mod = i % 3
            div = i // 3
            met = str(key)
            item = met.strip().split("{")
            print(item)

            panel = copy.deepcopy(create_panel())
            panel["id"] = 100 + i
            panel["title"] = "[$cluster_name] " + str(item[0])

            panel["gridPos"]["h"] = 6
            panel["gridPos"]["w"] = 8
            panel["gridPos"]["x"] = mod * 8
            panel["gridPos"]["y"] = row["gridPos"]["y"] + div * 6 + 1

            panel_targets = []
            target = {}
            target["expr"] = str(item[0]) + "{job=\"$cluster_name\"}"
            target["format"] = "time_series"
            target["intervalFactor"] = 1
            target["legendFormat"] = "{{instance}}"
            target["refId"] = "A"
            panel_targets.append(target)
            panel["targets"] = copy.deepcopy(panel_targets)

            row["panels"].append(panel)
            # print(row["panels"])
            i = i + 1

        # row = json.dumps(row)
        # print(row)
        rows.append(row)
        # print(dashboard)
        fp = open('./result.txt', 'w')
        json.dump(dashboard, fp)
        fp.close()


if __name__ == '__main__':
    metrics = request_metrics("c3-hadoop-doris-tst-st01.bj", "8040")
    # print(metrics)
    metrics = parase_metrics(metrics)
    # for key in metrics:
    #     print(str(key) + " : " + str(metrics[key]))

    parase_grafana_json_file("./grafana_json.txt", metrics)

