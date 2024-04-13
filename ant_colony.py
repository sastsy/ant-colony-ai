import networkx as nx
import numpy as np
import random

def create_graph():
    # Define the graph
    graph = nx.DiGraph()
    edges = [
        (1, 2, {'weight': 10}),
        (1, 3, {'weight': 20}),
        (2, 3, {'weight': 15}),
        (2, 4, {'weight': 25}),
        (3, 4, {'weight': 30}),
        (3, 5, {'weight': 35}),
        (4, 5, {'weight': 40}),
        (5, 1, {'weight': 45})
    ]
    graph.add_edges_from(edges)
    return graph

def initialize_pheromones(graph):
    return np.ones((len(graph), len(graph)))

def calculate_hamilton_cycle_cost(graph, cycle):
    cost = 0
    for i in range(len(cycle)):
        if graph.has_edge(cycle[i], cycle[(i + 1) % len(cycle)]):
            cost += graph[cycle[i]][cycle[(i + 1) % len(cycle)]]['weight']
        else:
            return float('inf')
    return cost

def tour_length(graph, tour):
    length = 0
    for i in range(len(tour)):
        if graph.has_edge(tour[i], tour[(i + 1) % len(tour)]):
            length += graph[tour[i]][tour[(i + 1) % len(tour)]]['weight']
        else:
            return float('inf')
    return length

def two_opt_swap(tour, i, j):
    new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
    return new_tour

def two_opt_local_search(graph, tour):
    improved = True
    best_tour = tour
    best_length = tour_length(graph, tour)

    while improved:
        improved = False
        for i in range(len(tour) - 1):
            for j in range(i + 1, len(tour)):
                new_tour = two_opt_swap(tour, i, j)
                new_length = tour_length(graph, new_tour)
                if new_length < best_length:
                    best_tour = new_tour
                    best_length = new_length
                    improved = True
        tour = best_tour

    return best_tour

def ant_colony_algorithm_with_2opt(graph, num_ants=10, num_iterations=100, evaporation_rate=0.5, alpha=1.0, beta=2.0):
    nodes = list(graph.nodes())
    pheromones = initialize_pheromones(graph)
    shortest_tour = None
    shortest_length = float('inf')
    
    for _ in range(num_iterations):
        for ant in range(num_ants):
            current_node = random.choice(nodes)
            tour = [current_node]
            allowed_nodes = [node for node in nodes if node != current_node]

            while allowed_nodes:
                allowed_indices = [i for i in range(len(allowed_nodes))]
                probabilities = np.zeros(len(allowed_nodes))
                total = 0
                for i, node in enumerate(allowed_nodes):
                    if graph.has_edge(current_node, node):
                        probabilities[i] = (pheromones[current_node - 1][node - 1] ** alpha) * \
                                           ((1.0 / graph[current_node][node]['weight']) ** beta)
                        total += probabilities[i]
                if total == 0:
                    next_node = random.choice(allowed_nodes)
                else:
                    probabilities /= total
                    next_node = allowed_nodes[np.random.choice(list(allowed_indices), p=probabilities)]

                tour.append(next_node)
                allowed_nodes.remove(next_node)
                current_node = next_node

            tour = two_opt_local_search(graph, tour)  # Apply 2-opt local search
            tour_len = tour_length(graph, tour)
            if tour_len < shortest_length:
                shortest_tour = tour
                shortest_length = tour_len
            for i in range(len(tour) - 1):
                pheromones[tour[i] - 1][tour[i + 1] - 1] += 1.0 / tour_len
                pheromones[tour[i + 1] - 1][tour[i] - 1] += 1.0 / tour_len
            pheromones[tour[-1] - 1][tour[0] - 1] += 1.0 / tour_len

        pheromones *= (1 - evaporation_rate)

    return shortest_tour, shortest_length

# Example usage:
if __name__ == "__main__":
    graph = create_graph()
    shortest_tour, shortest_length = ant_colony_algorithm_with_2opt(graph)
    print("Shortest Hamiltonian cycle:", shortest_tour)
    print("Length of the shortest Hamiltonian cycle:", shortest_length)
