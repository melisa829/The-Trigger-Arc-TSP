
from src.graph import Graph


def evaluate_route_cost(graph: Graph, route: list[int]) -> float:
    """
    Calculates the total cost of a route while considering
    trigger-target relationships.

    A trigger arc can change the cost of a target arc,
    but only if the target arc has not been traversed yet.

    If multiple triggers affect the same target arc,
    the most recently traversed trigger determines its cost.
    """

    # Create a dictionary for quick access to arcs by ID.
    arcs_by_id = {
        arc.id: arc
        for arc in graph.arcs
    }

    # Group trigger relations by their trigger arc.
    relations_by_trigger = {}

    for relation in graph.relations:
        relations_by_trigger.setdefault(
            relation.trigger_arc_id, []
        ).append(relation)

    # Store the new costs assigned to target arcs.
    pending_costs = {}

    # Keep track of arcs that have already been traversed.
    traversed_arcs = set()

    total_cost = 0.0

    # Process the route in its given order.
    for arc_id in route:

        if arc_id not in arcs_by_id:
            raise ValueError(f"Arc {arc_id} does not exist.")

        arc = arcs_by_id[arc_id]

        # Use the updated cost if one exists;
        # otherwise, use the original cost.
        current_cost = pending_costs.get(
            arc_id, arc.cost
        )

        total_cost += current_cost

        # Mark the current arc as traversed.
        traversed_arcs.add(arc_id)

        # Apply trigger effects to target arcs
        # that have not been traversed yet.
        for relation in relations_by_trigger.get(arc_id, []):

            target_id = relation.target_arc_id

            if target_id not in traversed_arcs:
                pending_costs[target_id] = relation.new_cost

    return total_cost
