import unittest

from juggling.pattern import Pattern


class PatternTests(unittest.TestCase):
    def test_basic_pattern(self):
        pattern = Pattern([4, 4, 1])
        self.assertTrue(pattern.is_symmetric)
        self.assertFalse(pattern.is_asymmetric)
        self.assertFalse(pattern.is_asymmetric)
        self.assertEqual(pattern.period, 3)
        self.assertEqual(pattern.num_objects, 3)
