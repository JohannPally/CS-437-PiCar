import math
import numpy as np
from collections import defaultdict
from typing import List, Tuple

# TODO: Specify correct number of rows and columns from grid that car scans

class AStar:
    def __init__(self, num = 100):
        self.NUM_ROWS = num
        self.NUM_COLS = num

    def get_neighbours(self, node: Tuple) -> List[Tuple]:
        r, c = node
        neighbours = []
        if r > 0:
            neighbours.append((r - 1, c))
        if r < self.NUM_ROWS - 1:
            neighbours.append((r + 1, c))
        if c > 0:
            neighbours.append((r, c - 1))
        if c < self.NUM_COLS - 1:
            neighbours.append((r, c + 1))
        return neighbours

    def compute(self, grid: List[List[int]], start_node: Tuple):
        end_node = (0, 0)
        dist = defaultdict(lambda: float('inf')) # Initially, distance to every other node is infinite. Replaced with tuple of 2 values which indicate a particular node (r, c)
        dist[start_node] = 0 # Distance from start node to start node is 0
        node = start_node
        path_trace = []
        visited = set()
        predecessor = {} # maps node to neighbour, used to trace path after destination has been found
        heuristic = {} # maps tuple (r, c) to heuristic value (euclidean distance to goal node)
        # Calculating the initial heuristic values using Euclidean distances
        x1, y1 = end_node
        y1 *= -1
        for r in range(self.NUM_ROWS):
            for c in range(self.NUM_COLS):
                x2, y2 = r, -c
                euclid_distance = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
                heuristic[(r, c)] = euclid_distance

        while True:
            if node != start_node:
                visited.add(node)
            neighbours = self.get_neighbours(node)
            unvisited_neighbours = list(filter(lambda n: n not in visited and n != start_node and grid[n[0]][n[1]] != 1, neighbours)) # if neighbour isn't visited, isn't a wall, nor the origin
            for neighbour in unvisited_neighbours:
                if dist[node] + 1 < dist[neighbour]:  # If current distance to a node is smaller than any previous possible distance, update it. Every node is only 1 node away from other nodes due to the fact that this is a nxn grid with no weights.
                    dist[neighbour] = dist[node] + 1
                    predecessor[neighbour] = node
                if neighbour == end_node:
                    print('Path found!')
                    n = neighbour
                    while n in predecessor:
                        if n not in [start_node, end_node]:
                            path_trace.append(n)
                        n = predecessor[n]
                    return path_trace[::-1] # reversed list. also, doesn't currently include origin or goal node in path trace
            smallest_path_dist, smallest_path_node = float('inf'), None
            for node in dist.keys():
                if (dist[node] + heuristic[node]) < smallest_path_dist and node not in visited and node != start_node and grid[node[0]][node[1]] != 1:
                    smallest_path_dist = dist[node] + heuristic[node]
                    smallest_path_node = node
            node = smallest_path_node
            if not node:
                print('No path found')
                return []

# use code below for testing random grids

# def get_random_grid_with_walls():
#     map_array = []
#     for r in range(NUM_ROWS):
#         new_row = []
#         for c in range(NUM_COLS):
#             random_state = np.random.choice([0, 1], p=[0.9, 0.1])
#             new_row.append(random_state)
#         map_array.append(new_row)
#     return np.array(map_array)

# grid = get_random_grid_with_walls()
# astar = AStar()
# path = astar.compute(grid, (NUM_ROWS - 1, NUM_COLS - 1))
# for n in path:
#     r, c = n
#     grid[r][c] = 8 # 8 used to indicate path when printing grid
# print(grid)
# print(path)