
import matplotlib.pyplot as plt
import networkx as nx

from collections import defaultdict

from src.graph import Graph


def create_graph_visualization(
    graph: Graph
) -> tuple[nx.MultiDiGraph, dict]:
    """
    Creates a directed multigraph from the Trigger Arc TSP instance.

    A MultiDiGraph preserves parallel arcs with different IDs and costs.

    Returns:
        The NetworkX multigraph and the node positions.
    """

    visual_graph = nx.MultiDiGraph()

    for node in range(graph.num_nodes):
        visual_graph.add_node(node)

    for arc in graph.arcs:
        visual_graph.add_edge(
            arc.tail,
            arc.head,
            key=arc.id,
            arc_id=arc.id,
            cost=arc.cost
        )

    positions = nx.spring_layout(
        visual_graph,
        seed=42
    )

    return visual_graph, positions


def _calculate_edge_curvatures(graph: Graph) -> dict:
    """
    Calculates different curvature values for parallel arcs.

    This prevents parallel arcs from being drawn on top of each other.
    """

    grouped_arcs = defaultdict(list)

    for arc in graph.arcs:
        grouped_arcs[(arc.tail, arc.head)].append(arc)

    curvatures = {}

    for arcs in grouped_arcs.values():
        count = len(arcs)

        for index, arc in enumerate(arcs):
            if count == 1:
                curvature = 0.12
            else:
                curvature = (
                    index - (count - 1) / 2
                ) * 0.3

            curvatures[arc.id] = curvature

    return curvatures


def _draw_arcs(
    graph: Graph,
    positions: dict,
    color: str,
    width: float = 1.5,
    arrowsize: int = 20,
    selected_arc_ids: set | None = None
) -> None:
    """
    Draws arcs individually, preserving parallel arcs.

    Each arc is identified by its unique ID.
    """

    curvatures = _calculate_edge_curvatures(graph)

    for arc in graph.arcs:

        if (
            selected_arc_ids is not None
            and arc.id not in selected_arc_ids
        ):
            continue

        nx.draw_networkx_edges(
            nx.MultiDiGraph([
                (
                    arc.tail,
                    arc.head,
                    {
                        "arc_id": arc.id,
                        "cost": arc.cost
                    }
                )
            ]),
            positions,
            edgelist=[(arc.tail, arc.head, 0)],
            edge_color=color,
            width=width,
            arrows=True,
            arrowsize=arrowsize,
            connectionstyle=(
                f"arc3,rad={curvatures[arc.id]}"
            )
        )


def _draw_arc_labels(
    graph: Graph,
    positions: dict
) -> None:
    """
    Draws labels for every arc separately.

    Labels contain the arc ID and its original cost.
    """

    grouped_arcs = defaultdict(list)

    for arc in graph.arcs:
        grouped_arcs[(arc.tail, arc.head)].append(arc)

    for arcs in grouped_arcs.values():

        count = len(arcs)

        for index, arc in enumerate(arcs):

            x1, y1 = positions[arc.tail]
            x2, y2 = positions[arc.head]

            dx = x2 - x1
            dy = y2 - y1

            if dx == 0 and dy == 0:
                label_x = x1
                label_y = y1
            else:
                offset = (
                    index - (count - 1) / 2
                ) * 0.08

                if count == 1:
                    offset = 0.04

                label_x = (
                    (x1 + x2) / 2
                    - dy * offset
                )

                label_y = (
                    (y1 + y2) / 2
                    + dx * offset
                )

            plt.text(
                label_x,
                label_y,
                f"A{arc.id}: {arc.cost}",
                fontsize=8,
                ha="center",
                va="center",
                bbox={
                    "facecolor": "white",
                    "edgecolor": "none",
                    "alpha": 0.75
                }
            )


def _draw_nodes(
    graph: Graph,
    visual_graph: nx.MultiDiGraph,
    positions: dict
) -> None:
    """
    Draws graph nodes and their labels.

    The depot is highlighted in orange.
    """

    node_colors = [
        "orange" if node == graph.depot else "skyblue"
        for node in visual_graph.nodes()
    ]

    nx.draw_networkx_nodes(
        visual_graph,
        positions,
        node_color=node_colors,
        node_size=900
    )

    nx.draw_networkx_labels(
        visual_graph,
        positions,
        font_size=11,
        font_weight="bold"
    )


def draw_graph(
    graph: Graph,
    show: bool = True,
    save_path: str | None = None
) -> None:
    """
    Draws the original directed multigraph.

    The depot is highlighted separately.
    Every arc has its own ID and original cost.
    Parallel arcs are displayed separately.
    """

    visual_graph, positions = create_graph_visualization(
        graph
    )

    plt.figure(figsize=(10, 7))

    _draw_nodes(
        graph,
        visual_graph,
        positions
    )

    _draw_arcs(
        graph,
        positions,
        color="gray",
        width=1.5,
        arrowsize=20
    )

    _draw_arc_labels(
        graph,
        positions
    )

    plt.title("Trigger Arc TSP - Original Graph")
    plt.axis("off")
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    if show:
        plt.show()
    else:
        plt.close()


def draw_route(
    graph: Graph,
    route: list[int],
    title: str = "Trigger Arc TSP - Solution Route",
    show: bool = True,
    save_path: str | None = None
) -> None:
    """
    Draws a Hamiltonian cycle on the original graph.

    Selected route arcs are highlighted in red.
    Other arcs remain visible in the background.

    The route is validated before drawing.
    """

    arcs_by_id = {
        arc.id: arc
        for arc in graph.arcs
    }

    if len(route) != graph.num_nodes:
        raise ValueError(
            "The route must contain exactly one arc per node."
        )

    if any(arc_id not in arcs_by_id for arc_id in route):
        raise ValueError(
            "The route contains an unknown arc ID."
        )

    if len(set(route)) != len(route):
        raise ValueError(
            "The route cannot contain repeated arcs."
        )

    current_node = graph.depot
    visited_nodes = {graph.depot}

    for index, arc_id in enumerate(route):
        arc = arcs_by_id[arc_id]

        if arc.tail != current_node:
            raise ValueError(
                "The route contains disconnected arcs."
            )

        current_node = arc.head

        if index < len(route) - 1:
            if current_node in visited_nodes:
                raise ValueError(
                    "The route visits a node more than once."
                )

            visited_nodes.add(current_node)

    if (
        current_node != graph.depot
        or len(visited_nodes) != graph.num_nodes
    ):
        raise ValueError(
            "The route is not a valid Hamiltonian cycle."
        )

    visual_graph, positions = create_graph_visualization(
        graph
    )

    plt.figure(figsize=(10, 7))

    _draw_nodes(
        graph,
        visual_graph,
        positions
    )

    # Draw all original arcs in the background.
    _draw_arcs(
        graph,
        positions,
        color="lightgray",
        width=1.5,
        arrowsize=15
    )

    # Highlight the selected route arcs in red.
    _draw_arcs(
        graph,
        positions,
        color="red",
        width=2.8,
        arrowsize=25,
        selected_arc_ids=set(route)
    )

    _draw_arc_labels(
        graph,
        positions
    )

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    if show:
        plt.show()
    else:
        plt.close()
