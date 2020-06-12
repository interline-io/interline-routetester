import os
import unittest

from routetester.checker import *

class TestMedian(unittest.TestCase):
    def test_median(self):
        a = [0, 1, 2, 3]
        self.assertEquals(median(a), 1.5)    
        b = [0, 1, 2, 3, 4]
        self.assertEquals(median(b), 2)

class TestChecker(unittest.TestCase):
    def test_checker(self):
        pass
