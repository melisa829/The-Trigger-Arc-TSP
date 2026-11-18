
from src.graph import Graph
from src.cost_evaluator import evaluate_route_cost


def greedy_algorithm(graph: Graph) -> tuple[list[int], float]:
    """
    Constructs a Hamiltonian cycle using a greedy strategy
    combined with backtracking.

    At each step, outgoing arcs are sorted by their current
    costs. The cheapest arc is tried first.

    If a choice leads to a dead end, the algorithm backtracks
    and tries the next candidate.

    The route starts and ends at the depot and visits every
    node exactly once.
    """

    # Group relations by their trigger arc.
    relations_by_trigger = {}

    for relation in graph.relations:
        relations_by_trigger.setdefault(
            relation.trigger_arc_id, []
        ).append(relation)

    def search(
        current_node: int,
        visited_nodes: set[int],
        route: list[int],
        pending_costs: dict[int, float],
        traversed_arcs: set[int]
    ) -> list[int] | None:

        # If every node has been visited, try to return
        # to the depot.
        if len(visited_nodes) == graph.num_nodes:

            return_candidates = [
                arc for arc in graph.arcs
                if arc.tail == current_node
                and arc.head == graph.depot
                and arc.id not in traversed_arcs
            ]

            return_candidates.sort(
                key=lambda arc: pending_costs.get(
                    arc.id, arc.cost
                )
            )

            if return_candidates:
                return route + [return_candidates[0].id]

            return None

        # Find outgoing arcs leading to unvisited nodes.
        candidates = [
            arc for arc in graph.arcs
            if arc.tail == current_node
            and arc.head not in visited_nodes
            and arc.id not in traversed_arcs
        ]

        # Try the cheapest candidate first.
        candidates.sort(
            key=lambda arc: pending_costs.get(
                arc.id, arc.cost
            )
        )

        for selected_arc in candidates:

            # Create independent state for this attempt.
            new_route = route + [selected_arc.id]

            new_visited_nodes = visited_nodes | {
                selected_arc.head
            }

            new_traversed_arcs = traversed_arcs | {
                selected_arc.id
            }

            new_pending_costs = pending_costs.copy()

            # Apply trigger effects to targets that have
            # not yet been traversed.
            for relation in relations_by_trigger.get(
                selected_arc.id, []
            ):

                target_id = relation.target_arc_id

                if target_id not in new_traversed_arcs:
                    new_pending_costs[target_id] = (
                        relation.new_cost
                    )

            # Recursively try to complete the route.
            result = search(
                current_node=selected_arc.head,
                visited_nodes=new_visited_nodes,
                route=new_route,
                pending_costs=new_pending_costs,
                traversed_arcs=new_traversed_arcs
            )

            # If a valid cycle was found, return it.
            if result is not None:
                return result

        # No candidate produced a valid Hamiltonian cycle.
        return None

    # Start searching from the depot.
    route = search(
        current_node=graph.depot,
        visited_nodes={graph.depot},
        route=[],
        pending_costs={},
        traversed_arcs=set()
    )

    if route is None:
        raise ValueError(
            "No valid Hamiltonian cycle exists for this graph."
        )

    # Calculate the exact total cost, including trigger effects.
    total_cost = evaluate_route_cost(graph, route)

    return route, total_cost
