
import unittest

from src.graph import Arc, TriggerRelation, Graph
from src.greedy import greedy_algorithm


class TestGreedyAlgorithm(unittest.TestCase):

    def setUp(self):
        self.arcs = [
            Arc(id=0, tail=0, head=1, cost=10),
            Arc(id=1, tail=0, head=2, cost=20),
            Arc(id=2, tail=1, head=2, cost=5),
            Arc(id=3, tail=1, head=0, cost=15),
            Arc(id=4, tail=2, head=0, cost=10),
            Arc(id=5, tail=2, head=1, cost=8)
        ]

        self.graph = Graph(
            num_nodes=3,
            arcs=self.arcs,
            relations=[]
        )

    def test_route_starts_and_ends_at_depot(self):
        route, cost = greedy_algorithm(self.graph)

        first_arc = next(
            arc for arc in self.arcs
            if arc.id == route[0]
        )

        last_arc = next(
            arc for arc in self.arcs
            if arc.id == route[-1]
        )

        self.assertEqual(first_arc.tail, 0)
        self.assertEqual(last_arc.head, 0)

    def test_all_nodes_are_visited(self):
        route, cost = greedy_algorithm(self.graph)

        visited_nodes = {0}

        for arc_id in route:
            arc = next(
                arc for arc in self.arcs
                if arc.id == arc_id
            )

            visited_nodes.add(arc.head)

        self.assertEqual(
            visited_nodes,
            {0, 1, 2}
        )

    def test_route_cost(self):
        route, cost = greedy_algorithm(self.graph)

        self.assertEqual(cost, 25)

    def test_route_contains_valid_arcs(self):
        route, cost = greedy_algorithm(self.graph)

        valid_arc_ids = {
            arc.id for arc in self.arcs
        }

        for arc_id in route:
            self.assertIn(arc_id, valid_arc_ids)

    def test_no_valid_return_arc(self):
        arcs = [
            Arc(id=0, tail=0, head=1, cost=10),
            Arc(id=1, tail=1, head=2, cost=5)
        ]

        graph = Graph(
            num_nodes=3,
            arcs=arcs,
            relations=[]
        )

        with self.assertRaises(ValueError):
            greedy_algorithm(graph)

    def test_greedy_avoids_dead_end(self):
        arcs = [
            Arc(id=0, tail=0, head=1, cost=1),
            Arc(id=1, tail=0, head=2, cost=5),
            Arc(id=2, tail=1, head=3, cost=1),
            Arc(id=3, tail=2, head=1, cost=1),
            Arc(id=4, tail=3, head=0, cost=1)
        ]

        graph = Graph(
            num_nodes=4,
            arcs=arcs,
            relations=[]
        )

        route, cost = greedy_algorithm(graph)

        self.assertEqual(route, [1, 3, 2, 4])
        self.assertEqual(cost, 8)

    def test_greedy_with_trigger_relation(self):
        arcs = [
            Arc(id=0, tail=0, head=1, cost=2),
            Arc(id=1, tail=1, head=2, cost=10),
            Arc(id=2, tail=2, head=0, cost=3)
        ]

        relations = [
            TriggerRelation(
                id=0,
                trigger_arc_id=0,
                target_arc_id=1,
                new_cost=4
            )
        ]

        graph = Graph(
            num_nodes=3,
            arcs=arcs,
            relations=relations
        )

        route, cost = greedy_algorithm(graph)

        self.assertEqual(route, [0, 1, 2])
        self.assertEqual(cost, 9)


if __name__ == "__main__":
    unittest.main()
