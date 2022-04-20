from queue import PriorityQueue

class Graph:

  class Node:
    def __init__(self, node_id, value=0):
      self.id = node_id
      self.value = value
      self.edges = {} 

    def add_edge(self, other_node_id, weight=0)
      self.edges[other_node_id] = weight

  def __init__(self, graph_id):
    self.graph_id = graph_id
    self.nodes = {}
    self.visited = []

  def add_node(self, node):
    self.nodes[node.id] = node

  def add_edge(self, node_id_1, node_id_2, weight):
    self.nodes[node_id_1].add_edge(node_id_2, weight)
    self.nodes[node_id_2].add_edge(node_id_1, weight)

  def dijkstra(self, start_vertex):
    nodes_number = len(self.nodes.keys())
    D = {v:float('inf') for v in range(nodes_number)}
    D[start_vertex.id] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex.id))

    while not pq.empty():
      (dist, current_vertex) = pq.get()
      self.visited.append(current_vertex.id)

      for neighbor_id, weight in current_vertex.edges:
        if neighbor_id not in self.visited:
          old_cost = D[neighbor_id]
          new_cost = D[current_vertex.id] + weight
          if new_cost < old_cost:
            pq.put((new_cost, neighbor_id))
            D[neighbor_id] = new_cost
    return D

  