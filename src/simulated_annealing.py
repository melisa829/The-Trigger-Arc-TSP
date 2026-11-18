
import math
import random

from src.graph import Graph
from src.cost_evaluator import evaluate_route_cost
from src.genetic_algorithm import (
    generate_random_route,
    is_valid_route
)


def generate_neighbor(
    graph: Graph,
    route: list[int]
) -> list[int]:
    """
    Generates a neighboring valid Hamiltonian cycle.

    A random prefix of the current route is preserved.
    The remaining route is rebuilt using randomized backtracking.
    """

    if not is_valid_route(graph, route):
        raise ValueError("Cannot generate a neighbor from an invalid route.")

    if graph.num_nodes == 1:
        return route.copy()

    cut_point = random.randint(
        0,
        graph.num_nodes - 1
    )

    route_prefix = route[:cut_point]

    arcs_by_id = {
        arc.id: arc
        for arc in graph.arcs
    }

    current_node = graph.depot
    visited_nodes = {graph.depot}
    used_arcs = set()

    for arc_id in route_prefix:
        arc = arcs_by_id[arc_id]

        current_node = arc.head
        visited_nodes.add(current_node)
        used_arcs.add(arc_id)

    def search(
        node: int,
        visited: set[int],
        used: set[int],
        new_route: list[int]
    ) -> list[int] | None:

        if len(visited) == graph.num_nodes:

            return_candidates = [
                arc for arc in graph.arcs
                if arc.tail == node
                and arc.head == graph.depot
                and arc.id not in used
            ]

            random.shuffle(return_candidates)

            if return_candidates:
                return new_route + [
                    return_candidates[0].id
                ]

            return None

        candidates = [
            arc for arc in graph.arcs
            if arc.tail == node
            and arc.head not in visited
            and arc.id not in used
        ]

        random.shuffle(candidates)

        for arc in candidates:

            result = search(
                arc.head,
                visited | {arc.head},
                used | {arc.id},
                new_route + [arc.id]
            )

            if result is not None:
                return result

        return None

    neighbor = search(
        current_node,
        visited_nodes,
        used_arcs,
        route_prefix
    )

    if neighbor is None:
        return route.copy()

    return neighbor


def acceptance_probability(
    current_cost: float,
    neighbor_cost: float,
    temperature: float
) -> float:
    """
    Calculates the probability of accepting a neighboring solution.

    Better solutions are always accepted.
    Worse solutions may be accepted depending on temperature.
    """

    if temperature <= 0:
        raise ValueError("Temperature must be greater than zero.")

    if neighbor_cost < current_cost:
        return 1.0

    return math.exp(
        -(neighbor_cost - current_cost) / temperature
    )


def simulated_annealing(
    graph: Graph,
    initial_temperature: float = 1000.0,
    cooling_rate: float = 0.995,
    minimum_temperature: float = 0.01,
    max_iterations: int = 1000
) -> tuple[list[int], float]:
    """
    Executes Simulated Annealing for the Trigger Arc TSP.

    Returns:
        A tuple containing the best route and its total cost.
    """

    if initial_temperature <= 0:
        raise ValueError(
            "Initial temperature must be greater than zero."
        )

    if not 0 < cooling_rate < 1:
        raise ValueError(
            "Cooling rate must be between 0 and 1."
        )

    if minimum_temperature <= 0:
        raise ValueError(
            "Minimum temperature must be greater than zero."
        )

    if minimum_temperature >= initial_temperature:
        raise ValueError(
            "Minimum temperature must be lower than initial temperature."
        )

    if max_iterations < 0:
        raise ValueError(
            "Maximum iterations cannot be negative."
        )

    # Generate the initial solution.
    current_route = generate_random_route(graph)

    if current_route is None:
        raise ValueError(
            "No valid Hamiltonian cycle exists in the graph."
        )

    current_cost = evaluate_route_cost(
        graph,
        current_route
    )

    # Store the best solution found so far.
    best_route = current_route.copy()
    best_cost = current_cost

    temperature = initial_temperature

    # Main Simulated Annealing loop.
    for _ in range(max_iterations):

        if temperature <= minimum_temperature:
            break

        # Generate a neighboring solution.
        neighbor_route = generate_neighbor(
            graph,
            current_route
        )

        neighbor_cost = evaluate_route_cost(
            graph,
            neighbor_route
        )

        # Calculate the acceptance probability.
        probability = acceptance_probability(
            current_cost,
            neighbor_cost,
            temperature
        )

        # Decide whether to accept the neighboring solution.
        if random.random() < probability:
            current_route = neighbor_route
            current_cost = neighbor_cost

        # Update the best solution.
        if current_cost < best_cost:
            best_route = current_route.copy()
            best_cost = current_cost

        # Reduce the temperature.
        temperature *= cooling_rate

    return best_route, best_cost
