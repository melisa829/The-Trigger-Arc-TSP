
import random
import unittest

from src.graph import Graph, Arc, TriggerRelation
from src.cost_evaluator import evaluate_route_cost
from src.genetic_algorithm import is_valid_route
from src.simulated_annealing import (
    generate_neighbor,
    acceptance_probability,
    simulated_annealing,
)


class TestSimulatedAnnealing(unittest.TestCase):

    def setUp(self):
        random.seed(42)

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

        self.route1 = [0, 1, 2]
        self.route2 = [3, 4, 5]

    # Tests for generate_neighbor()

    def test_generate_neighbor(self):
        neighbor = generate_neighbor(
            self.graph,
            self.route1
        )

        self.assertTrue(
            is_valid_route(self.graph, neighbor)
        )

    def test_generate_neighbor_preserves_original_route(self):
        original_route = self.route1.copy()

        generate_neighbor(
            self.graph,
            self.route1
        )

        self.assertEqual(
            self.route1,
            original_route
        )

    def test_generate_neighbor_with_invalid_route(self):
        with self.assertRaises(ValueError):
            generate_neighbor(
                self.graph,
                [0, 4, 5]
            )

    # Tests for acceptance_probability()

    def test_acceptance_probability_better_solution(self):
        probability = acceptance_probability(
            current_cost=20,
            neighbor_cost=10,
            temperature=100
        )

        self.assertEqual(probability, 1.0)

    def test_acceptance_probability_equal_solution(self):
        probability = acceptance_probability(
            current_cost=10,
            neighbor_cost=10,
            temperature=100
        )

        self.assertEqual(probability, 1.0)

    def test_acceptance_probability_worse_solution(self):
        probability = acceptance_probability(
            current_cost=10,
            neighbor_cost=20,
            temperature=100
        )

        self.assertGreater(probability, 0)
        self.assertLess(probability, 1)

    def test_acceptance_probability_lower_temperature(self):
        high_temperature_probability = acceptance_probability(
            current_cost=10,
            neighbor_cost=20,
            temperature=100
        )

        low_temperature_probability = acceptance_probability(
            current_cost=10,
            neighbor_cost=20,
            temperature=1
        )

        self.assertGreater(
            high_temperature_probability,
            low_temperature_probability
        )

    def test_acceptance_probability_invalid_temperature(self):
        with self.assertRaises(ValueError):
            acceptance_probability(
                current_cost=10,
                neighbor_cost=20,
                temperature=0
            )

    # Tests for simulated_annealing()

    def test_simulated_annealing(self):
        best_route, best_cost = simulated_annealing(
            self.graph,
            initial_temperature=100,
            cooling_rate=0.95,
            minimum_temperature=0.01,
            max_iterations=100
        )

        self.assertTrue(
            is_valid_route(self.graph, best_route)
        )

        self.assertAlmostEqual(
            best_cost,
            evaluate_route_cost(self.graph, best_route)
        )

        self.assertLessEqual(best_cost, 15)

    def test_simulated_annealing_zero_iterations(self):
        best_route, best_cost = simulated_annealing(
            self.graph,
            max_iterations=0
        )

        self.assertTrue(
            is_valid_route(self.graph, best_route)
        )

        self.assertAlmostEqual(
            best_cost,
            evaluate_route_cost(self.graph, best_route)
        )

    def test_simulated_annealing_with_invalid_initial_temperature(self):
        with self.assertRaises(ValueError):
            simulated_annealing(
                self.graph,
                initial_temperature=0
            )

    def test_simulated_annealing_with_invalid_cooling_rate(self):
        with self.assertRaises(ValueError):
            simulated_annealing(
                self.graph,
                cooling_rate=1
            )

    def test_simulated_annealing_with_invalid_minimum_temperature(self):
        with self.assertRaises(ValueError):
            simulated_annealing(
                self.graph,
                initial_temperature=100,
                minimum_temperature=100
            )

    def test_simulated_annealing_with_negative_iterations(self):
        with self.assertRaises(ValueError):
            simulated_annealing(
                self.graph,
                max_iterations=-1
            )


if __name__ == "__main__":
    unittest.main()
