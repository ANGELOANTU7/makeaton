##team oregano

import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def _init_(self, point):
        self.point = point
        self.neighbors = []

    def add_neighbor(self, neighbor, difficulty):
        self.neighbors.append((neighbor, difficulty))

class WeightedGraph:
    def _init_(self):
        self.points = {}
        self.G = nx.Graph()

    def add_point(self, point):
        new_point = Node(point)
        self.points[point] = new_point
        self.G.add_node(point)

    def add_path(self, source, destination, difficulty):
        if source not in self.points:
            self.add_point(source)
        if destination not in self.points:
            self.add_point(destination)
        self.points[source].add_neighbor(self.points[destination], difficulty)
        self.points[destination].add_neighbor(self.points[source], difficulty)
        self.G.add_edge(source, destination, weight=difficulty)

    def dijkstra(self, start):
        difficulties = {point: float('infinity') for point in self.points}
        previous_points = {point: None for point in self.points}
        difficulties[start] = 0
        priority_queue = [(0, start)]

        while priority_queue:
            current_difficulty, current_point = heapq.heappop(priority_queue)
            if current_difficulty > difficulties[current_point]:
                continue
            
            for neighbor, difficulty in self.points[current_point].neighbors:
                path_difficulty = current_difficulty + difficulty
                if path_difficulty < difficulties[neighbor.point]:
                    difficulties[neighbor.point] = path_difficulty
                    previous_points[neighbor.point] = current_point
                    heapq.heappush(priority_queue, (path_difficulty, neighbor.point))
        
        return difficulties, previous_points
    
    def reroute_from_new_node(self, traveled_path, new_current_node, end_node):
        """
        Finds a new path from the new current node to the end node and appends it to the traveled path.
        """
        # Find a new path from the new current node to the end node
        new_path = self.best_path(new_current_node, end_node)
        if new_path:
            # Exclude the first node of the new path if it is the same as the last node of the traveled path
            if traveled_path[-1] == new_path[0]:
                new_path = new_path[1:]
            # Combine the traveled path with the new path
            combined_path = traveled_path + new_path
            # Compute the total new distance by adding the traveled distance and the distance of the new path
            new_distance = self.find_shortest_distance(new_current_node, end_node)
            return combined_path, new_distance
        else:
            return traveled_path, None  # Return the traveled path if no new path is found

    
    def best_path(self, start, end):
        difficulties, previous_points = self.dijkstra(start)
        path = []
        current_point = end

        while current_point is not None:
            path.insert(0, current_point)
            current_point = previous_points[current_point]

        if difficulties[end] != float('infinity'):
            return path
        else:
            return []

    def find_shortest_distance(self, start, end):
        difficulties, _ = self.dijkstra(start)
        return difficulties[end]

    def visualize_graph(self, highlight_path=None):
        pos = nx.spring_layout(self.G)
        nx.draw_networkx_nodes(self.G, pos)
        nx.draw_networkx_labels(self.G, pos)
        nx.draw_networkx_edges(self.G, pos, edgelist=self.G.edges(data=True), width=1, edge_color='gray')

        if highlight_path:
            edges = [(highlight_path[i], highlight_path[i+1]) for i in range(len(highlight_path)-1)]
            nx.draw_networkx_edges(self.G, pos, edgelist=edges, edge_color='red', width=2)

        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)

        plt.axis('off')
        plt.show()

def get_user_input():
    while True:
        print("\nMenu:")
        print("1. Add a node")
        print("2. Add a path")
        print("3. Find shortest path")
        print("4. Visualize graph")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            node = input("Enter the node label: ")
            graph.add_point(node)
            print(f"Node '{node}' added.")
            
        elif choice == "2":
            src = input("Enter the source node: ")
            dest = input("Enter the destination node: ")
            try:
                difficulty = float(input("Enter the difficulty level: "))
                graph.add_path(src, dest, difficulty)
                print(f"Path from '{src}' to '{dest}' with difficulty {difficulty} added.")
            except ValueError:
                print("Invalid difficulty level. Please enter a number.")
        
        
        elif choice == "3":
            start_node = input("Enter the start node: ")
            end_node = input("Enter the end node: ")
            shortest_path = graph.best_path(start_node, end_node)
            if shortest_path:
                print(f"Best Path from Node {start_node} to Node {end_node}: {' -> '.join(shortest_path)}")
                shortest_distance = graph.find_shortest_distance(start_node, end_node)
                print(f"Shortest Distance from Node {start_node} to Node {end_node}: {shortest_distance}")

                graph.visualize_graph(shortest_path)  # Visualize the original shortest path.

                reroute = input("Do you need to reroute from a new current node? (yes/no): ").lower()
                if reroute == 'yes':
                    traveled_nodes = input("Enter the nodes you have traveled so far, separated by commas: ")
                    traveled_path = [node.strip() for node in traveled_nodes.split(',')]
                    new_current_node = traveled_path[-1]  # Last node is the current position

                    new_path, new_distance = graph.reroute_from_new_node(traveled_path, new_current_node, end_node)
                    if new_path:
                        print(f"Combined Path including traveled and new path: {' -> '.join(new_path)}")
                        if new_distance is not None:
                            print(f"New Shortest Distance from Node {new_current_node} to Node {end_node}: {new_distance}")
                        graph.visualize_graph(new_path)  # Visualize the new combined path.
                    else:
                        print("Unable to find a new path from your current location.")

	        
        elif choice == "4":
            start_node = input("Enter the start node for path visualization (optional, press Enter to skip): ")
            end_node = input("Enter the end node for path visualization (optional, press Enter to skip): ")
            if start_node and end_node:
                graph.visualize_graph(graph.best_path(start_node, end_node))
            else:
                graph.visualize_graph()
                
        elif choice == "5":
            print("Exiting...")
            break
            
        else:
            print("Invalid choice, please try again.")

# Initialize the graph
graph = WeightedGraph()

# Start the user input loop
get_user_input()