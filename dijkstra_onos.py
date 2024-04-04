import sys
import json
import requests
import curlify
import os
import mapper
import time

class Graph(object):

    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(self, nodes, init_graph):
        graph = {}
        for node in nodes:
            graph[node] = {}
        graph.update(init_graph)
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
        return graph

    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes

    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]

odwroconalista = []

def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
    # Add the start node manually
    path.append(start_node)
    reversedlist = list(reversed(path))
    print(reversedlist)
    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed(path)))
    return reversedlist

def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
    shortest_path = {}
    previous_nodes = {}
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[start_node] = 0
    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                previous_nodes[neighbor] = current_min_node
        unvisited_nodes.remove(current_min_node)
    return previous_nodes, shortest_path

def json_extract(obj, key):
    arr = []
    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    values = extract(obj, arr, key)
    return values

def switchNameToNode(node):
    if node == "warszawa":
        node = "of:0000000000000001"
    elif node == "bialystok":
        node = "of:0000000000000002"
    elif node == "gdansk":
        node = "of:0000000000000003"
    elif node == "szczecin":
        node = "of:0000000000000004"
    elif node == "poznan":
        node = "of:0000000000000005"
    elif node == "bydgoszcz":
        node = "of:0000000000000006"
    elif node == "lodz":
        node = "of:0000000000000007"
    elif node == "krakow":
        node = "of:0000000000000008"
    elif node == "wroclaw":
        node = "of:0000000000000009"
    elif node == "rzeszow":
        node = "of:000000000000000a"
    return node

def sendRules1(lista, url, headers, username, password):
    for z in lista:
        response = requests.post(url=url, json=z, headers=headers, auth=(username, password))
        print(response.status_code)
        print(response.text)

def sendRules(flow_list, url, headers, username, password):
    payload = {"flows": flow_list}  # Ensure the "flows" key is present in the payload
    response = requests.post(url=url, json=payload, headers=headers, auth=(username, password))
    print(response.status_code)
    print(response.text)
def sendRulesAll(flow_table, url, headers, username, password):
    response = requests.post(url=url, json=flow_table, headers=headers, auth=(username, password))
    print(response.status_code)
    print(response.text)
def rulesConfiguration():
    DEVICE_INFO = "deviceInfo.json"
    map_switch_to_host=mapper.map_switch_to_host
    with open('links.json', 'r') as f:
        data = json.load(f)
        device = json_extract(data, 'device')
        print("Devices:\n---------------------------------------------------------------------------")
        print(device)
        print("---------------------------------------------------------------------------")
        print("Ports:---------------------------------------------------------------------------")
        port = json_extract(data, 'port')
        print(port)
        print("---------------------------------------------------------------------------\n\n")
        for x in range(1, len(odwroconalista) - 1):
            tab = []
            for y in range(1, len(odwroconalista) - 1):
                for m in range(0, len(device)):
                    if (odwroconalista[x] == device[m] and odwroconalista[x + 1] == device[m + 1] and m % 2 == 0):
                        for p in range(0, len(device) - 1):
                            if (odwroconalista[x] == device[p + 1] and odwroconalista[x - 1] == device[p]):
                                dictionary = {"flows": []}
                                ipA = str(map_switch_to_host(switch_id=odwroconalista[x + 1], json_file=DEVICE_INFO))
                                ipA = str(mapper.extract_ip_without_mask(ipA))
                                ipB = str(map_switch_to_host(switch_id=odwroconalista[x - 1], json_file=DEVICE_INFO))
                                ipB = str(mapper.extract_ip_without_mask(ipB))
                                a = {
                            "priority": 40000,
                            "timeout": 0,
                            "isPermanent": "true",
                            "deviceId": odwroconalista[x],
                            "treatment": {"instructions": [{"type": "OUTPUT", "port": port[m]}]},
                            "selector": {
                                "criteria": [
                                    {"type": "IN_PORT", "port": port[p + 1]},
                                    {"type": "ETH_TYPE", "ethType": "0x0800"},
                                    {"type": "IPV4_DST", "ip": ipA + "/32"}]}}

                                b = {
                                    "priority": 40000,
                                    "timeout": 0,
                                    "isPermanent": "true",
                                    "deviceId": odwroconalista[x],
                                    "treatment": {"instructions": [{"type": "OUTPUT", "port": port[p + 1]}]},
                                    "selector": {
                                        "criteria": [
                                            {"type": "IN_PORT", "port": port[m]},
                                            {"type": "ETH_TYPE", "ethType": "0x0800"},
                                            {"type": "IPV4_DST", "ip": ipB + "/32"}
                                        ]
                                    }
                                }

                                dictionary["flows"].append(a)
                                dictionary["flows"].append(b)

                                bigDictionary["flows"].append(a)
                                bigDictionary["flows"].append(b)

                                tab.append(a)
                                tab.append(b)

                                #sendRules(flow_list=tab, url=url, headers=headers, username=username, password=password)
                                sendRulesAll(flow_table=bigDictionary, url=url, headers=headers, username=username, password=password)

                                tab.clear()
                                dictionary.clear()
                                
        for d in range(0, len(device)):
            if (odwroconalista[0] == device[d] and odwroconalista[1] == device[d + 1]):
                for k in range(0, len(device) - 1):
                    if (odwroconalista[-1] == device[k + 1] and odwroconalista[-2] == device[k]):
                        ipE = str(map_switch_to_host(switch_id=device[d + 1], json_file=DEVICE_INFO))
                        ipF = str(map_switch_to_host(switch_id=device[d], json_file=DEVICE_INFO))
                        ipG = str(map_switch_to_host(switch_id=device[k + 1], json_file=DEVICE_INFO))
                        ipH = str(map_switch_to_host(switch_id=device[k + 1], json_file=DEVICE_INFO))
                        ipI = str(map_switch_to_host(switch_id=device[k], json_file=DEVICE_INFO))
                        ipJ = str(map_switch_to_host(switch_id=device[d], json_file=DEVICE_INFO))
                        
                        ipE = str(mapper.extract_ip_without_mask(ipE))
                        ipF = str(mapper.extract_ip_without_mask(ipF))
                        ipG = str(mapper.extract_ip_without_mask(ipG))
                        ipH = str(mapper.extract_ip_without_mask(ipH))
                        ipI = str(mapper.extract_ip_without_mask(ipI))
                        ipJ = str(mapper.extract_ip_without_mask(ipJ))
                        
                        e = {"priority": 40000, "timeout": 0, "isPermanent": "true", "deviceId": odwroconalista[0],
                             "treatment": {"instructions": [{"type": "OUTPUT", "port": port[d]}]}, "selector": {
                                "criteria": [{"type": "IN_PORT", "port": "1"},
                                             {"type": "ETH_TYPE", "ethType": "0x0800"},
                                             {"type": "IPV4_DST", "ip": ipE + "/32"}]}}
                        f = {"priority": 40000, "timeout": 0, "isPermanent": "true", "deviceId": odwroconalista[0],
                             "treatment": {"instructions": [{"type": "OUTPUT", "port": "1"}]}, "selector": {
                                "criteria": [{"type": "IN_PORT", "port": port[d]},
                                             {"type": "ETH_TYPE", "ethType": "0x0800"},
                                             {"type": "IPV4_DST", "ip": ipF + "/32"}]}}
                        g = {"priority": 40000, "timeout": 0, "isPermanent": "true", "deviceId": odwroconalista[0],
                             "treatment": {"instructions": [{"type": "OUTPUT", "port": port[d]}]}, "selector": {
                                "criteria": [{"type": "IN_PORT", "port": "1"},
                                             {"type": "ETH_TYPE", "ethType": "0x0800"},
                                             {"type": "IPV4_DST", "ip": ipG + "/32"}]}}
                        h = {"priority": 40000, "timeout": 0, "isPermanent": "true", "deviceId": odwroconalista[-1],
                             "treatment": {"instructions": [{"type": "OUTPUT", "port": "1"}]}, "selector": {
                                "criteria": [{"type": "IN_PORT", "port": port[k + 1]},
                                             {"type": "ETH_TYPE", "ethType": "0x0800"},
                                             {"type": "IPV4_DST", "ip": ipH + "/32"}]}}
                        i = {"priority": 40000, "timeout": 0, "isPermanent": "true", "deviceId": odwroconalista[-1],
                             "treatment": {"instructions": [{"type": "OUTPUT", "port": port[k + 1]}]}, "selector": {
                                "criteria": [{"type": "IN_PORT", "port": "1"},
                                             {"type": "ETH_TYPE", "ethType": "0x0800"},
                                             {"type": "IPV4_DST", "ip": ipI + "/32"}]}}
                        j = {"priority": 40000, "timeout": 0, "isPermanent": "true", "deviceId": odwroconalista[-1],
                             "treatment": {"instructions": [{"type": "OUTPUT", "port": port[k + 1]}]}, "selector": {
                                "criteria": [{"type": "IN_PORT", "port": "1"},
                                             {"type": "ETH_TYPE", "ethType": "0x0800"},
                                             {"type": "IPV4_DST", "ip": ipJ + "/32"}]}}
                        dictionary1["flows"].append(e)
                        dictionary1["flows"].append(f)
                        dictionary1["flows"].append(g)
                        dictionary2["flows"].append(h)
                        dictionary2["flows"].append(i)
                        dictionary2["flows"].append(j)
                        val1.append(e)
                        val1.append(f)
                        val1.append(g)
                        val2.append(h)
                        val2.append(i)
                        val2.append(j)
                        bigDictionary["flows"].append(e)
                        bigDictionary["flows"].append(f)
                        bigDictionary["flows"].append(g)
                        bigDictionary["flows"].append(h)
                        bigDictionary["flows"].append(i)
                        bigDictionary["flows"].append(j)
                        #urL2 = f"http://{host}:{portX}/onos/v1/flows/" + "of:000000000000000" + odwroconalista[-1][-1]
                        #urL1 = f"http://{host}:{portX}/onos/v1/flows/" + "of:000000000000000" + odwroconalista[0][-1]
                        urL1 = f"http://{host}:{portX}/onos/v1/flows/of%3A" + odwroconalista[-1].split(":")[1]
                        urL2 = f"http://{host}:{portX}/onos/v1/flows/of%3A"+ odwroconalista[0].split(":")[1]
                        #for i in range(len(val1)):
                       # 	sendRules(flow_list=val1[i], url=urL1, headers=headers, username=username, password=password)
                       # 	sendRules(flow_list=val2[i], url=urL2, headers=headers, username=username, password=password)
                        sendRulesAll(flow_table=bigDictionary, url=url, headers=headers, username=username, password=password)
                        



if __name__=="__main__":

    nodes=mapper.getNodesFromJson("devices.json")
    print("Nodes:\n{}".format(nodes))
    
    
    init_graph = {}
    for node in nodes:
        init_graph[node] = {}

    init_graph["of:0000000000000001"]["of:0000000000000002"] = 1.41  # Warszawa-Bialystok
    init_graph["of:0000000000000001"]["of:0000000000000003"] = 2.40  # Warszawa-Gdansk
    init_graph["of:0000000000000003"]["of:0000000000000004"] = 2.55  # Gdansk-Szczecin
    init_graph["of:0000000000000001"]["of:0000000000000005"] = 2.20  # Warszawa-Poznan
    init_graph["of:0000000000000005"]["of:0000000000000006"] = 0.98  # Poznan-Bydgoszcz
    init_graph["of:0000000000000001"]["of:0000000000000007"] = 0.96  # Warszawa-Lodz
    init_graph["of:0000000000000001"]["of:0000000000000008"] = 2.05  # Warszawa-Krakow
    init_graph["of:0000000000000008"]["of:0000000000000009"] = 1.91  # Krakow-Wroclaw
    init_graph["of:0000000000000008"]["of:000000000000000a"] = 1.18  # Krakow-Rzeszow

    init_graph["of:0000000000000001"]["of:000000000000000a"] = 2.33  # Warszawa-Rzeszow 330km
    init_graph["of:0000000000000001"]["of:0000000000000006"] = 2.13  # Warszawa-Bydgoszcz 302km
    init_graph["of:0000000000000007"]["of:0000000000000008"] = 1.97  # Lodz-Krakow 280 km
    init_graph["of:0000000000000007"]["of:0000000000000009"] = 1.56  # Lodz-Wroclaw 221km
    init_graph["of:0000000000000007"]["of:0000000000000005"] = 1.50  # Lodz-Poznan 212km
    init_graph["of:0000000000000005"]["of:0000000000000009"] = 1.29  # Poznan-Wroclaw 183km
    init_graph["of:0000000000000005"]["of:0000000000000004"] = 1.88  # Poznan-Szczecin 266km
    init_graph["of:0000000000000004"]["of:0000000000000009"] = 2.94  # Szczecin-Wroclaw 416km
    init_graph["of:0000000000000004"]["of:0000000000000006"] = 1.83  # Szczecin-Bydgoszcz 259km
    init_graph["of:0000000000000002"]["of:000000000000000a"] = 3.41  # Bialystok-Rzeszow 482km
    init_graph["of:0000000000000003"]["of:0000000000000002"] = 2.76  # Gdansk-Bialystok 391km
    init_graph["of:0000000000000003"]["of:0000000000000006"] = 1.18  # Gdansk-Bydgoszcz 167km
    graph = Graph(nodes, init_graph)

    host = "localhost"
    portX = "8181"
    username = "onos"
    password = "rocks"
    url = f"http://{host}:{portX}/onos/v1/flows"
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    start_node = input(str("Type start_node:"))
    target_node = input(str("Type target_node:"))
    start_node = switchNameToNode(start_node)
    target_node = switchNameToNode(target_node)

    previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=start_node)
    odwroconalista = print_result(previous_nodes, shortest_path, start_node=start_node, target_node=target_node)
    print(odwroconalista)

    bigDictionary = {"flows":[]}

    dictionary1 = {"flows": []}
    dictionary2 = {"flows": []}
    val1=[]
    val2=[]
    listContainingJsonRequests = []

    prefixIP="192.168.0."
    
   # mapper.run(odwroconalista)
    time.sleep(1)
    
    rulesConfiguration()
