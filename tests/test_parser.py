
import unittest
import tempfile
from pathlib import Path

from src.parser import parse_instance
from src.graph import Arc, TriggerRelation, Graph


class TestParser(unittest.TestCase):

    def setUp(self):
        self.instance_content = (
            "3 3 1\n"
            "0 0 1 10\n"
            "1 1 2 15\n"
            "2 2 0 20\n"
            "0 1 5\n"
        )

    def create_temp_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".txt",
            delete=False
        )

        temp_file.write(content)
        temp_file.close()

        self.addCleanup(Path(temp_file.name).unlink, missing_ok=True)

        return temp_file.name

    def test_parse_valid_instance(self):
        file_path = self.create_temp_file(self.instance_content)

        graph = parse_instance(file_path)

        self.assertIsInstance(graph, Graph)
        self.assertEqual(graph.num_nodes, 3)
        self.assertEqual(len(graph.arcs), 3)
        self.assertEqual(len(graph.relations), 1)

    def test_parse_arc_data(self):
        file_path = self.create_temp_file(self.instance_content)

        graph = parse_instance(file_path)

        self.assertEqual(
            graph.arcs[0],
            Arc(id=0, tail=0, head=1, cost=10.0)
        )

    def test_parse_trigger_relation(self):
        file_path = self.create_temp_file(self.instance_content)

        graph = parse_instance(file_path)

        self.assertEqual(
            graph.relations[0],
            TriggerRelation(
                id=0,
                trigger_arc_id=0,
                target_arc_id=1,
                new_cost=5.0
            )
        )

    def test_empty_file(self):
        file_path = self.create_temp_file("")

        with self.assertRaises(ValueError):
            parse_instance(file_path)

    def test_invalid_header(self):
        file_path = self.create_temp_file("invalid header\n")

        with self.assertRaises(ValueError):
            parse_instance(file_path)

    def test_missing_lines(self):
        file_path = self.create_temp_file(
            "3 3 1\n"
            "0 0 1 10\n"
        )

        with self.assertRaises(ValueError):
            parse_instance(file_path)

    def test_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            parse_instance("nonexistent_instance.txt")


if __name__ == "__main__":
    unittest.main()
