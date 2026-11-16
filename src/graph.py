
from dataclasses import dataclass


@dataclass
class Arc:
    """
    Represents a directed arc in the graph.
    """

    id: int
    tail: int
    head: int
    cost: float


@dataclass
class TriggerRelation:
    """
    Represents a trigger-target relationship between two arcs.
    """

    id: int
    trigger_arc_id: int
    target_arc_id: int
    new_cost: float


@dataclass
class Graph:
    """
    Represents the directed graph for the Trigger Arc TSP problem.
    """

    num_nodes: int
    arcs: list[Arc]
    relations: list[TriggerRelation]
    depot: int = 0

    def __post_init__(self):
        # Check the number of nodes.
        if self.num_nodes <= 0:
            raise ValueError("The graph must have at least one node.")

        # Check that the depot is a valid node.
        if not 0 <= self.depot < self.num_nodes:
            raise ValueError("The depot is not a valid node.")

        # Check that arc IDs are unique.
        arc_ids = [arc.id for arc in self.arcs]

        if len(arc_ids) != len(set(arc_ids)):
            raise ValueError("Arc IDs must be unique.")

        # Check that every arc has valid endpoints and cost.
        for arc in self.arcs:
            if not (0 <= arc.tail < self.num_nodes):
                raise ValueError(f"Invalid tail node in arc {arc.id}.")

            if not (0 <= arc.head < self.num_nodes):
                raise ValueError(f"Invalid head node in arc {arc.id}.")

            if arc.cost < 0:
                raise ValueError(f"Invalid cost in arc {arc.id}.")

        # Check that relation IDs are unique.
        relation_ids = [relation.id for relation in self.relations]

        if len(relation_ids) != len(set(relation_ids)):
            raise ValueError("Relation IDs must be unique.")

        # Check that all referenced arcs exist.
        for relation in self.relations:
            if relation.trigger_arc_id not in arc_ids:
                raise ValueError(
                    f"Trigger arc {relation.trigger_arc_id} does not exist."
                )

            if relation.target_arc_id not in arc_ids:
                raise ValueError(
                    f"Target arc {relation.target_arc_id} does not exist."
                )

            if relation.new_cost < 0:
                raise ValueError(
                    f"Invalid new cost in relation {relation.id}."
                )
