import unittest

from juggling.notation import siteswap


class SiteswapUtilsTests(unittest.TestCase):
    def test_siteswap_char_to_int(self):
        self.assertEqual(siteswap.siteswap_char_to_int('0'), 0)
        self.assertEqual(siteswap.siteswap_char_to_int('1'), 1)
        self.assertEqual(siteswap.siteswap_char_to_int('a'), 10)
        self.assertEqual(siteswap.siteswap_char_to_int('f'), 15)
        self.assertEqual(siteswap.siteswap_char_to_int('z'), 35)

    def test_invalid_char(self):
        self.assertRaises(ValueError, siteswap.siteswap_char_to_int, [3])
        self.assertRaises(ValueError, siteswap.siteswap_char_to_int, 10)
        self.assertRaises(ValueError, siteswap.siteswap_char_to_int, '#')
        self.assertRaises(ValueError, siteswap.siteswap_char_to_int, 'multichar')

    def test_siteswap_int_to_char(self):
        self.assertEqual(siteswap.siteswap_int_to_char(9), '9')
        self.assertEqual(siteswap.siteswap_int_to_char(0), '0')
        self.assertEqual(siteswap.siteswap_int_to_char(10), 'a')
        self.assertEqual(siteswap.siteswap_int_to_char(15), 'f')
        self.assertEqual(siteswap.siteswap_int_to_char(35), 'z')

    def test_invalid_int(self):
        self.assertRaises(ValueError, siteswap.siteswap_int_to_char, ['3'])
        self.assertRaises(ValueError, siteswap.siteswap_int_to_char, 'a')
        self.assertRaises(ValueError, siteswap.siteswap_int_to_char, 36)
        self.assertRaises(ValueError, siteswap.siteswap_int_to_char, -1)


class SiteSwapSyntaxValidationTests(unittest.TestCase):
    def test_valid_syntax(self):
        solo_patterns = [
            '441',
            '(6x,4)(4,6x)',
            '(6x,4)*',
            '[64]020',
            '[33](3,3)123',
            '(4,2)(2x,[44x])',
        ]
        for pattern in solo_patterns:
            self.assertTrue(siteswap.is_valid_siteswap_syntax(pattern))

        passing_patterns = [
            ('<4p|3><2|3p>', 2),
            ('<2|3p><2p|3><[3p22]|3p><3|3>', 2),
            ('<(2p3,4x)|(2xp3,4p1)|(2xp2,4xp2)>', 3)
        ]
        for pattern, num_jugglers in passing_patterns:
            self.assertTrue(siteswap.is_valid_siteswap_syntax(pattern, num_jugglers))

    def test_return_match(self):
        import re
        sre_match_object = type(re.match('', ''))

        self.assertTrue(siteswap.is_valid_siteswap_syntax('441', return_match=False))

        _, match = siteswap.is_valid_siteswap_syntax('441', return_match=True)
        self.assertIsInstance(match, sre_match_object)

        _, match = siteswap.is_valid_siteswap_syntax('###', return_match=True)
        self.assertIsNone(match)

    def test_invalid_syntax(self):
        solo_patterns = [
            '#!j',
            '((3232,3)',
            '(3232,3))',
            '[(3232,3)])',
        ]
        for pattern in solo_patterns:
            self.assertFalse(siteswap.is_valid_siteswap_syntax(pattern))
