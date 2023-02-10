from abstractGM import abstractGMAlgorithm
from parser.meMap_parser import me_map
import time
import json

path = [
        'C:\\Users\\max_b\\PycharmProjects\\abstract_goal_models\\me-maps\\input''\\InternetShop.json'
     #   'me-maps\\input\\newtest1000_@T_6_364@T_6_365@T_6_366@T_6_367@T_6_368@T_6_369@T_6_370@T_6_371@T_6_372@T_6_373@T_6_374@T_6_375@T_6_376@T_6_377@T_6_378@T_6_379@T_6_380@T_6_381@T_6_382@T_6_383.json',
     #   'me-maps\\input\\newtest1500_@T_7_1093@T_7_1094@T_7_1095@T_7_1096@T_7_1097@T_7_1098@T_7_1099@T_7_1100@T_7_1101@T_7_1102@T_7_1103@T_7_1104@T_7_1105@T_7_1106@T_7_1107@T_7_1108@T_7_1109@T_7_1110@T_7_1111@T_7_1112.json',
      #  'me-maps\\input\\newtest2000_@T_7_1093@T_7_1094@T_7_1095@T_7_1096@T_7_1097@T_7_1098@T_7_1099@T_7_1100@T_7_1101@T_7_1102@T_7_1103@T_7_1104@T_7_1105@T_7_1106@T_7_1107@T_7_1108@T_7_1109@T_7_1110@T_7_1111@T_7_1112.json'
]

mandatory = [
        ['Manage Internet Shop ']
        # ['t', 'q1', 'q2', 'q8', 't6', 't7', 't8', 't11']
        # ['T_6_364','T_6_365','T_6_366','T_6_367','T_6_368','T_6_369','T_6_370','T_6_371','T_6_372','T_6_373','T_6_374','T_6_375','T_6_376','T_6_377','T_6_378','T_6_379','T_6_380','T_6_381','T_6_382','T_6_383'],
        # ['T_7_1093','T_7_1094','T_7_1095','T_7_1096','T_7_1097','T_7_1098','T_7_1099','T_7_1100','T_7_1101','T_7_1102','T_7_1103','T_7_1104','T_7_1105','T_7_1106','T_7_1107','T_7_1108','T_7_1109','T_7_1110','T_7_1111','T_7_1112'],
        # ['T_7_1093','T_7_1094','T_7_1095','T_7_1096','T_7_1097','T_7_1098','T_7_1099','T_7_1100','T_7_1101','T_7_1102','T_7_1103','T_7_1104','T_7_1105','T_7_1106','T_7_1107','T_7_1108','T_7_1109','T_7_1110','T_7_1111','T_7_1112']
]

names = ['Synthetic Map - 500',
         'Synthetic Map - 1000',
         'Synthetic Map - 1500',
         'Synthetic Map - 2000'

]


for i in range(len(mandatory)):
        start = time.time()
        graph = abstractGMAlgorithm(path=path[i], mandatory=mandatory[i], default=True)
        end = time.time()

        Ta = 0
        Qu = 0
        AB = 0
        CO = 0
        Con = 0

        me_map_graph = me_map(path[i], mandatory=mandatory[i])

        for node in me_map_graph.me_map_graph.nodes:
            if me_map_graph.nodes[node].node_type == 'Task':
                Ta += 1
            if me_map_graph.nodes[node].node_type == 'Quality':
                Qu += 1

        for edge in me_map_graph.me_map_graph.edges:
            if me_map_graph.edges[(edge[0], edge[1])].edge_type == 'AchievedBy':
                AB += 1
            if me_map_graph.edges[(edge[0], edge[1])].edge_type == 'ConsistsOf':
                CO += 1
            else:
                Con += 1

        EL = Ta + Qu + AB + CO + Con
        Dec = ( ((len(me_map_graph.me_map_graph.nodes) -  len(graph.me_map_graph.nodes))) / (len(me_map_graph.me_map_graph.nodes)))
        # Dec = (len(graph.me_map_graph.nodes) / (len(me_map_graph.me_map_graph.nodes))) * 100
        print("|name %s | TA %f | Qu %f | AB %d | CO %d | Con %d | El %d| Dec %f | Abst.(msec) %f" %
              (names[i], Ta, Qu, AB, CO, Con, EL, Dec, (end-start) * 1000))

data = {"class": "go.GraphLinksModel", "nodeDataArray": [], "linkDataArray": []}
i = -1
temp = {}
for node in graph.me_map_graph.nodes:
    node_info = {}
    node_info["category"] = me_map_graph.nodes[node].node_type
    node_info["text"] = me_map_graph.nodes[node].label
    node_info["fill"] = "#ffffff"
    node_info["stroke"] = "#000000"
    node_info["strokeWidth"] = 1
    node_info["key"] = i
    temp[node] = i
    i -= 1
    node_info["refs"] = []
    node_info["ctsx"] = []
    node_info["comment"] = "null"
    data["nodeDataArray"].append(node_info)

for edge in graph.me_map_graph.edges:
    edge_info = {}
    edge_type = me_map_graph.edges[(edge[0], edge[1])].edge_type
    if edge_type == 'ConsistsOf' or edge_type == 'AchievedBy' or edge_type == 'Association':
        edge_info["category"] = edge_type
        edge_info['text'] = edge_type
    else:
        edge_info["category"] = 'Contribution'
        edge_info['text'] = edge_type

    edge_info["routing"] = {"yb": "Normal", "oE": 1}
    edge_info["from"] = temp[edge[0]]
    edge_info["to"] = temp[edge[1]]
    edge_info["refs"] = []
    edge_info["ctsx"] = []
    edge_info["comment"] = "null"
    data["linkDataArray"].append(edge_info)


json_data = json.dumps(data)

with open("graph.json", "w") as f:
    f.write(json_data)
