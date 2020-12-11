import requests
import json
import copy
import uuid


'''通过http接口获取BE的所有metrics信息'''
def request_metrics(host, port):
    try:
        response = requests.get(url='http://' + host + ':' + port + '/metrics')
    except:
        print('Internet Error')
    else:
        return response.text


'''通过http接口获取BE的所有metrics的单位信息'''
def request_metrics_unit(host, port):
    metrics_unit = {}
    try:
        response = requests.get(url='http://' + host + ':' + port + '/metrics?type=json')
    except:
        print('Internet Error')
    else:
        metrics = json.loads(response.text)
        for metric in metrics:

            metrics_unit["doris_be_" + metric["tags"]["metric"]] = metric["unit"]
        return metrics_unit

'''
对获取的BE metrics信息进行解析:
metric名称和参数：{metric1: [{'status': ', 'type': ''},{'status': ', 'type': ''},...], metric2: [{'device': ''},{'device': ''},...], metric2: [{'path': ''},{'path': ''},...] ...}
metric类型：     {metric1: 'counter', metric2: 'gauge', metric3: 'counter', ...}
'''
def parse_metrics(str):
    lines = str.split("\n")
    metrics = dict()
    metric_type = dict()
    for line in lines:
        if line.startswith("#"):                              # 获取注释行，用于解析metric的类型是counter还是guage
            comment = line.strip().split(" ")
            metric_type[comment[2]] = comment[3]              # 提取metric的类型信息
        else:
            item = line.strip().split()                        # 使用“ ”分割metric和值
            if len(item) == 2:
                metric_params = item[0].strip("}").split("{")  # 使用"{"分割metric与其后面{}中的参数列表，比如：doris_be_engine_requests_total{status="failed",type="publish"}
                metric = metric_params[0]                      # 获取metric名称
                if metric not in metrics.keys():               # 判断当前行的metric是否是第一次出现
                    metrics[metric] = []
                if len(metric_params) == 2:
                    params = metric_params[1].strip().split(",")  # 使用“,”分割参数列表中的每一个参数
                    params_item = dict()
                    for param in params:
                        kv = param.strip().split("=")             # 使用“=”分割参数列表中的每一个参数的key和value
                        k = kv[0]
                        v = kv[1].strip("\"")
                        params_item[k] = v
                    metrics[metric].append(params_item)           # 将参数列表添加到当前metric中
    return [metrics, metric_type]


'''创建一个grafana的panel模板'''
def create_panel_template():
    panel = dict()
    panel["aliasColors"] = {}
    panel["bars"] = False
    panel["dashLength"] = 10
    panel["dashes"] = False
    panel["datasource"] = "default"
    panel["description"] = ""
    panel["fill"] = 0
    panel["fillGradient"] = 0
    panel["gridPos"] = {}               # panel坐标：需要在创建panel时更新
    panel["id"] = 0                     # panel id：需要在创建panel时更新
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
    panel["target"] = []               # 具体的metric：需要在创建panel时更新
    panel["thresholds"] = []
    panel["timeFrom"] = None
    panel["timeShift"] = None
    panel["title"] = ""                # panel标题：需要在创建panel时更新
    panel["tooltip"] = {"shared": True, "sort": 0, "value_type": "individual"}
    panel["type"] = "graph"
    panel["xaxis"] = {"buckets": None, "mode": "time", "name": None, "show": True, "values": []}
    panel["yaxes"] = [{"decimals": None, "format": "short", "label": None, "logBase": 1, "max": None, "min": None,
                       "show": True},
                      {"decimals": None, "format": "short", "label": None, "logBase": 1, "max": None, "min": None,
                       "show": False}]
    panel["yaxis"] = {"align": False, "alignLevel": None}
    return panel


'''获取模板文件中已经存在的metrics'''
def get_exist_metrics_from_base(rows):
    exist_metrics = []
    for row in rows:
        if "panels" not in row.keys():
            targets = row["targets"]
            for target in targets:
                exist_metrics.append(target["expr"])      # 取每一个panel的target["expr"]
        else:
            panels = row["panels"]
            for panel in panels:
                targets = panel["targets"]
                for target in targets:
                    exist_metrics.append(target["expr"])  # 取每一个panel的target["expr"]
    return exist_metrics


'''添加新的panel到base文件中，所有新添加的panel组织在一个新的row中'''
def append_grafana_panel_to_base(file_name, metrics, metric_type, metrics_unit):
    with open(file_name, "r") as file:
        dashboard = json.load(file)                     # 加载base模板文件
        # print(json_str)
        dashboard["title"] = "dashboard-test"           # 设置dashboard的名称
        dashboard["uid"] = str(uuid.uuid1())            # 为dashboard设置uid
        rows = dashboard["panels"]                      # 获取base模板dashboard中的所有row
        exist_metrics = get_exist_metrics_from_base(rows)  # 统计已经在base模板dashboard中存在的metrics

        row = dict()                 # 创建一个新的row
        row["collapsed"] = True
        row["datasource"] = None
        row["id"] = 76                                  # 设置row的id，基于模板文件修改
        gridPos = dict()
        gridPos["h"] = 1
        gridPos["w"] = 24
        gridPos["x"] = 0
        gridPos["y"] = 29                                # 设置row的坐标，基于模板文件修改
        row["gridPos"] = gridPos
        row["title"] = "BE Other Metrics"                # 设置row的名称
        row["type"] = "row"                              # 设置row的类型
        row["panels"] = []                               # row["panels"]中保存row中新增的所有panel
        i = 0

        for metric in metrics:                      # 依次遍历每一个metric
            exist = False
            for exist_metric in exist_metrics:      # 判断当前metric是否在base dashboard中已经存在
                if exist_metric.find(metric) != -1:
                    exist = True
                    break
            if exist:
                continue

            for metric_param in metrics[metric]:     # 依次遍历metric中的每一个参数列表
                s = ""
                if "path" not in metric_param.keys() and "device" not in metric_param.keys():  # 判断参数列表中是否包含“path”（表示磁盘）参数，集群中同一个metric下的所有磁盘信息在同一个panel中展示
                    for key in metric_param:
                        s = s + ", " + str(key) + "=\"" + str(metric_param[key]) + "\""

                panel = copy.deepcopy(create_panel_template()) # 创建一个panel模板
                panel["id"] = 200 + i                          # 为panel设置id，基于模板文件修改,注意不能与已有的panel id重复
                panel["title"] = "[$cluster_name] " + str(metric.replace("doris_be_", "")) + s  # 为panel设置名称

                mod = i % 3    # row中每行放置3个panel
                div = i // 3
                panel["gridPos"]["h"] = 6
                panel["gridPos"]["w"] = 8
                panel["gridPos"]["x"] = mod * 8
                panel["gridPos"]["y"] = row["gridPos"]["y"] + div * 6 + 1  # 为panel设置坐标

                panel_targets = []
                target = dict()
                if metric_type[metric] == "counter":
                    target["expr"] = "rate(" + str(metric) + "{job=\"$cluster_name\"" + s + "}[$interval])"  # 为panel设置具体的metric，counter类型的metric需要计算每秒的增长量
                else:
                    target["expr"] = str(metric) + "{job=\"$cluster_name\"" + s + "}"                        # 为panel设置具体的metric，guage类型的metric直接使用metric值展示
                target["format"] = "time_series"                           # 在panel中以时间顺序呈现metric值
                target["intervalFactor"] = 1
                if "path" in metric_param.keys():
                    target["legendFormat"] = "{{instance}}:{{path}}"
                elif "device" in metric_param.keys():
                    target["legendFormat"] = "{{instance}}:{{device}}"
                else:
                    target["legendFormat"] = "{{instance}}"
                target["refId"] = "A"
                panel_targets.append(target)
                panel["targets"] = copy.deepcopy(panel_targets)

                if metrics_unit[metric] == "nanoseconds":
                    panel["yaxes"][0]["format"] = "ns"

                if metrics_unit[metric] == "microseconds":
                    panel["yaxes"][0]["format"] = "µs"

                if metrics_unit[metric] == "milliseconds":
                    panel["yaxes"][0]["format"] = "ms"

                if metrics_unit[metric] == "seconds":
                    panel["yaxes"][0]["format"] = "s"

                if metrics_unit[metric] == "bytes":
                    if metric_type[metric] == "counter":
                        panel["yaxes"][0]["format"] = "Bps"
                    else:
                        panel["yaxes"][0]["format"] = "bytes"

                if metrics_unit[metric] == "percent":
                    panel["yaxes"][0]["format"] = "percent"

                if metrics_unit[metric] == "requests":
                    if metric_type[metric] == "counter":
                        panel["yaxes"][0]["format"] = "rps"
                    else:
                        panel["yaxes"][0]["format"] = "requests"

                if metrics_unit[metric] == "operations":
                    if metric_type[metric] == "counter":
                        panel["yaxes"][0]["format"] = "ops"
                    else:
                        panel["yaxes"][0]["format"] = "ops"

                row["panels"].append(panel)
                i = i + 1
                if "path" in metric_param.keys() or "device" in metric_param.keys():
                    break

        # row = json.dumps(row)
        # print(row)
        rows.append(row)
        # print(dashboard)
        fp = open('./result.txt', 'w')
        json.dump(dashboard, fp)  # 将生成的新的dashboard的json数据保存到文件
        fp.close()


if __name__ == '__main__':
    metrics = request_metrics("c3-hadoop-doris-tst-st01.bj", "8040")
    [metrics, metric_type] = parse_metrics(metrics)
    # print(metrics)
    print(metric_type)
    metrics_unit = request_metrics_unit("c3-hadoop-doris-tst-st01.bj", "8040")
    print(metrics_unit)
    # for key in metrics_unit:
    #     print(metrics_unit[key])

    append_grafana_panel_to_base("./grafana_json.txt", metrics, metric_type, metrics_unit)

