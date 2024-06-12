import networkx as nx

from parser.meMap_parser import me_map
from algorithms.inducedSubmodel import induced_subModel
from algorithms.propMand import propMandAlgorithm
from algorithms.absAbCo import absAbCoAlgorithm
from parser.quality_graph import quality_map
from parser.task_graph import tasks_map

from collections import defaultdict, deque

from components.edge import edge as ed


def min_edge(label_1=None, label_2=None):
    """

    :param label_1:
    :param label_2:
    :return:
    """
    if label_1 == '--' and label_2 == '--':
        return '++'
    if (label_1 == '-' and label_2 == '--') or (label_1 == '--' and label_2 == '-'):
        return '+'
    if label_1 == '--' or label_2 == '--':
        return '--'
    if label_1 == '-' or label_2 == '-':
        return '-'
    if label_1 == '+' or label_2 == '++':
        return '+'
    else:
        '++'


def add_task_edges(quality_graph=None, task_graph=None):
    """

    :param quality_graph:
    :param task_graph:
    :return:
    """
    for node in task_graph.me_map_graph.nodes:
        quality_graph.me_map_graph.add_node(node)

    for edge in task_graph.me_map_graph.edges:
        if task_graph.edges[edge].edge_type != 'AchievedBy' and task_graph.edges[edge].edge_type != 'ConsistsOf':
            quality_graph.me_map_graph.add_edge(edge[0], edge[1])
            quality_graph.edges[(edge[0], edge[1])] = task_graph.edges[(edge[0], edge[1])]


# A recursive function used by topological_sort
def topological_sort_util(graph, v, visited, stack):
    # Mark the current node as visited.
    visited[v] = True

    # Recur for all the vertices adjacent to this vertex
    for i in list(graph.me_map_graph.adj[v].keys()):
        if not visited[i]:
            topological_sort_util(graph, i, visited, stack)

    # Push current vertex to stack which stores the result
    stack.append(v)


# The function to do Topological Sort. It uses recursive
# topological_sort_util()

def topological_sort(graph):
    # Mark all the vertices as not visited
    visited = {}
    for i in list(graph.nodes.keys()):
        visited[i] = False
    # visited = [False] * len(list(graph.nodes.keys()))
    stack = []

    # Call the recursive helper function to store Topological
    # Sort starting from all vertices one by one
    for i in list(graph.nodes.keys()):
        if not visited[i]:
            topological_sort_util(graph, i, visited, stack)

    # Return contents of stack in reverse order
    return stack[::-1]


def topological_sort_dfs(graph, start_vertex):
    visited = set()
    stack = []

    def dfs(vertex):
        visited.add(vertex)
        for neighbor in list(graph.me_map_graph.adj[start_vertex].keys()):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(vertex)

    dfs(start_vertex)
    return stack[::-1]


def collect_reachable_vertices(graph, start_vertex):
    visited = set()
    reachable = []

    def dfs(vertex):
        visited.add(vertex)
        for neighbor in list(graph.me_map_graph.adj[start_vertex].keys()):
            if neighbor not in visited:
                dfs(neighbor)
        reachable.append(vertex)

    dfs(start_vertex)
    return reachable


def collect_reachable_edges(graph, start_vertex):
    visited = set()
    reachable_edges = []

    def dfs(vertex):
        visited.add(vertex)
        for neighbor in list(graph.me_map_graph.adj[vertex].keys()):
            reachable_edges.append((vertex, neighbor))
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start_vertex)
    output = []
    for edge in reachable_edges:
        if start_vertex == edge[0]:
            output.append(edge)
    return output


# Function to perform topological sort on a subgraph
def topological_sort_edges(graph, edges):
    # Create an in-degree dictionary for the edges
    in_degree = defaultdict(int)
    adj_list = defaultdict(list)

    for u, v in edges:
        adj_list[u].append(v)
        in_degree[v] += 1

    # Queue for nodes with no incoming edges
    queue = deque([u for u in graph.nodes if in_degree[u] == 0])
    topo_sort = []

    while queue:
        u = queue.popleft()
        for v in adj_list[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
        topo_sort.append(u)

    # Collect the sorted edges
    sorted_edges = []
    for u in topo_sort:
        for v in adj_list[u]:
            sorted_edges.append((u, v))

    return sorted_edges


def abstractContLinksAlgorithm(graph=None, default=True):
    """

    :param default:
    :param graph:
    :return:
    """

    tasks_nodes = []
    stack = topological_sort(graph)
    dSr = {}

    for e in graph.edges:
        dSr[graph.edges[e]] = {graph.edges[e]}

    while len(stack) > 0:
        # step 1
        Eseed = {}
        v_i = stack.pop()
        reachable_edges = collect_reachable_edges(graph, v_i)
        out_vi = topological_sort_edges(graph, reachable_edges)
        Eseed = process_edges(graph, out_vi, Eseed, dSr)
        if len(Eseed) == 0:
            continue
        # step 2
        seed_vi = topological_sort_edges(graph, Eseed)
        Eseed = process_edges(graph, seed_vi, Eseed, dSr, flag_eseed=True)
        # step 3
        for edge in Eseed:
            graph.me_map_graph.add_edge(edge[0], edge[1])
            graph.edges[edge[0], edge[1]] = ed(from_node=edge[0], to_node=edge[1],
                                               edge_type=Eseed[(edge[0], edge[1])].edge_type)
            removeRedNodes(v_i, graph)


def process_edges(graph, edges, Eseed, dSr, flag_eseed=False):
    for edge in edges:
        seed = calc_seed(graph, edge, Eseed, dSr, flag_eseed=flag_eseed)
        # seed = calc_seed(graph, edge, Eseed, dSr)
        Eseed.update(seed)
        if not flag_eseed:
            graph.edges[edge].is_visited = True
    return Eseed


def calc_seed(graph, e_s, Eseed, dSr, flag_eseed):
    v_s = e_s[0]
    v_m = e_s[1]
    if not flag_eseed:
        l_s = graph.edges[e_s].edge_type
    if flag_eseed:
        l_s = Eseed[(v_s, v_m)].edge_type

    reachable_edges = collect_reachable_edges(graph, v_m)
    out_vm = topological_sort_edges(graph, reachable_edges)

    for e_t in out_vm:
        # step 1
        v_t = e_t[1]
        # if not flag_eseed:
        #     l_t = graph.edges[e_t].edge_type
        # if flag_eseed:
        #     l_t = Eseed[e_t].edge_type
        try:
            l_t = graph.edges[e_t].edge_type
        except:
            l_t = Eseed[e_t].edge_type
        l = min_edge(l_s, l_t)
        e_st_c_i = ed(v_s, v_t, l)
        if not flag_eseed:
            dSr[e_st_c_i] = [graph.edges[e_s], graph.edges[e_t]]
        else:
            dSr[e_st_c_i] = [Eseed[e_s], graph.edges[e_t]]
        # step 2
        Sr_up = [e_st_c_i]
        flag = False
        if (v_s, v_t) in graph.me_map_graph.edges:
            flag = True
            Sr_up.append(graph.edges[(v_s, v_t)])
        # step 3
        update = True
        if (v_s, v_t) in Eseed:
            e_prev_st = Eseed[(v_s, v_t)]
            Sr_prev = dSr[e_prev_st]
            if deep_subset(Sr_1=Sr_up, Sr_2=Sr_prev, dSr=dSr):
                update = False
            else:
                if flag:
                    Sr_prev = list(set(dSr[e_prev_st]) - set([graph.edges[(v_s, v_t)]]))
                Sr_up = deep_union(Sr_up, Sr_prev, dSr)

        # step 4
        if update:
            e = crEdge(v_s, v_t, Sr_up, dSr)
            # Eseed.remove((v_s, v_t))
            if (v_s, v_t) in list(Eseed.keys()):
                Eseed.pop((v_s, v_t))
            Eseed[(v_s, v_t)] = e

    return Eseed

def removeRedNodes(vi, G):
    edges = []
    to_remove = []
    for edge in G.edges:
        if edge[0] == vi and G.nodes[edge[1]].node_label_type == 'R':
            edges.append(edge)
    for edge in edges:
        ongoing = []
        for edge_og in G.edges:
            if edge[1] == edge_og[1]:
                ongoing.append(edge_og)
        flag = True
        for ed_1 in ongoing:
            if not G.edges[ed_1].is_visited:
                flag = False
        if flag:
            to_remove.append(edge)
    for edge in to_remove:
        try:
            G.me_map_graph.remove_node(int(edge[1]))
        except:
            continue


def updateLabel(all_types):
    """

    :return:
    """

    score = 0
    for edge_type in all_types:
        if edge_type == '++':
            score += 90
        if edge_type == '+':
            score += 70
        if edge_type == '-':
            score += 50
        if edge_type == '--':
            score += 20

    tot = score / len(all_types)

    if tot > 90:
        return '++'
    elif tot > 60:
        return '+'
    elif tot > 40:
        return '-'
    else:
        return '--'


def crEdge(v_s, v_t, sources, dSr):
    lb = []
    for e_i in sources:
        lb.append(e_i.edge_type)
    l = updateLabel(lb)
    e_st_i = ed(v_s, v_t, l)
    dSr[e_st_i] = sources

    return e_st_i


def flattenSuperSet(alpha, dSr):
    output = []
    stack = []
    for item in dSr[alpha]:
        stack.append(item)

    while len(stack) > 0:
        item = stack.pop(0)
        output.append(item)
        try:
            for it in dSr[item]:
                if it not in output:
                    stack.append(it)
        except:
            continue

    out = []
    for item in output:
        out.append((item.from_node, item.to_node))

    return out

def deep_union(Sr_new, Sr_pc, dSr):
    Sr_nr = []
    for sn in Sr_new:
        if deep_subset([sn], Sr_pc, dSr):
            Sr_nr.append(sn)
    Sr_new = list(set(Sr_new) - set(Sr_nr))

    Sr_cr = []
    for sc in Sr_pc:
        if deep_subset([sc], Sr_new, dSr):
            Sr_cr.append(sc)

    Sr_pc = list(set(Sr_pc) - set(Sr_cr))

    return list(set(Sr_pc) | set(Sr_new) | (set(Sr_nr) & set(Sr_cr)))

def deep_subset(Sr_1, Sr_2, dSr):
    for alpha in Sr_1:
        fSS_Sr1 = flattenSuperSet(alpha, dSr)

        for beta in Sr_2:
            fSS_Sr2 = flattenSuperSet(beta, dSr)
            for item in fSS_Sr1:
                if item not in fSS_Sr2:
                    return False

    return True
    # for key in graph.me_map_graph.nodes:
    #     if graph.nodes[key].node_type == 'Task' and len(graph.me_map_graph.out_edges(key)) > 0:
    #         # print(graph.me_map_graph.out_edges(key))
    #         tasks_nodes.append(key)
    # # tasks_nodes = [-8]
    # while len(tasks_nodes) > 0:
    #     # print('======================')
    #     # print("task nodes" + str(tasks_nodes))
    #     t_i = tasks_nodes.pop()
    #     # print("t_i" + str(t_i))
    #     outgoing_edges_main = graph.me_map_graph.out_edges(t_i)
    #
    #     for outgoing_edge_main in outgoing_edges_main:
    #
    #         if graph.edges[(outgoing_edge_main[0], outgoing_edge_main[1])].is_visited:
    #             continue
    #         if graph.edges[(outgoing_edge_main[0], outgoing_edge_main[1])].edge_type == 'Association':
    #             continue
    #
    #         t_j = outgoing_edge_main[1]
    #         label = graph.edges[(t_i, t_j)].edge_type
    #         graph.edges[(t_i, t_j)].is_visited = True
    #
    #         visited_incoming_edges = True
    #         incoming_edges = graph.me_map_graph.in_edges(t_j)
    #
    #         # print(f't_j {t_j}')
    #         # print(f'incoming_edges of t_j {incoming_edges}')
    #
    #         for incoming_edge_1 in list(incoming_edges):
    #             if not graph.edges[(incoming_edge_1[0], incoming_edge_1[1])]:
    #                 visited_incoming_edges = False
    #         if visited_incoming_edges:
    #             tasks_nodes.append(t_j)
    #
    #         incoming_edges_start_node = list(graph.me_map_graph.in_edges(t_i))
    #         print(f'incoming_edges of t_i {incoming_edges_start_node}')
    #         while len(list(incoming_edges_start_node)) > 0:
    #             t_h = incoming_edges_start_node.pop()[0]
    #             l = min_edge(label, graph.edges[(t_h, t_i)].edge_type)
    #
    #             if (t_h, t_j) not in graph.me_map_graph.edges:
    #                 graph.me_map_graph.add_edge(t_h, t_j)
    #                 graph.edges[t_h, t_j] = ed(from_node=t_h, to_node=t_j, edge_type=l)
    #                 graph.edges[t_h, t_j].all_types.append(label)
    #                 # print('edge', str((t_h, t_j)), 'added')
    #             else:
    #                 graph.edges[t_h, t_j].all_types.append(l)
    #
    #             graph.edges[t_h, t_j].updateLabel()
    #
    # for node in list(graph.me_map_graph.nodes):
    #     if default:
    #         has_association = False
    #
    #         if graph.nodes[node].node_label_type == 'M':
    #             continue
    #
    #         for edge in graph.me_map_graph.in_edges(node):
    #             if graph.edges[(edge[0], edge[1])].edge_type == 'Association':
    #                 has_association = True
    #                 break
    #         for edge in graph.me_map_graph.out_edges(node):
    #             if graph.edges[(edge[0], edge[1])].edge_type == 'Association':
    #                 has_association = True
    #                 break
    #         if not has_association:
    #             if graph.nodes[node].node_label_type == 'R':
    #                 graph.me_map_graph.remove_node(node)
    #     else:
    #         if graph.nodes[node].node_label_type == 'R':
    #             graph.me_map_graph.remove_node(node)


def run():
    path = 'C:\\Users\\max_b\\PycharmProjects\\abstract_goal_models\\me-maps\\2_example.json'
    mandatory = ['t6', 'q1']
    me_map_1 = me_map(path, mandatory=mandatory)
    induced_subModel(me_map_1)
    task_graph = tasks_map(me_map_1)
    propMandAlgorithm(graph=task_graph, start_node=task_graph.nodes[-1])
    for key in task_graph.nodes:
        task_graph.nodes[key].is_visited = False
    absAbCoAlgorithm(graph=task_graph, start_node=-1)
    for node in task_graph.nodes.keys():
        if task_graph.nodes[node].node_label_type == 'R' and task_graph.nodes[node].node_type == 'Task':
            try:
                task_graph.me_map_graph.remove_node(node)
            except nx.exception.NetworkXError:
                continue

    me_map_2 = me_map(path, mandatory=mandatory)
    quality_graph = quality_map(complete_graph=me_map_2, task_graph=task_graph)

    for key in quality_graph.nodes:
        quality_graph.nodes[key].is_visited = False

    abstractContLinksAlgorithm(graph=quality_graph)


if __name__ == '__main__':
    run()
