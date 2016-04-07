from unittest import TestCase
from pyexpect import expect

class DbTests(TestCase):
    def test_smoke(self):
        expect(False) == True