import heapq
import networkx as nx
import matplotlib.pyplot as plt
import csv
import os
import ast





class Node:
    def __init__(self, point):
        self.point = point
        self.neighbors = []

    def add_neighbor(self, neighbor, difficulty):
        self.neighbors.append((neighbor, difficulty))

class WeightedGraph:
    def __init__(self):
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

        if isinstance(difficulty, (int, float)):
            self.points[source].add_neighbor(self.points[destination], difficulty)
            self.points[destination].add_neighbor(self.points[source], difficulty)
            self.G.add_edge(source, destination, weight=difficulty)
        else:
            print("Invalid difficulty level. Please enter a valid number.")

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
        new_path = self.best_path(new_current_node, end_node)
        if new_path:
            if traveled_path[-1] == new_path[0]:
                new_path = new_path[1:]
            combined_path = traveled_path + new_path
            new_distance = self.find_shortest_distance(new_current_node, end_node)
            return combined_path, new_distance
        else:
            return traveled_path, None

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

    def add_path_to_csv(self, csv_file, source, destination, time, list):
        header_exists = os.path.isfile(csv_file)
        with open(csv_file, mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            if not header_exists:
                csv_writer.writerow(['Source', 'Destination', 'Time', 'Path'])
            csv_writer.writerow([source, destination, time,list])

    def load_data_from_csv(self, csv_file):
        if not os.path.isfile(csv_file):
            print("CSV file not found.")
            return

        with open(csv_file, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                source, destination, time = row
                if time.replace('.', '', 1).isdigit():
                    time = float(time)
                    self.add_path(source, destination, time)
                else:
                    print(f"Invalid time value in CSV: {time}")



    def travel(self, source, destination, time1, csv_file):
        closest_time = None
        chosen_path = None

        with open(csv_file, mode='r') as file:
            csv_reader = csv.reader(file)
            closest_time_diff = float('inf')

            for row in csv_reader:
                s, d, t, path_str = row
                if s == source and d == destination:
                    time_diff = abs(float(t) - float(time1))
                    if time_diff < closest_time_diff:
                        closest_time_diff = time_diff
                        closest_time = float(t)
                        chosen_path = ast.literal_eval(path_str)

        if chosen_path:
            print(f"Chosen path: {chosen_path} with a time of: {closest_time}")
            self.visualize_graph(highlight_path=chosen_path)
        else:
            print("No matching path found in CSV. Calculating best path...")
            chosen_path = self.best_path(source, destination)
            if not chosen_path:
                print(f"No path found from {source} to {destination}.")
                return None
            self.visualize_graph(highlight_path=chosen_path)

        # Current node checker and rerouter
        travelled_path = []
        current_node = source  # Initialize the current node with the source
        while current_node != 'done':
            print(f"Current node: {current_node}")
            # Display adjacent nodes to the current node
            adjacent_nodes = [neighbor[0].point for neighbor in self.points[current_node].neighbors]
            print(f"Adjacent nodes: {', '.join(adjacent_nodes)}")

            next_node = input("Enter the next node or 'done' if you have reached the destination: ").strip()
            if next_node == 'done':
                break
            if next_node in adjacent_nodes or next_node == current_node:  # Check if the next node is adjacent
                print("Valid adjacent node.")
                travelled_path.append(next_node)
                new_route_and_distance = self.reroute_from_new_node(travelled_path, next_node, destination)

                if new_route_and_distance:
                    new_path, _ = new_route_and_distance  # Separate the path and distance
                    if new_path and isinstance(new_path, list):
                        print(f"New route: {' -> '.join(new_path)}")
                        self.visualize_graph(highlight_path=new_path)
                        chosen_path = new_path
                    else:
                        print("Received an invalid path from reroute_from_new_node.")
                        return None
                else:
                    print("Invalid path. Cannot reroute to the specified node.")

            else:
                print("Entered node is not adjacent to the current node. Please enter a valid adjacent node.")
                continue  # Prompt for input again without changing the current node

            current_node = next_node

        # Storing the final path to CSV after reaching the destination
        if current_node == 'done':
            self.add_path_to_csv(csv_file, source, destination, time1, chosen_path)
            print("Final path details stored to CSV.")
            return chosen_path







graph = WeightedGraph()
def get_user_input():
    
    csv_file = input("Enter the CSV file path: ")
    while True:
        
        print("\nMenu:")
        print("1. Add a node")
        print("2. Add a path")
        print("4. Visualize grap1h")
        print("7. Travel")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            node = input("Enter the node label: ")
            graph.add_point(node)
            print(f"Node '{node}' added.")

        elif choice == "2":
            src = input("Enter the source node: ")
            dest = input("Enter the destination node: ")
            difficulty = input("Enter the difficulty level: ")
            if difficulty.replace('.', '', 1).isdigit():
                difficulty = float(difficulty)
                graph.add_path(src, dest, difficulty)
                print(f"Path from '{src}' to '{dest}' with difficulty {difficulty} added.")
            else:
                print("Invalid difficulty level. Please enter a valid number.")

    

        elif choice == "4":
            start_node = input("Enter the start node for path visualization (optional, press Enter to skip): ")
            end_node = input("Enter the end node for path visualization (optional, press Enter to skip): ")
            if start_node and end_node:
                graph.visualize_graph(graph.best_path(start_node, end_node))
            else:
                graph.visualize_graph()



        elif choice == "7":
            source = input("Enter the source node: ")
            destination = input("Enter the destination node: ")
            most_frequent = input("Choose most frequent path (yes/no): ").lower()
            time=input("time :")
            most_frequent = most_frequent == 'yes'
            graph.travel(source, destination,time, csv_file)

        elif choice == "8":
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")

get_user_input()
