from flake8_class import ClassChecker
import os
from unittest import TestCase


class TestChecks(
    TestCase
):
    def test_get_noqa_lines(self):
        checker = ClassChecker(None, filename=get_absolute_path('data/no_qa.py'))
        self.assertEqual(checker.get_noqa_lines(checker.get_file_contents()), [2])


class DoublesTestChecks(
    TestCase
):
    def test_single_inheritance(self):
        checker = ClassChecker(None, filename=get_absolute_path('data/single.py'))

        self.assertEqual(list(checker.get_class_errors(checker.get_file_contents())), [
            {'message': 'C000 Fix class declaration.', 'line': 61, 'col': 0},
        ])

    def test_multi_inheritance(self):
        checker = ClassChecker(None, filename=get_absolute_path('data/multi.py'))

        self.assertEqual(list(checker.get_class_errors(checker.get_file_contents())), [
            {'message': 'C000 Fix class declaration.', 'line': 69, 'col': 0},
        ])


def get_absolute_path(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)
