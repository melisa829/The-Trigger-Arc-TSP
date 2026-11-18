
import argparse
import time

from src.parser import parse_instance
from src.cost_evaluator import evaluate_route_cost
from src.greedy import greedy_algorithm
from src.genetic_algorithm import genetic_algorithm
from src.simulated_annealing import simulated_annealing
from src.visualization import draw_graph, draw_route


def run_greedy(graph):
    start_time = time.perf_counter()

    route, cost = greedy_algorithm(graph)

    execution_time = time.perf_counter() - start_time

    return route, cost, execution_time


def run_genetic_algorithm(graph):
    start_time = time.perf_counter()

    route, cost = genetic_algorithm(graph)

    execution_time = time.perf_counter() - start_time

    return route, cost, execution_time


def run_simulated_annealing(graph):
    start_time = time.perf_counter()

    route, cost = simulated_annealing(graph)

    execution_time = time.perf_counter() - start_time

    return route, cost, execution_time


def display_result(
    algorithm_name,
    graph,
    route,
    cost,
    execution_time
):
    print("\n" + "=" * 50)
    print(f"Algorithm: {algorithm_name}")
    print("=" * 50)

    print(f"Route (arc IDs): {route}")
    print(f"Total cost: {cost:.2f}")
    print(f"Execution time: {execution_time:.6f} seconds")

    # Verify the reported cost.
    verified_cost = evaluate_route_cost(
        graph,
        route
    )

    print(f"Verified cost: {verified_cost:.2f}")

    print("=" * 50)


def run_algorithm(graph, algorithm_name):
    """
    Executes the selected algorithm and returns its result.
    """

    algorithms = {
        "greedy": run_greedy,
        "genetic": run_genetic_algorithm,
        "annealing": run_simulated_annealing
    }

    if algorithm_name not in algorithms:
        raise ValueError(
            f"Unknown algorithm: {algorithm_name}"
        )

    return algorithms[algorithm_name](graph)


def compare_algorithms(graph):
    """
    Executes all algorithms and compares their results.
    """

    algorithms = [
        ("Greedy", run_greedy),
        ("Genetic Algorithm", run_genetic_algorithm),
        ("Simulated Annealing", run_simulated_annealing)
    ]

    results = []

    print("\nSTARTING ALGORITHM COMPARISON")

    for name, algorithm in algorithms:

        print(f"\nRunning {name}...")

        try:
            route, cost, execution_time = algorithm(graph)

            display_result(
                name,
                graph,
                route,
                cost,
                execution_time
            )

            results.append({
                "name": name,
                "route": route,
                "cost": cost,
                "time": execution_time
            })

        except ValueError as error:
            print(f"{name} could not find a solution: {error}")

    if not results:
        print("\nNo algorithm produced a valid solution.")
        return []

    print("\n" + "=" * 65)
    print("FINAL COMPARISON")
    print("=" * 65)

    print(
        f"{'Algorithm':<25}"
        f"{'Total Cost':<18}"
        f"{'Time (seconds)':<20}"
    )

    print("-" * 65)

    for result in results:
        print(
            f"{result['name']:<25}"
            f"{result['cost']:<18.2f}"
            f"{result['time']:<20.6f}"
        )

    best_result = min(
        results,
        key=lambda result: result["cost"]
    )

    print("-" * 65)
    print(f"Best solution: {best_result['name']}")
    print(f"Best cost: {best_result['cost']:.2f}")
    print(f"Best route: {best_result['route']}")
    print("=" * 65)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="The Trigger Arc TSP Solver"
    )

    parser.add_argument(
        "input_file",
        help="Path to the input instance file"
    )

    parser.add_argument(
        "--algorithm",
        choices=["greedy", "genetic", "annealing", "all"],
        default="all",
        help="Algorithm to execute"
    )

    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Display graph and solution visualizations"
    )

    args = parser.parse_args()

    try:
        graph = parse_instance(args.input_file)

        print("\nTHE TRIGGER ARC TSP")
        print("=" * 50)
        print(f"Number of nodes: {graph.num_nodes}")
        print(f"Number of arcs: {len(graph.arcs)}")
        print(f"Number of trigger relations: {len(graph.relations)}")
        print(f"Depot node: {graph.depot}")
        print("=" * 50)

        if args.visualize:
            draw_graph(graph)

        if args.algorithm == "all":
            results = compare_algorithms(graph)

        else:
            route, cost, execution_time = run_algorithm(
                graph,
                args.algorithm
            )

            display_result(
                args.algorithm,
                graph,
                route,
                cost,
                execution_time
            )

            results = [{
                "name": args.algorithm,
                "route": route,
                "cost": cost,
                "time": execution_time
            }]

        if args.visualize:
            for result in results:
                draw_route(
                    graph,
                    result["route"],
                    title=f"{result['name']} - Cost: {result['cost']:.2f}"
                )

    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' was not found.")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
