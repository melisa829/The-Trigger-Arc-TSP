
# The Trigger Arc TSP

A Python implementation of the **Trigger Arc Traveling Salesperson Problem (Trigger Arc TSP)** using three different algorithmic approaches: Greedy with Backtracking, Genetic Algorithm, and Simulated Annealing.

## 1. Project Overview

The Trigger Arc Traveling Salesperson Problem is a variant of the classical Traveling Salesperson Problem (TSP) defined on a directed graph.

The objective is to find a minimum-cost Hamiltonian cycle that:

- Starts at a designated depot node (node 0).
- Visits every node exactly once.
- Returns to the depot.
- Minimizes the total traversal cost while considering trigger-target relationships between arcs.

### Trigger-Target Relationships

A trigger relation connects a trigger arc to a target arc.

When a trigger arc is traversed, it may change the cost of its associated target arc. The following rules apply:

- A trigger affects a target arc only if the target has not yet been traversed.
- If multiple triggers affect the same target, the most recently traversed trigger determines its updated cost.
- Once a target arc has been traversed, its cost cannot be changed retroactively.

## 2. Implemented Algorithms

The project includes three approaches:

### 2.1 Greedy with Backtracking

Constructs a route by prioritizing candidate arcs according to their current costs. Backtracking is used when a selected path cannot be completed into a valid Hamiltonian cycle.

### 2.2 Genetic Algorithm

Uses a population-based metaheuristic inspired by natural evolution.

Main operations include:
- Random initial population generation.
- Fitness evaluation.
- Tournament selection.
- Crossover.
- Mutation.
- Elitism.

### 2.3 Simulated Annealing

Uses a probabilistic search strategy inspired by the physical annealing process.

The algorithm explores neighboring routes and uses a temperature-dependent acceptance probability to sometimes accept worse solutions, helping it explore the search space.

## 3. Project Structure

```text
The-Trigger-Arc-TSP/
│
├── instances/
│   ├── test_instance.txt
│   ├── test_instance_5.txt
│   └── test_instance_6.txt
│
├── src/
│   ├── __init__.py
│   ├── graph.py
│   ├── parser.py
│   ├── cost_evaluator.py
│   ├── greedy.py
│   ├── genetic_algorithm.py
│   ├── simulated_annealing.py
│   ├── visualization.py
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   ├── test_graph.py
│   ├── test_parser.py
│   ├── test_cost_evaluator.py
│   ├── test_greedy.py
│   ├── test_genetic_algorithm.py
│   ├── test_simulated_annealing.py
│   └── test_visualization.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## 4. Requirements

- Python 3.10 or newer
- Dependencies listed in `requirements.txt`

## 5. Installation

Clone the repository:

```bash
git clone https://github.com/melisa829/The-Trigger-Arc-TSP.git
cd The-Trigger-Arc-TSP
```

Create and activate a virtual environment:

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 6. Running the Project

Run all implemented algorithms and compare their results:

```bash
python -m src.main instances/test_instance.txt
```

Run a specific algorithm:

**Greedy with Backtracking**

```bash
python -m src.main instances/test_instance.txt --algorithm greedy
```

**Genetic Algorithm**

```bash
python -m src.main instances/test_instance.txt --algorithm genetic
```

**Simulated Annealing**

```bash
python -m src.main instances/test_instance.txt --algorithm annealing
```

Display graph and route visualizations:

```bash
python -m src.main instances/test_instance.txt --visualize
```

The program reports:
- Selected route (arc IDs).
- Total route cost.
- Execution time.
- Independently verified route cost.
- Comparative results when all algorithms are executed.

## 7. Input File Format

Each instance is stored in a text file.

### Header

The first line contains:

```text
number_of_nodes number_of_arcs number_of_trigger_relations
```

### Arc Definitions

Each arc is represented by:

```text
arc_id tail_node head_node cost
```

### Trigger Relations

Each trigger relation is represented by:

```text
trigger_arc_id target_arc_id new_cost
```

### Example

```text
4 12 3
1 0 1 10
2 0 2 15
3 0 3 20
4 1 0 10
5 1 2 9
6 1 3 12
7 2 0 15
8 2 1 9
9 2 3 8
10 3 0 20
11 3 1 12
12 3 2 8
1 5 5
2 9 4
5 10 6
```

Nodes are numbered from `0` to `N-1`, and node `0` is the depot.

## 8. Testing

Run the complete automated test suite:

```bash
python -m unittest discover -s tests -v
```

The tests cover:
- Graph validation.
- Input parsing.
- Trigger-aware cost evaluation.
- Greedy with Backtracking.
- Genetic Algorithm.
- Simulated Annealing.
- Graph and route visualization.

## 9. Experimental Results

The implementation has been tested using three synthetic instances.

| Instance | Nodes | Arcs | Trigger Relations | Optimal Cost |
|---|---:|---:|---:|---:|
| Test 1 | 4 | 12 | 3 | 29 |
| Test 2 | 5 | 20 | 4 | 46 |
| Test 3 | 6 | 30 | 6 | 49 |

For these small instances, exhaustive enumeration was used to independently verify the optimal costs.

The three implemented algorithms achieved the following results:

| Instance | Greedy | Genetic Algorithm | Simulated Annealing |
|---|---:|---:|---:|
| Test 1 | 29 | 29 | 29 |
| Test 2 | 46 | 46 | 46 |
| Test 3 | 54 | 49 | 49 |

The results demonstrate that different algorithmic approaches may produce different solution qualities. In particular, Greedy with Backtracking did not find the optimal solution for the third instance, while both metaheuristics did.

These are experimental results on synthetic test instances, not official benchmark results.

## 10. Limitations

- Greedy with Backtracking does not guarantee a globally optimal solution.
- Genetic Algorithm and Simulated Annealing are stochastic metaheuristics and do not guarantee an optimal solution.
- Search procedures involving backtracking may require exponential time in the worst case.
- Experimental results on small synthetic instances do not establish performance on larger benchmark instances.

## 11. Technologies

- Python
- NetworkX
- Matplotlib
- unittest

## 12. License

This project was developed for academic purposes.
