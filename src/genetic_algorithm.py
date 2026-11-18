
import random

from src.graph import Graph
from src.cost_evaluator import evaluate_route_cost


def is_valid_route(graph: Graph, route: list[int]) -> bool:
    """
    Checks whether a route is a valid Hamiltonian cycle.
    """

    if len(route) != graph.num_nodes:
        return False

    arcs_by_id = {
        arc.id: arc
        for arc in graph.arcs
    }

    if any(arc_id not in arcs_by_id for arc_id in route):
        return False

    if len(set(route)) != len(route):
        return False

    current_node = graph.depot
    visited_nodes = {graph.depot}

    for index, arc_id in enumerate(route):
        arc = arcs_by_id[arc_id]

        if arc.tail != current_node:
            return False

        current_node = arc.head

        if index < len(route) - 1:
            if current_node in visited_nodes:
                return False

            visited_nodes.add(current_node)

    return (
        current_node == graph.depot
        and len(visited_nodes) == graph.num_nodes
    )


def generate_random_route(
    graph: Graph
) -> list[int] | None:
    """
    Generates a random valid Hamiltonian cycle using backtracking.
    """

    def search(
        current_node: int,
        visited_nodes: set[int],
        route: list[int]
    ) -> list[int] | None:

        if len(visited_nodes) == graph.num_nodes:

            return_candidates = [
                arc for arc in graph.arcs
                if arc.tail == current_node
                and arc.head == graph.depot
                and arc.id not in route
            ]

            random.shuffle(return_candidates)

            if return_candidates:
                return route + [return_candidates[0].id]

            return None

        candidates = [
            arc for arc in graph.arcs
            if arc.tail == current_node
            and arc.head not in visited_nodes
            and arc.id not in route
        ]

        random.shuffle(candidates)

        for arc in candidates:

            result = search(
                arc.head,
                visited_nodes | {arc.head},
                route + [arc.id]
            )

            if result is not None:
                return result

        return None

    return search(
        graph.depot,
        {graph.depot},
        []
    )


def generate_initial_population(
    graph: Graph,
    population_size: int
) -> list[list[int]]:
    """
    Generates the initial population of valid Hamiltonian cycles.
    """

    if population_size <= 0:
        raise ValueError(
            "Population size must be greater than zero."
        )

    population = []
    max_attempts = population_size * 100

    for _ in range(max_attempts):

        if len(population) == population_size:
            break

        route = generate_random_route(graph)

        if route is not None:
            population.append(route)

    if not population:
        raise ValueError(
            "No valid Hamiltonian cycle exists or could be generated."
        )

    while len(population) < population_size:
        population.append(
            random.choice(population).copy()
        )

    return population


def calculate_fitness(
    graph: Graph,
    route: list[int]
) -> float:
    """
    Calculates fitness based on route cost.

    Lower costs produce higher fitness values.
    """

    route_cost = evaluate_route_cost(graph, route)

    return 1 / (1 + route_cost)


def select_parent(
    population: list[list[int]],
    fitness_scores: list[float],
    tournament_size: int = 3
) -> list[int]:
    """
    Selects a parent using Tournament Selection.
    """

    if not population:
        raise ValueError("Population cannot be empty.")

    if len(population) != len(fitness_scores):
        raise ValueError(
            "Population and fitness scores must have equal lengths."
        )

    if tournament_size <= 0:
        raise ValueError(
            "Tournament size must be greater than zero."
        )

    tournament_size = min(
        tournament_size,
        len(population)
    )

    selected_indices = random.sample(
        range(len(population)),
        tournament_size
    )

    winner_index = max(
        selected_indices,
        key=lambda index: fitness_scores[index]
    )

    return population[winner_index].copy()


def crossover(
    graph: Graph,
    parent1: list[int],
    parent2: list[int]
) -> list[int]:
    """
    Creates a child by combining two valid Hamiltonian cycles.

    A prefix from parent1 is preserved.
    The remaining route prefers arcs from parent2.
    Backtracking guarantees a valid completion when one is found.
    """

    if not is_valid_route(graph, parent1):
        raise ValueError("Parent 1 is not a valid Hamiltonian cycle.")

    if not is_valid_route(graph, parent2):
        raise ValueError("Parent 2 is not a valid Hamiltonian cycle.")

    if graph.num_nodes == 1:
        return parent1.copy()

    cut_point = random.randint(
        1,
        graph.num_nodes - 1
    )

    route_prefix = parent1[:cut_point]

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

    parent2_positions = {
        arc_id: index
        for index, arc_id in enumerate(parent2)
    }

    def search(
        node: int,
        visited: set[int],
        used: set[int],
        route: list[int]
    ) -> list[int] | None:

        if len(visited) == graph.num_nodes:

            return_candidates = [
                arc for arc in graph.arcs
                if arc.tail == node
                and arc.head == graph.depot
                and arc.id not in used
            ]

            return_candidates.sort(
                key=lambda arc: (
                    arc.id not in parent2_positions,
                    parent2_positions.get(
                        arc.id,
                        float("inf")
                    )
                )
            )

            if return_candidates:
                return route + [return_candidates[0].id]

            return None

        candidates = [
            arc for arc in graph.arcs
            if arc.tail == node
            and arc.head not in visited
            and arc.id not in used
        ]

        candidates.sort(
            key=lambda arc: (
                arc.id not in parent2_positions,
                parent2_positions.get(
                    arc.id,
                    float("inf")
                )
            )
        )

        for arc in candidates:

            result = search(
                arc.head,
                visited | {arc.head},
                used | {arc.id},
                route + [arc.id]
            )

            if result is not None:
                return result

        return None

    child = search(
        current_node,
        visited_nodes,
        used_arcs,
        route_prefix
    )

    if child is None:
        return parent1.copy()

    return child


def mutate(
    graph: Graph,
    route: list[int],
    mutation_rate: float = 0.1
) -> list[int]:
    """
    Mutates a route while preserving Hamiltonian cycle validity.
    """

    if not 0 <= mutation_rate <= 1:
        raise ValueError(
            "Mutation rate must be between 0 and 1."
        )

    if not is_valid_route(graph, route):
        raise ValueError("Cannot mutate an invalid route.")

    if random.random() >= mutation_rate:
        return route.copy()

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

    mutated_route = search(
        current_node,
        visited_nodes,
        used_arcs,
        route_prefix
    )

    if mutated_route is None:
        return route.copy()

    return mutated_route


def genetic_algorithm(
    graph: Graph,
    population_size: int = 50,
    generations: int = 100,
    crossover_rate: float = 0.8,
    mutation_rate: float = 0.1,
    tournament_size: int = 3,
    elitism_count: int = 1
) -> tuple[list[int], float]:
    """
    Executes the Genetic Algorithm for the Trigger Arc TSP.

    Returns:
        A tuple containing the best route and its total cost.
    """

    if population_size < 2:
        raise ValueError(
            "Population size must be at least 2."
        )

    if generations < 0:
        raise ValueError(
            "Generations cannot be negative."
        )

    if not 0 <= crossover_rate <= 1:
        raise ValueError(
            "Crossover rate must be between 0 and 1."
        )

    if not 0 <= mutation_rate <= 1:
        raise ValueError(
            "Mutation rate must be between 0 and 1."
        )

    if tournament_size <= 0:
        raise ValueError(
            "Tournament size must be greater than zero."
        )

    if not 1 <= elitism_count < population_size:
        raise ValueError(
            "Elitism count must be at least 1 "
            "and smaller than population size."
        )

    # Generate the initial population.
    population = generate_initial_population(
        graph,
        population_size
    )

    # Find the best initial solution.
    best_route = min(
        population,
        key=lambda route: evaluate_route_cost(graph, route)
    ).copy()

    best_cost = evaluate_route_cost(
        graph,
        best_route
    )

    # Execute the generations.
    for _ in range(generations):

        # Calculate fitness for every individual.
        fitness_scores = [
            calculate_fitness(graph, route)
            for route in population
        ]

        # Sort individuals by fitness, highest first.
        ranked_population = sorted(
            zip(population, fitness_scores),
            key=lambda item: item[1],
            reverse=True
        )

        # Preserve the best individuals (elitism).
        new_population = [
            route.copy()
            for route, _ in ranked_population[:elitism_count]
        ]

        # Create the rest of the new population.
        while len(new_population) < population_size:

            parent1 = select_parent(
                population,
                fitness_scores,
                tournament_size
            )

            parent2 = select_parent(
                population,
                fitness_scores,
                tournament_size
            )

            # Apply crossover with the specified probability.
            if random.random() < crossover_rate:
                child = crossover(
                    graph,
                    parent1,
                    parent2
                )
            else:
                child = parent1.copy()

            # Apply mutation.
            child = mutate(
                graph,
                child,
                mutation_rate
            )

            new_population.append(child)

        population = new_population

        # Update the best solution found so far.
        generation_best = min(
            population,
            key=lambda route: evaluate_route_cost(graph, route)
        )

        generation_best_cost = evaluate_route_cost(
            graph,
            generation_best
        )

        if generation_best_cost < best_cost:
            best_route = generation_best.copy()
            best_cost = generation_best_cost

    return best_route, best_cost
