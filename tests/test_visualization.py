
import os
import unittest

from src.graph import Graph, Arc, TriggerRelation
from src.visualization import (
    create_graph_visualization,
    draw_graph,
    draw_route,
)


class TestVisualization(unittest.TestCase):

    def setUp(self):
        self.graph = Graph(
            num_nodes=3,
            arcs=[
                Arc(0, 0, 1, 2),
                Arc(1, 1, 2, 10),
                Arc(2, 2, 0, 3),
                Arc(3, 0, 2, 5),
                Arc(4, 2, 1, 4),
                Arc(5, 1, 0, 6),
            ],
            relations=[
                TriggerRelation(
                    id=0,
                    trigger_arc_id=0,
                    target_arc_id=1,
                    new_cost=4
                )
            ]
        )

        self.valid_route = [0, 1, 2]

    def test_create_graph_visualization(self):
        visual_graph, positions = create_graph_visualization(
            self.graph
        )

        self.assertEqual(
            visual_graph.number_of_nodes(),
            3
        )

        self.assertEqual(
            visual_graph.number_of_edges(),
            6
        )

        self.assertEqual(
            set(visual_graph.nodes()),
            {0, 1, 2}
        )

        self.assertEqual(
            set(positions.keys()),
            {0, 1, 2}
        )

    def test_graph_contains_arc_attributes(self):
        visual_graph, _ = create_graph_visualization(
            self.graph
        )

        self.assertEqual(
            visual_graph[0][1]["arc_id"],
            0
        )

        self.assertEqual(
            visual_graph[0][1]["cost"],
            2
        )

    def test_draw_graph_without_display(self):
        draw_graph(
            self.graph,
            show=False
        )

    def test_draw_graph_and_save_image(self):
        save_path = "test_graph_visualization.png"

        try:
            draw_graph(
                self.graph,
                show=False,
                save_path=save_path
            )

            self.assertTrue(
                os.path.exists(save_path)
            )

        finally:
            if os.path.exists(save_path):
                os.remove(save_path)

    def test_draw_route_without_display(self):
        draw_route(
            self.graph,
            self.valid_route,
            show=False
        )

    def test_draw_route_and_save_image(self):
        save_path = "test_route_visualization.png"

        try:
            draw_route(
                self.graph,
                self.valid_route,
                show=False,
                save_path=save_path
            )

            self.assertTrue(
                os.path.exists(save_path)
            )

        finally:
            if os.path.exists(save_path):
                os.remove(save_path)

    def test_draw_route_with_wrong_length(self):
        with self.assertRaises(ValueError):
            draw_route(
                self.graph,
                [0, 1],
                show=False
            )

    def test_draw_route_with_unknown_arc(self):
        with self.assertRaises(ValueError):
            draw_route(
                self.graph,
                [0, 1, 99],
                show=False
            )

    def test_draw_route_with_repeated_arc(self):
        with self.assertRaises(ValueError):
            draw_route(
                self.graph,
                [0, 1, 0],
                show=False
            )

    def test_draw_route_with_disconnected_arcs(self):
        with self.assertRaises(ValueError):
            draw_route(
                self.graph,
                [0, 4, 5],
                show=False
            )

    def test_draw_route_that_does_not_return_to_depot(self):
        with self.assertRaises(ValueError):
            draw_route(
                self.graph,
                [0, 1, 4],
                show=False
            )


if __name__ == "__main__":
    unittest.main()
