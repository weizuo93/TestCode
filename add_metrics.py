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


def parse_metrics(str):
    lines = str.split("\n")
    metrics = dict()
    for line in lines:
        if line.startswith("#"):
            continue
        else:
            item = line.strip().split()                        # 使用“ ”分割metric和值
            if len(item) == 2:
                # print(item[0])
                metric_item = dict()
                metric_params = item[0].strip("}").split("{")   # 使用"{"分割metric与其后面{}中的参数列表，比如：doris_be_engine_requests_total{status="failed",type="publish"}
                metric = metric_params[0]
                if metric not in metrics.keys():
                    metrics[metric] = []
                if len(metric_params) == 2:
                    params = metric_params[1].strip().split(",")  # 使用“,”分割参数列表中的每一个参数
                    params_item = dict()
                    for param in params:
                        kv = param.strip().split("=")             # 使用“=”分割参数列表中的每一个参数的key和value
                        k = kv[0]
                        v = kv[1].strip("\"")
                        params_item[k] = v
                    metrics[metric].append(params_item)
    return metrics


def create_panel():
    panel = dict()
    panel["aliasColors"] = {}
    panel["bars"] = False
    panel["dashLength"] = 10
    panel["dashes"] = False
    panel["datasource"] = "default"
    panel["description"] = ""
    panel["fill"] = 0
    panel["fillGradient"] = 0
    panel["gridPos"] = {}
    panel["id"] = 0
    panel["legend"] = {"alignAsTable": True, "avg": False, "current": False, "max": False, "min": False,
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
    panel["xaxis"] = {"buckets": None, "mode": "time", "name": None, "show": True, "values": []}
    panel["yaxes"] = [{"decimals": None, "format": "short", "label": None, "logBase": 1, "max": None, "min": None,
                       "show": True},
                      {"decimals": None, "format": "short", "label": None, "logBase": 1, "max": None, "min": None,
                       "show": False}]
    panel["yaxis"] = {"align": False, "alignLevel": None}
    return panel


def parse_grafana_json_file(file_name, metrics):
    with open(file_name, "r") as file:
        dashboard = json.load(file)                     # 加载模板文件
        # print(json_str)
        dashboard["title"] = "dashboard-test"
        dashboard["uid"] = str(uuid.uuid1())
        rows = dashboard["panels"]

        row = dict()
        row["collapsed"] = True
        row["datasource"] = None
        row["id"] = 76                                  # 基于模板文件修改
        gridPos = dict()
        gridPos["h"] = 1
        gridPos["w"] = 24
        gridPos["x"] = 0
        gridPos["y"] = 29                                # 基于模板文件修改
        row["gridPos"] = gridPos
        row["title"] = "BE Other Metrics"
        row["type"] = "row"
        row["panels"] = []
        i = 0
        for metric in metrics:
            for metric_param in metrics[metric]:

                mod = i % 3
                div = i // 3

                s = ""
                if "path" not in metric_param.keys():
                    for key in metric_param:
                        s = s + ", " + str(key) + "=\"" + str(metric_param[key]) + "\""

                panel = copy.deepcopy(create_panel())
                panel["id"] = 200 + i                          # 基于模板文件修改,注意不能与已有的panel id重复
                panel["title"] = "[$cluster_name] " + str(metric.replace("doris_be_", "")) + s

                panel["gridPos"]["h"] = 6
                panel["gridPos"]["w"] = 8
                panel["gridPos"]["x"] = mod * 8
                panel["gridPos"]["y"] = row["gridPos"]["y"] + div * 6 + 1

                panel_targets = []
                target = dict()

                target["expr"] = str(metric) + "{job=\"$cluster_name\"" + s + "}"
                target["format"] = "time_series"
                target["intervalFactor"] = 1
                # target["legendFormat"] = "{{instance}}"
                target["refId"] = "A"
                panel_targets.append(target)
                panel["targets"] = copy.deepcopy(panel_targets)

                row["panels"].append(panel)
                i = i + 1
                if "path" in metric_param.keys():
                    break

        # row = json.dumps(row)
        # print(row)
        rows.append(row)
        # print(dashboard)
        fp = open('./result.txt', 'w')
        json.dump(dashboard, fp)
        fp.close()


if __name__ == '__main__':
    metrics = request_metrics("c3-hadoop-doris-tst-st01.bj", "8040")
    metrics = parse_metrics(metrics)
    print(metrics)

    parse_grafana_json_file("./grafana_json.txt", metrics)

