from queue import PriorityQueue
class Node:
  def __init__(self, node_id, value=0):
    self.id = node_id
    self.value = value
    self.edges = {} 

  def add_edge(self, other_node_id, distance=0):
    self.edges[other_node_id] = distance

class Graph:

  def __init__(self, graph_id):
    self.graph_id = graph_id
    self.nodes = {}
    self.visited = []

  def add_node(self, node):
    self.nodes[node.id] = node

  """
  def add_edge(self, node_id_1, node_id_2, weight):
    self.nodes[node_id_1].add_edge(node_id_2, weight)
    self.nodes[node_id_2].add_edge(node_id_1, weight)
  """

  def dijkstra(self, start_vertex):
    D = {node_id:float('inf') for node_id in self.nodes.keys()}
    D[start_vertex.id] = 0
    prev = {node_id: None for node_id in self.nodes.keys()}
    queue = []
    queue.append(start_vertex)

    while len(queue) > 0:
      current_vertex = queue.pop(0)

      for neighbor_id, distance in current_vertex.edges.items():
        old_cost = D[neighbor_id] if neighbor_id in D else float('inf')
        new_cost = D[current_vertex.id] + distance
        if new_cost < old_cost:
          queue.append(self.nodes[neighbor_id])
          D[neighbor_id] = new_cost
          prev[neighbor_id] = current_vertex.id

    return D, prev

  def dijkstra_all_nodes(self):
    node_ids = list(self.nodes.keys())
    V = len(node_ids)
    D = {node_id:{} for node_id in node_ids}
    queue = []

    """
    here there is a bitmap es. [1010] which represents exactly the nodes which have been visited and can be used as key in a dict
    """
    for i in range(V):
      D[node_ids[i]][2**i] = 0
      queue.append((self.nodes[node_ids[i]], 2**i))

    while len(queue) > 0:
      (current_vertex, mask) = queue.pop(0)
      for neighbor_id, distance in current_vertex.edges.items():
        new_mask = mask | 2**node_ids.index(neighbor_id)

        old_cost = D[neighbor_id][mask] if mask in D[neighbor_id] else float('inf')
        new_cost = D[current_vertex.id][mask] + distance
        
        # print(f"current: {current_vertex.id}, neighbour: {neighbor_id}, mask: {bin(mask)}, old_cost: {old_cost}, new_cost: {new_cost}")
        
        if old_cost > new_cost:
          queue.append((self.nodes[neighbor_id], new_mask))
          D[neighbor_id][new_mask] = D[current_vertex.id][mask] + distance
    
    best_answer = float('inf')
    solution_mask = 2**V-1
    for i in range(V):
      answer = D[node_ids[i]][solution_mask] if solution_mask in D[node_ids[i]] else float('inf')
      best_answer = min(best_answer, answer)
    
    return best_answer

  def discover_dijkstra_path(self, node_id, prev, solution = []):
    if prev[node_id] is None:
      return solution + [node_id]
    
    return self.discover_dijkstra_path(prev[node_id], prev, solution) + [node_id]

  def floyd_warshall(self):
    return float('inf')

  def _calculate_permutations(self, node, permutations=[]):
      for neighbor_id in node.edges:
        pass

    return

  def brute_force_search(self):
    node_ids = list(self.nodes.keys())
    distance = {node_id:{} for node_id in node_ids}

    for node_id_1 in node_ids:
      for node_id_2 in node_ids:
        distance[node_id_1][node_id_2] = floyd_warshall() if node_id_1 != node_id_2 else 0
    
    permutations = _calculate_permutations(self.nodes.values()[0])
  
if __name__ == "__main__":
  graph = Graph("test")
  node_A = Node("A")  
  node_B = Node("B")  
  node_C = Node("C")  
  node_D = Node("D")  
  node_E = Node("E")

  node_A.add_edge("B", 15)
  node_A.add_edge("C", 4)
  node_B.add_edge("E", 5)
  node_C.add_edge("D", 2)
  node_C.add_edge("E", 11)
  node_D.add_edge("E", 3)

  graph.add_node(node_A)
  graph.add_node(node_B)
  graph.add_node(node_C)
  graph.add_node(node_D)
  graph.add_node(node_E)

  solution, prev = graph.dijkstra(node_A)
  print("Dijkstra: ", solution)
  for node_id in graph.nodes.keys():
    print(f"Path for node '{node_id}'", graph.discover_dijkstra_path(node_id, prev))

  graph_2 = Graph("test_all_nodes")
  node_A = Node("A")  
  node_B = Node("B")  
  node_C = Node("C")  
  node_D = Node("D")

  node_A.add_edge("B", 1)
  node_A.add_edge("C", 1)
  node_A.add_edge("D", 1)
  node_B.add_edge("A", 1)
  node_C.add_edge("A", 1)
  node_D.add_edge("A", 1)

  graph_2.add_node(node_A)
  graph_2.add_node(node_B)
  graph_2.add_node(node_C)
  graph_2.add_node(node_D)
  
  solution = graph_2.dijkstra_all_nodes()
  print("Dijkstra shortest path visiting all nodes: ", solution)
  