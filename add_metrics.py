import requests
import json
import copy


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


def parase_grafana_json_file(file_name, metrics):
    with open(file_name, "r") as file:
        json_str = json.load(file)
        # print(json_str)
        rows = json_str["panels"]
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
                if rows[len(rows) - 1]["panels"] != None and rows[len(rows) - 1]["panels"][0] != None:
                    panel = copy.deepcopy(rows[len(rows) - 1]["panels"][0])
                    mod = i % 3
                    div = i // 3
                    panel["gridPos"]["h"] = 6
                    panel["gridPos"]["w"] = 8
                    panel["gridPos"]["x"] = mod * 8
                    panel["gridPos"]["y"] = row["gridPos"]["y"] + div * 6 + 1
                    row["panels"].append(panel)
                    # print(row["panels"])
                i = i + 1

        row = json.dumps(row)
        print(row)
        rows.append(row)



if __name__ == '__main__':
    metrics = request_metrics("c3-hadoop-doris-tst-st01.bj", "8040")
    # print(metrics)
    metrics = parase_metrics(metrics)
    # for key in metrics:
    #     print(str(key) + " : " + str(metrics[key]))

    parase_grafana_json_file("./grafana_json.txt", metrics)

