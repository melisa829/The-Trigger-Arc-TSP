
from src.graph import Graph
from src.cost_evaluator import evaluate_route_cost


def greedy_algorithm(graph: Graph) -> tuple[list[int], float]:
    """
    Constructs a route using a greedy strategy.

    At each step, selects the cheapest outgoing arc
    that leads to an unvisited node.

    The route starts and ends at the depot.
    """

    current_node = graph.depot

    # Track visited nodes.
    visited_nodes = {current_node}

    # Store the selected arc IDs.
    route = []

    # Store pending trigger costs.
    pending_costs = {}

    # Create a dictionary for quick arc lookup.
    arcs_by_id = {
        arc.id: arc
        for arc in graph.arcs
    }

    # Group relations by trigger arc.
    relations_by_trigger = {}

    for relation in graph.relations:
        relations_by_trigger.setdefault(
            relation.trigger_arc_id, []
        ).append(relation)

    # Visit every node.
    while len(visited_nodes) < graph.num_nodes:

        candidates = [
            arc
            for arc in graph.arcs
            if arc.tail == current_node
            and arc.head not in visited_nodes
        ]

        if not candidates:
            raise ValueError(
                f"No valid outgoing arc from node {current_node}."
            )

        # Select the cheapest candidate using its current cost.
        selected_arc = min(
            candidates,
            key=lambda arc: pending_costs.get(
                arc.id, arc.cost
            )
        )

        route.append(selected_arc.id)

        visited_nodes.add(selected_arc.head)

        current_node = selected_arc.head

        # Apply trigger effects to targets not yet traversed.
        for relation in relations_by_trigger.get(
            selected_arc.id, []
        ):
            target_id = relation.target_arc_id

            if target_id not in route:
                pending_costs[target_id] = relation.new_cost

    # Find an arc that returns to the depot.
    return_candidates = [
        arc
        for arc in graph.arcs
        if arc.tail == current_node
        and arc.head == graph.depot
    ]

    if not return_candidates:
        raise ValueError(
            f"No valid arc from node {current_node} "
            "back to the depot."
        )

    return_arc = min(
        return_candidates,
        key=lambda arc: pending_costs.get(
            arc.id, arc.cost
        )
    )

    route.append(return_arc.id)

    # Calculate the exact total route cost.
    total_cost = evaluate_route_cost(graph, route)

    return route, total_cost
