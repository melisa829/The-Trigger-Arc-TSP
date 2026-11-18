
import random
import unittest

from src.graph import Graph, Arc, TriggerRelation
from src.genetic_algorithm import (
    is_valid_route,
    generate_random_route,
    generate_initial_population,
    calculate_fitness,
    select_parent,
    crossover,
    mutate,
    genetic_algorithm,
)
from src.cost_evaluator import evaluate_route_cost


class TestGeneticAlgorithm(unittest.TestCase):

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

    def test_valid_route(self):
        self.assertTrue(
            is_valid_route(self.graph, self.route1)
        )

    def test_invalid_route(self):
        invalid_route = [0, 4, 5]

        self.assertFalse(
            is_valid_route(self.graph, invalid_route)
        )

    def test_route_with_missing_arc(self):
        invalid_route = [0, 1, 99]

        self.assertFalse(
            is_valid_route(self.graph, invalid_route)
        )

    def test_generate_random_route(self):
        route = generate_random_route(self.graph)

        self.assertIsNotNone(route)
        self.assertTrue(
            is_valid_route(self.graph, route)
        )

    def test_generate_initial_population(self):
        population = generate_initial_population(
            self.graph,
            population_size=10
        )

        self.assertEqual(len(population), 10)

        for route in population:
            self.assertTrue(
                is_valid_route(self.graph, route)
            )

    def test_invalid_population_size(self):
        with self.assertRaises(ValueError):
            generate_initial_population(
                self.graph,
                population_size=0
            )

    def test_calculate_fitness(self):
        fitness = calculate_fitness(
            self.graph,
            self.route1
        )

        expected_cost = evaluate_route_cost(
            self.graph,
            self.route1
        )

        expected_fitness = 1 / (1 + expected_cost)

        self.assertAlmostEqual(
            fitness,
            expected_fitness
        )

    def test_select_parent(self):
        population = [
            self.route1,
            self.route2
        ]

        fitness_scores = [
            calculate_fitness(self.graph, route)
            for route in population
        ]

        parent = select_parent(
            population,
            fitness_scores,
            tournament_size=2
        )

        self.assertIn(parent, population)

        # The selected parent must be an independent copy.
        parent.append(99)

        self.assertNotIn(99, self.route1)
        self.assertNotIn(99, self.route2)

    def test_select_parent_with_empty_population(self):
        with self.assertRaises(ValueError):
            select_parent([], [])

    def test_select_parent_with_invalid_tournament_size(self):
        with self.assertRaises(ValueError):
            select_parent(
                [self.route1],
                [1.0],
                tournament_size=0
            )

    def test_crossover(self):
        child = crossover(
            self.graph,
            self.route1,
            self.route2
        )

        self.assertTrue(
            is_valid_route(self.graph, child)
        )

    def test_crossover_with_invalid_parent(self):
        with self.assertRaises(ValueError):
            crossover(
                self.graph,
                [0, 4, 5],
                self.route2
            )

    def test_mutation_without_mutation(self):
        result = mutate(
            self.graph,
            self.route1,
            mutation_rate=0
        )

        self.assertEqual(result, self.route1)
        self.assertIsNot(result, self.route1)

    def test_mutation_with_probability_one(self):
        result = mutate(
            self.graph,
            self.route1,
            mutation_rate=1
        )

        self.assertTrue(
            is_valid_route(self.graph, result)
        )

    def test_mutation_with_invalid_probability(self):
        with self.assertRaises(ValueError):
            mutate(
                self.graph,
                self.route1,
                mutation_rate=1.5
            )

    def test_mutation_with_invalid_route(self):
        with self.assertRaises(ValueError):
            mutate(
                self.graph,
                [0, 4, 5]
            )

    def test_genetic_algorithm(self):
        best_route, best_cost = genetic_algorithm(
            self.graph,
            population_size=10,
            generations=10,
            crossover_rate=0.8,
            mutation_rate=0.2,
            tournament_size=3,
            elitism_count=1
        )

        self.assertTrue(
            is_valid_route(self.graph, best_route)
        )

        self.assertAlmostEqual(
            best_cost,
            evaluate_route_cost(self.graph, best_route)
        )

        self.assertLessEqual(best_cost, 15)

    def test_genetic_algorithm_with_zero_generations(self):
        best_route, best_cost = genetic_algorithm(
            self.graph,
            population_size=10,
            generations=0
        )

        self.assertTrue(
            is_valid_route(self.graph, best_route)
        )

        self.assertAlmostEqual(
            best_cost,
            evaluate_route_cost(self.graph, best_route)
        )

    def test_genetic_algorithm_invalid_population_size(self):
        with self.assertRaises(ValueError):
            genetic_algorithm(
                self.graph,
                population_size=1
            )

    def test_genetic_algorithm_invalid_generations(self):
        with self.assertRaises(ValueError):
            genetic_algorithm(
                self.graph,
                generations=-1
            )

    def test_genetic_algorithm_invalid_crossover_rate(self):
        with self.assertRaises(ValueError):
            genetic_algorithm(
                self.graph,
                crossover_rate=1.5
            )

    def test_genetic_algorithm_invalid_elitism(self):
        with self.assertRaises(ValueError):
            genetic_algorithm(
                self.graph,
                population_size=10,
                elitism_count=10
            )


if __name__ == "__main__":
    unittest.main()
