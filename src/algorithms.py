import heapq
import time
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass


@dataclass
class PathResult:
    path: List[str]
    distance: float
    nodes_explored: int
    execution_time_ms: float
    algorithm: str


class Graph:
    def __init__(self):
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = {}
        self.node_positions: Dict[str, Tuple[float, float]] = {}
    
    def add_node(self, node_id: str, x: float = 0, y: float = 0):
        if node_id not in self.adjacency_list:
            self.adjacency_list[node_id] = []
        self.node_positions[node_id] = (x, y)
    
    def add_edge(self, from_node: str, to_node: str, weight: float, bidirectional: bool = True):
        if from_node not in self.adjacency_list:
            self.add_node(from_node)
        if to_node not in self.adjacency_list:
            self.add_node(to_node)
        
        self.adjacency_list[from_node].append((to_node, weight))
        if bidirectional:
            self.adjacency_list[to_node].append((from_node, weight))
    
    def get_neighbors(self, node_id: str) -> List[Tuple[str, float]]:
        return self.adjacency_list.get(node_id, [])
    
    def get_nodes(self) -> List[str]:
        return list(self.adjacency_list.keys())
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Graph':
        graph = cls()
        
        for node in data.get('nodes', []):
            if isinstance(node, dict):
                graph.add_node(
                    node['id'],
                    node.get('x', 0),
                    node.get('y', 0)
                )
            else:
                graph.add_node(str(node))
        
        for edge in data.get('edges', []):
            graph.add_edge(
                edge['from'],
                edge['to'],
                edge.get('weight', 1.0),
                edge.get('bidirectional', True)
            )
        
        return graph


def dijkstra(graph: Graph, start: str, end: str) -> Optional[PathResult]:
    start_time = time.perf_counter()
    
    if start not in graph.adjacency_list or end not in graph.adjacency_list:
        return None
    
    distances: Dict[str, float] = {node: float('inf') for node in graph.adjacency_list}
    distances[start] = 0
    previous: Dict[str, Optional[str]] = {node: None for node in graph.adjacency_list}
    
    priority_queue: List[Tuple[float, str]] = [(0, start)]
    visited = set()
    nodes_explored = 0
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        nodes_explored += 1
        
        if current_node == end:
            break
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph.get_neighbors(current_node):
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    if distances[end] == float('inf'):
        return None
    
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    execution_time = (time.perf_counter() - start_time) * 1000
    
    return PathResult(
        path=path,
        distance=distances[end],
        nodes_explored=nodes_explored,
        execution_time_ms=round(execution_time, 4),
        algorithm="dijkstra"
    )


def euclidean_heuristic(graph: Graph, node: str, goal: str) -> float:
    if node not in graph.node_positions or goal not in graph.node_positions:
        return 0
    
    x1, y1 = graph.node_positions[node]
    x2, y2 = graph.node_positions[goal]
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def manhattan_heuristic(graph: Graph, node: str, goal: str) -> float:
    if node not in graph.node_positions or goal not in graph.node_positions:
        return 0
    
    x1, y1 = graph.node_positions[node]
    x2, y2 = graph.node_positions[goal]
    return abs(x2 - x1) + abs(y2 - y1)


def astar(
    graph: Graph,
    start: str,
    end: str,
    heuristic: str = "euclidean"
) -> Optional[PathResult]:
    start_time = time.perf_counter()
    
    if start not in graph.adjacency_list or end not in graph.adjacency_list:
        return None
    
    heuristic_fn: Callable[[Graph, str, str], float]
    if heuristic == "manhattan":
        heuristic_fn = manhattan_heuristic
    else:
        heuristic_fn = euclidean_heuristic
    
    g_score: Dict[str, float] = {node: float('inf') for node in graph.adjacency_list}
    g_score[start] = 0
    
    f_score: Dict[str, float] = {node: float('inf') for node in graph.adjacency_list}
    f_score[start] = heuristic_fn(graph, start, end)
    
    previous: Dict[str, Optional[str]] = {node: None for node in graph.adjacency_list}
    
    open_set: List[Tuple[float, str]] = [(f_score[start], start)]
    open_set_hash = {start}
    closed_set = set()
    nodes_explored = 0
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current not in open_set_hash:
            continue
        
        open_set_hash.discard(current)
        nodes_explored += 1
        
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = previous[current]
            path.reverse()
            
            execution_time = (time.perf_counter() - start_time) * 1000
            
            return PathResult(
                path=path,
                distance=g_score[end],
                nodes_explored=nodes_explored,
                execution_time_ms=round(execution_time, 4),
                algorithm=f"astar_{heuristic}"
            )
        
        closed_set.add(current)
        
        for neighbor, weight in graph.get_neighbors(current):
            if neighbor in closed_set:
                continue
            
            tentative_g = g_score[current] + weight
            
            if tentative_g < g_score[neighbor]:
                previous[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic_fn(graph, neighbor, end)
                
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
    
    return None
