# import unittest

from django.test import TestCase

from django.urls import reverse


class ViewTests(TestCase):
    def test_index(self):
        response = self.client.get(reverse("dowwner:index"))
        self.assertEqual(response.status_code, 200)
        return
