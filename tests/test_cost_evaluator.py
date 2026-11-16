
import unittest

from src.graph import Arc, TriggerRelation, Graph
from src.cost_evaluator import evaluate_route_cost


class TestCostEvaluator(unittest.TestCase):

    def setUp(self):
        self.arcs = [
            Arc(id=0, tail=0, head=1, cost=10),
            Arc(id=1, tail=1, head=2, cost=15),
            Arc(id=2, tail=2, head=0, cost=20)
        ]

        self.relations = [
            TriggerRelation(
                id=0,
                trigger_arc_id=0,
                target_arc_id=1,
                new_cost=5
            )
        ]

        self.graph = Graph(
            num_nodes=3,
            arcs=self.arcs,
            relations=self.relations
        )

    def test_normal_route_cost(self):
        graph = Graph(
            num_nodes=3,
            arcs=self.arcs,
            relations=[]
        )

        self.assertEqual(
            evaluate_route_cost(graph, [0, 1, 2]),
            45
        )

    def test_trigger_changes_target_cost(self):
        self.assertEqual(
            evaluate_route_cost(self.graph, [0, 1, 2]),
            35
        )

    def test_target_before_trigger(self):
        self.assertEqual(
            evaluate_route_cost(self.graph, [1, 0, 2]),
            45
        )

    def test_multiple_triggers_same_target(self):
        relations = [
            TriggerRelation(0, 0, 2, 12),
            TriggerRelation(1, 1, 2, 7)
        ]

        graph = Graph(
            num_nodes=3,
            arcs=self.arcs,
            relations=relations
        )

        self.assertEqual(
            evaluate_route_cost(graph, [0, 1, 2]),
            32
        )

    def test_nonexistent_arc(self):
        with self.assertRaises(ValueError):
            evaluate_route_cost(self.graph, [0, 5, 2])


if __name__ == "__main__":
    unittest.main()
