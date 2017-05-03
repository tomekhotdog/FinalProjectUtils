import unittest
import Bayesian


class TestBayesianNetwork(unittest.TestCase):

    def test_validates_valid_network(self):
        Bayesian.BayesianNetwork({'a': 0.5, 'b': 0.8, 'c': 0.3})

    def test_validates_invalid_network(self):
        def invalid_network_instantiation():
            Bayesian.BayesianNetwork({'a': 0.4, 'b': 1.0001, 'c': -0.4})

        self.assertRaises(Bayesian.InvalidRandomVariableException, invalid_network_instantiation)