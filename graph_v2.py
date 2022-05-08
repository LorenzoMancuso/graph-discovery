from queue import PriorityQueue
class Node:
  def __init__(self, node_id, value=0):
    self.id = node_id
    self.value = value
    self.edges = {} 

  def add_edge(self, other_node_id, distance=0):
    self.edges[other_node_id] = distance

  def add_undirected_edge(self, other_node, distance=0):
    self.edges[other_node.id] = distance
    other_node.edges[self.id] = distance

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
  
  # --------------------------------------------

  def _stuck(self, node, path, k=0):
    #print("stuck ", path, node.id, k)
    stuck = True
    if path.count(node.id) >= 1:
      return True
    if k == 2:
      return True
    if node.id not in path:
      return False
    
    for neighbour_id in node.edges.keys():
      stuck = stuck and self._stuck(self.nodes[neighbour_id], path + [node.id], k+1)

    return stuck

  def find_all_paths_visiting_all_nodes(self):
    all_paths = []
    for node in self.nodes.values():
      all_paths += self.find_all_paths_visiting_all_nodes_from_node(node)
    return all_paths
    
  def find_all_paths_visiting_all_nodes_from_node(self, node):
    solution_paths = []
    nodes_ids = node.edges.keys()
    node_ids = list(self.nodes.keys())
    V = len(node_ids)
    solution_mask = 2**V-1
    mask = 2**node_ids.index(node.id)

    for neighbour_id in nodes_ids:
      self.find_all_paths_visiting_all_nodes_from_node_helper(self.nodes[neighbour_id], [node.id], solution_paths, mask, solution_mask, node_ids)
    
    return solution_paths

  def find_all_paths_visiting_all_nodes_from_node_helper(self, node, path, solution_paths, mask, solution_mask, node_ids):
    if self._stuck(node, path):
      pass
    elif mask == solution_mask:
      solution_paths.append(path+[node.id])
    else:    
      for neighbour_id in node.edges.keys():
        new_mask = mask | 2**node_ids.index(neighbour_id)
        self.find_all_paths_visiting_all_nodes_from_node_helper(self.nodes[neighbour_id], path+[node.id], solution_paths, new_mask, solution_mask, node_ids)

  # --------------------------------------------

  def floyd_warshall(self):
    node_ids = list(self.nodes.keys())
    distance = {node_id:{node_id:float('inf') for node_id in node_ids} for node_id in node_ids}
    for node_id in node_ids:
      distance[node_id][node_id] = 0

    for node in self.nodes.values():
      for neighbor_id, weight in node.edges.items():
        distance[node.id][neighbor_id] = weight

    for k in node_ids:
      for i in node_ids:
        for j in node_ids:
          if distance[i][j] > distance[i][k] + distance[k][j]:
            distance[i][j] = distance[i][k] + distance[k][j]

    return distance

  def _calculate_permutations(self, elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in self._calculate_permutations(elements[1:]):
            for i in range(len(elements)):
                # nb elements[0:1] works in both string and list contexts
                yield perm[:i] + elements[0:1] + perm[i:]

  def brute_force_search(self):
    distance = self.floyd_warshall()
    # permutations = list(self._calculate_permutations(list(self.nodes.keys())))
    permutations = self.find_all_paths_visiting_all_nodes()
    answer = float('inf')
    best_path = None

    for permutation in permutations:
      cost = 0
      previous_node_id = permutation[0]
      for node_id in permutation:
        cost += distance[previous_node_id][node_id]
        previous_node_id = node_id
      if cost < answer:
        answer = cost
        best_path = permutation

    return best_path, answer


if __name__ == "__main__":
  graph = Graph("test")
  node_A = Node("A")  
  node_B = Node("B")  
  node_C = Node("C")  
  node_D = Node("D")  
  node_E = Node("E")

  node_A.add_undirected_edge(node_B, 15)
  node_A.add_undirected_edge(node_C, 4)
  node_B.add_undirected_edge(node_E, 5)
  node_C.add_undirected_edge(node_D, 2)
  node_C.add_undirected_edge(node_E, 11)
  node_D.add_undirected_edge(node_E, 3)

  graph.add_node(node_A)
  graph.add_node(node_B)
  graph.add_node(node_C)
  graph.add_node(node_D)
  graph.add_node(node_E)

  """
  solution, prev = graph.dijkstra(node_A)
  print("Dijkstra: ", solution)
  for node_id in graph.nodes.keys():
    print(f"Path for node '{node_id}'", graph.discover_dijkstra_path(node_id, prev))

  solution = graph.dijkstra_all_nodes()
  print("Dijkstra shortest path visiting all nodes: ", solution)
  """
  solution = graph.find_all_paths_visiting_all_nodes_from_node(node_A)

  solution = sorted(solution, key=lambda x: len(x))[:5]

  print(solution)
  #solution, cost = graph.brute_force_search()
  #print("Brute force search: ", solution, " Cost: ", cost)

  #---------------------------------------
  """
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
  
  # solution = graph_2.dijkstra_all_nodes()
  # print("Dijkstra visiting all nodes: ", solution)

  solution = graph_2.dijkstra_all_nodes()
  print("Dijkstra shortest path visiting all nodes: ", solution)

  solution, cost = graph_2.brute_force_search()
  print("Brute force search: ", solution, " Cost: ", cost)
  """