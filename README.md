# Ant Colony Optimization with 2-opt Local Search for Finding the Shortest Hamiltonian Cycle

## Contents

- [Overview](#overview)
- [Implementation Details](#implementation-details)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)
- [License](#license)

## Overview

This project implements the Ant Colony Optimization (ACO) algorithm with 2-opt local search to find the shortest Hamiltonian cycle in a given graph. ACO is a metaheuristic algorithm inspired by the foraging behavior of ants.

In this implementation, the algorithm is applied to find the shortest Hamilton cycle in a given directed graph. A Hamilton cycle is a cycle that visits each vertex exactly once and returns to the starting vertex.

The modification introduced in this implementation involves 2-opt local search. The 2-opt local search is a local optimization method commonly used to improve the solution obtained by constructive algorithms like ACO.

## Implementation Details
- Graph Representation: The graph is represented using NetworkX, a Python library for the creation, manipulation, and study of complex networks.

- Pheromone Matrix: Pheromone levels are maintained in a matrix, where each entry represents the amount of pheromone on the edge between two nodes.

- Parameter Tuning: The algorithm provides flexibility through parameters such as the number of ants, number of iterations, evaporation rate, and pheromone and heuristic importance factors (alpha and beta).


## Usage

To use the simulated annealing algorithm:

1. Ensure you have Python installed on your system.
2. Install the required dependencies listed in the [Dependencies](#dependencies) section.
3. Run the `GUI.py` file.
4. Click on the canvas to add vertices.
5. Click on the "Add Weighted Edge" button to add edges between vertices.
6. Once the graph is constructed, click on the "Calculate Cycle" button to find the shortest Hamilton cycle.

## File Structure

- `annealing.py`: Contains the implementation of the ACO algorithm with 2-opt local search.
- `GUI.py`: Implements a graphical user interface for visualizing graphs and interacting with the algorithm.
  
## Dependencies

- `networkx`: For handling graphs and calculating the Hamilton cycle cost.
- `tkinter`: For creating the graphical user interface.
- `matplotlib`: For plotting the graph visualization.
- `numpy`: For numerical calculations.
  
You can install the dependencies using pip:

```bash
pip install networkx matplotlib numpy
```