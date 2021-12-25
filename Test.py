import unittest
from Early import *


class TestTheTask(unittest.TestCase):
    def test_one_symbol(self):
        n = 1
        rules = {Rule("S", "a")}
        word = "a"
        algo = EarlyParser(rules)
        self.assertEqual(True, algo.predict(word))

    def test_simple_recursion(self):
        n = 2
        rules = {Rule("S", "aB"), Rule("B", "c")}
        word = "ac"
        algo = EarlyParser(rules)
        self.assertEqual(True, algo.predict(word))

    def test_complex_recursion(self):
        n = 5
        rules = {
            Rule("S", "AbCd"),
            Rule("A", "k"),
            Rule("A", "l"),
            Rule("C", "dE"),
            Rule("E", "d"),
        }
        word = "lbddd"
        algo = EarlyParser(rules)
        self.assertEqual(True, algo.predict(word))

    def test_complex_example2(self):
        n = 8
        word1 = "aaacbbbbbbbbcccba"
        word2 = "aaacbbbbbbbbcccbac"
        rules = {
            Rule("S", "aTb"),
            Rule("S", "aSa"),
            Rule("T", "U"),
            Rule("T", "aTc"),
            Rule("U", "bVc"),
            Rule("U", "cUc"),
            Rule("V", "bV"),
            Rule("V", "b"),
        }
        algo = EarlyParser(rules)
        self.assertEqual(True, algo.predict(word1))
        self.assertEqual(False, algo.predict(word2))

    def test_complex_example_with_epsilon(self):
        n = 8
        word1 = "a"
        word2 = "1"
        word3 = "cc"
        rules = {
            Rule("S", "cTc"),
            Rule("S", "a"),
            Rule("T", "Uc"),
            Rule("T", "1"),
            Rule("U", "bSa"),
            Rule("U", "b"),
        }
        algo = EarlyParser(rules)
        self.assertEqual(True, algo.predict(word1))
        self.assertEqual(False, algo.predict(word2))
        self.assertEqual(True, algo.predict(word3))


if __name__ == "__main__":
    unittest.main()
