
from pathlib import Path

from src.graph import Arc, TriggerRelation, Graph


def parse_instance(file_path: str) -> Graph:
    """
    Reads a Trigger Arc TSP instance from a text file
    and returns a Graph object.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Instance file not found: {file_path}")

    with path.open("r", encoding="utf-8") as file:
        lines = [
            line.strip()
            for line in file
            if line.strip()
        ]

    if not lines:
        raise ValueError("The instance file is empty.")

    # Read the number of nodes, arcs and relations.
    try:
        num_nodes, num_arcs, num_relations = map(
            int, lines[0].split()
        )
    except ValueError:
        raise ValueError("Invalid instance header.")

    expected_lines = 1 + num_arcs + num_relations

    if len(lines) != expected_lines:
        raise ValueError(
            f"Expected {expected_lines} lines, "
            f"but found {len(lines)}."
        )

    arcs = []

    # Read arc information.
    for i in range(1, 1 + num_arcs):
        try:
            arc_id, tail, head, cost = lines[i].split()

            arcs.append(
                Arc(
                    id=int(arc_id),
                    tail=int(tail),
                    head=int(head),
                    cost=float(cost)
                )
            )
        except ValueError:
            raise ValueError(f"Invalid arc data on line {i + 1}.")

    relations = []

    # Read trigger-target relationships.
    for i in range(1 + num_arcs, expected_lines):
        try:
            trigger_id, target_id, new_cost = lines[i].split()

            relations.append(
                TriggerRelation(
                    id=len(relations),
                    trigger_arc_id=int(trigger_id),
                    target_arc_id=int(target_id),
                    new_cost=float(new_cost)
                )
            )
        except ValueError:
            raise ValueError(
                f"Invalid trigger relation on line {i + 1}."
            )

    return Graph(
        num_nodes=num_nodes,
        arcs=arcs,
        relations=relations,
        depot=0
    )
