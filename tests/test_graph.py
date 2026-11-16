
import unittest

from src.graph import Arc, TriggerRelation, Graph


class TestGraph(unittest.TestCase):

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

    def test_create_arc(self):
        arc = Arc(id=0, tail=0, head=1, cost=10)

        self.assertEqual(arc.id, 0)
        self.assertEqual(arc.tail, 0)
        self.assertEqual(arc.head, 1)
        self.assertEqual(arc.cost, 10)

    def test_create_trigger_relation(self):
        relation = self.relations[0]

        self.assertEqual(relation.trigger_arc_id, 0)
        self.assertEqual(relation.target_arc_id, 1)
        self.assertEqual(relation.new_cost, 5)

    def test_create_valid_graph(self):
        graph = Graph(
            num_nodes=3,
            arcs=self.arcs,
            relations=self.relations
        )

        self.assertEqual(graph.num_nodes, 3)
        self.assertEqual(graph.depot, 0)
        self.assertEqual(len(graph.arcs), 3)
        self.assertEqual(len(graph.relations), 1)

    def test_invalid_depot(self):
        with self.assertRaises(ValueError):
            Graph(
                num_nodes=3,
                arcs=self.arcs,
                relations=self.relations,
                depot=5
            )

    def test_invalid_arc_endpoint(self):
        invalid_arcs = [
            Arc(id=0, tail=0, head=5, cost=10)
        ]

        with self.assertRaises(ValueError):
            Graph(
                num_nodes=3,
                arcs=invalid_arcs,
                relations=[]
            )

    def test_negative_arc_cost(self):
        invalid_arcs = [
            Arc(id=0, tail=0, head=1, cost=-10)
        ]

        with self.assertRaises(ValueError):
            Graph(
                num_nodes=3,
                arcs=invalid_arcs,
                relations=[]
            )

    def test_missing_trigger_arc(self):
        invalid_relations = [
            TriggerRelation(
                id=0,
                trigger_arc_id=10,
                target_arc_id=1,
                new_cost=5
            )
        ]

        with self.assertRaises(ValueError):
            Graph(
                num_nodes=3,
                arcs=self.arcs,
                relations=invalid_relations
            )


if __name__ == "__main__":
    unittest.main()
