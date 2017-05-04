import unittest
import Bayesian
import Semantics

bn = Bayesian.BayesianNetwork({'a': 0.5, 'b': 0.8, 'c': 0.3})
a = Semantics.Sentence('a', random_variable=True)
a_neg = Semantics.Sentence('a', random_variable=True, negation=True)
b = Semantics.Sentence('b', random_variable=True)
b_neg = Semantics.Sentence('b', random_variable=True, negation=True)
c = Semantics.Sentence('c', random_variable=True)
c_neg = Semantics.Sentence('c', random_variable=True, negation=True)
d = Semantics.Sentence('d', random_variable=True)


class TestBayesianNetwork(unittest.TestCase):

    def test_validates_valid_network(self):
        bn.validate()

    def test_validates_invalid_network(self):
        def invalid_network_instantiation():
            Bayesian.BayesianNetwork({'a': 0.4, 'b': 1.0001, 'c': -0.4})

        self.assertRaises(Bayesian.InvalidRandomVariableException, invalid_network_instantiation)

    def test_p(self):
        baba = Bayesian.BayesianNetwork({'a': 0.5, 'b': 0.8, 'c': 0.3})
        self.assertAlmostEqual(0.5, baba.p(a))
        self.assertAlmostEqual(0.5, baba.p(a_neg))
        self.assertAlmostEqual(0.8, baba.p(b))
        self.assertAlmostEqual(0.2, baba.p(b_neg))
        self.assertAlmostEqual(0.3, baba.p(c))
        self.assertAlmostEqual(0.7, baba.p(c_neg))

    def test_p_raises_exception_for_invalid_random_variable(self):
        baba = Bayesian.BayesianNetwork({'a': 0.5})

        def get_b_probability():
            return baba.p(b)

        self.assertRaises(Bayesian.InvalidRandomVariableException, get_b_probability)

    def test_p_world_raises_exception_for_invalid_world(self):
        def invalid_p_world():
            return bn.p_world([a, b, c, d])

        self.assertRaises(Bayesian.InvalidRandomVariableWorldException, invalid_p_world)

    def test_p_world(self):
        self.assertAlmostEqual(0.12, bn.p_world([a, b, c]))
        self.assertAlmostEqual(0.12, bn.p_world([a_neg, b, c]))
        self.assertAlmostEqual(0.03, bn.p_world([a, b_neg, c]))
        self.assertAlmostEqual(0.07, bn.p_world([a, b_neg, c_neg]))
