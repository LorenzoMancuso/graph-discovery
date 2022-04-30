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

    queue = []
    queue.append(start_vertex)

    while len(queue) > 0:
      current_vertex = queue.pop(0)
      print("current vertex ", current_vertex.id)
      print("current vertex edges", current_vertex.edges)

      for neighbor_id, distance in current_vertex.edges.items():
        print("visited: ", self.visited)
        print(f"neighbour id: {neighbor_id}, distance: {distance}")

        old_cost = D[neighbor_id] if neighbor_id in D else float('inf')
        new_cost = D[current_vertex.id] + distance
        if new_cost < old_cost:
          queue.append(self.nodes[neighbor_id])
          D[neighbor_id] = new_cost
    return D

  def dijkstra_all_nodes(self):
    node_ids = self.node.keys()
    V = len(node_ids)
    D = {node_id:{2^i:float('inf') for i in range(V)} for node_id in node_ids}
    queue = []

    """
    here there is a bitmap es. [1010] which represents exactly the nodes which have been visited and can be used as key in a dict
    """
    for i in range(V):
      D[node_ids[i]][2^i] = 0
      queue.append(node_ids[i], 2^i)

    while len(queue) > 0:
      (current_vertex, mask) = queue.pop(0)

      for neighbor_id, distance in current_vertex.edges.items():
        new_mask = mask | 2^node_ids.index(neighbor_id)
        if D[neighbor_id][new_mask] > D[current_vertex.id][mask] + distance:
          queue.append(self.nodes[neighbor_id], new_mask)
          D[neighbor_id][new_mask] = D[current_vertex.id][mask] + distance
    
    answer = float('inf')
    for i in range(V):
      answer = min(answer, D[node_ids[i]][2^V-1])
    
    return answer


    return D

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

  solution = graph.dijkstra(node_A)
  print(solution)
  