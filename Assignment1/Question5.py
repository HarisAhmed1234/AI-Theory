import heapq

class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, node1, node2, cost):
        if node1 not in self.edges:
            self.edges[node1] = []
        if node2 not in self.edges:
            self.edges[node2] = []
        self.edges[node1].append((node2, cost))
        self.edges[node2].append((node1, cost))

def calculate_path_cost(graph, path):
    cost = 0
    for i in range(len(path) - 1):
        for neighbor, edge_cost in graph.edges[path[i]]:
            if neighbor == path[i + 1]:
                cost += edge_cost
                break
    return cost

def bfs(graph, start, goal):
    queue = [(start, [start])]
    visited = set()

    while queue:
        current, path = queue.pop(0)
        if current == goal:
            return path, calculate_path_cost(graph, path)
        if current not in visited:
            visited.add(current)
            for neighbor, _ in graph.edges.get(current, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None, float('inf')

def uniform_cost_search(graph, start, goal):
    priority_queue = [(0, start, [])]
    cost_so_far = {start: 0}

    while priority_queue:
        cost, current, path = heapq.heappop(priority_queue)
        if current == goal:
            return path + [current], cost
        for neighbor, edge_cost in graph.edges.get(current, []):
            new_cost = cost + edge_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(priority_queue, (new_cost, neighbor, path + [current]))
    return None, float('inf')

def greedy_best_first_search(graph, start, goal, heuristic):
    priority_queue = [(heuristic[start], start, [start])]
    visited = set()

    while priority_queue:
        _, current, path = heapq.heappop(priority_queue)
        if current == goal:
            return path, calculate_path_cost(graph, path)
        if current not in visited:
            visited.add(current)
            for neighbor, _ in graph.edges.get(current, []):
                if neighbor not in visited:
                    heapq.heappush(priority_queue, (heuristic[neighbor], neighbor, path + [neighbor]))
    return None, float('inf')

def iterative_deepening_dfs(graph, start, goal, max_depth=100):
    for depth in range(max_depth):
        result = depth_limited_search(graph, start, goal, depth, [])
        if result:
            return result, calculate_path_cost(graph, result)
    return None, float('inf')

def depth_limited_search(graph, current, goal, depth, path):
    if current == goal:
        return path + [current]
    if depth == 0:
        return None
    for neighbor, _ in graph.edges.get(current, []):
        if neighbor not in path:
            result = depth_limited_search(graph, neighbor, goal, depth - 1, path + [current])
            if result:
                return result
    return None

romania_graph = Graph()
romania_graph.add_edge("Arad", "Zerind", 75)
romania_graph.add_edge("Arad", "Timisoara", 118)
romania_graph.add_edge("Arad", "Sibiu", 140)
romania_graph.add_edge("Zerind", "Oradea", 71)
romania_graph.add_edge("Oradea", "Sibiu", 151)
romania_graph.add_edge("Sibiu", "Fagaras", 99)
romania_graph.add_edge("Sibiu", "Rimnicu Vilcea", 80)
romania_graph.add_edge("Fagaras", "Bucharest", 211)
romania_graph.add_edge("Rimnicu Vilcea", "Pitesti", 97)
romania_graph.add_edge("Rimnicu Vilcea", "Craiova", 146)
romania_graph.add_edge("Pitesti", "Bucharest", 101)
romania_graph.add_edge("Bucharest", "Giurgiu", 90)
romania_graph.add_edge("Bucharest", "Urziceni", 85)
romania_graph.add_edge("Urziceni", "Vaslui", 142)
romania_graph.add_edge("Vaslui", "Iasi", 92)
romania_graph.add_edge("Iasi", "Neamt", 87)
romania_graph.add_edge("Timisoara", "Lugoj", 111)
romania_graph.add_edge("Lugoj", "Mehadia", 70)
romania_graph.add_edge("Mehadia", "Drobeta", 75)
romania_graph.add_edge("Drobeta", "Craiova", 120)
romania_graph.add_edge("Urziceni", "Hirsova", 98)
romania_graph.add_edge("Hirsova", "Eforie", 86)

heuristic = {
    "Arad": 366, "Zerind": 374, "Oradea": 380, "Sibiu": 253, "Fagaras": 178,
    "Rimnicu Vilcea": 193, "Pitesti": 98, "Craiova": 160, "Bucharest": 0,
    "Giurgiu": 77, "Urziceni": 80, "Vaslui": 199, "Iasi": 226, "Neamt": 234,
    "Timisoara": 329, "Lugoj": 244, "Mehadia": 241, "Drobeta": 242, 
    "Hirsova": 151, "Eforie": 161
}

start_city = input("Enter the start city: ")
goal_city = input("Enter the goal city: ")

bfs_path, bfs_cost = bfs(romania_graph, start_city, goal_city)
ucs_path, ucs_cost = uniform_cost_search(romania_graph, start_city, goal_city)
gbfs_path, gbfs_cost = greedy_best_first_search(romania_graph, start_city, goal_city, heuristic)
iddfs_path, iddfs_cost = iterative_deepening_dfs(romania_graph, start_city, goal_city)

print(f"\nBFS Path: {bfs_path}, Cost: {bfs_cost}")
print(f"UCS Path: {ucs_path}, Cost: {ucs_cost}")
print(f"GBFS Path: {gbfs_path}, Cost: {gbfs_cost}")
print(f"IDDFS Path: {iddfs_path}, Cost: {iddfs_cost}")
