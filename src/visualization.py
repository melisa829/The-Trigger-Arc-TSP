
import matplotlib.pyplot as plt
import networkx as nx

from src.graph import Graph


def create_graph_visualization(
    graph: Graph
) -> tuple[nx.DiGraph, dict]:
    """
    Creates a directed graph from the Trigger Arc TSP instance.

    Returns:
        The NetworkX graph and the node positions.
    """

    visual_graph = nx.DiGraph()

    for node in range(graph.num_nodes):
        visual_graph.add_node(node)

    for arc in graph.arcs:
        visual_graph.add_edge(
            arc.tail,
            arc.head,
            arc_id=arc.id,
            cost=arc.cost
        )

    positions = nx.spring_layout(
        visual_graph,
        seed=42
    )

    return visual_graph, positions


def draw_graph(
    graph: Graph,
    show: bool = True,
    save_path: str | None = None
) -> None:
    """
    Draws the original directed graph.

    The depot is highlighted separately.
    Arc labels contain their IDs and original costs.
    """

    visual_graph, positions = create_graph_visualization(
        graph
    )

    plt.figure(figsize=(10, 7))

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

    nx.draw_networkx_edges(
        visual_graph,
        positions,
        edge_color="gray",
        arrows=True,
        arrowsize=20,
        connectionstyle="arc3,rad=0.1"
    )

    edge_labels = {
        (arc.tail, arc.head): (
            f"A{arc.id}: {arc.cost}"
        )
        for arc in graph.arcs
    }

    nx.draw_networkx_edge_labels(
        visual_graph,
        positions,
        edge_labels=edge_labels,
        font_size=8
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

    Selected route arcs are highlighted.
    Other arcs remain visible in the background.
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

    nx.draw_networkx_edges(
        visual_graph,
        positions,
        edge_color="lightgray",
        arrows=True,
        arrowsize=15,
        connectionstyle="arc3,rad=0.1"
    )

    route_edges = [
        (
            arcs_by_id[arc_id].tail,
            arcs_by_id[arc_id].head
        )
        for arc_id in route
    ]

    nx.draw_networkx_edges(
        visual_graph,
        positions,
        edgelist=route_edges,
        edge_color="red",
        width=2.8,
        arrows=True,
        arrowsize=25,
        connectionstyle="arc3,rad=0.1"
    )

    edge_labels = {
        (arc.tail, arc.head): (
            f"A{arc.id}: {arc.cost}"
        )
        for arc in graph.arcs
    }

    nx.draw_networkx_edge_labels(
        visual_graph,
        positions,
        edge_labels=edge_labels,
        font_size=8
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
