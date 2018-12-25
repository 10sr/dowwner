import unittest

from django.test import TestCase


class TestFailure(TestCase):
    @unittest.skip("demonstrating failing and skipping")
    def test_failure(self):
        self.assertEqual(True, False)
        return
