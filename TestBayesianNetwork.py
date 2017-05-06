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

    def test_conditional_probability_sum(self):
        cp_map = {"bc": 0.4, "b~c": 0.3, "~bc": 0.2, "~b~c": 0.1}
        cp = Bayesian.ConditionalProbability(a, [b, c], cp_map)
        self.assertAlmostEqual(1.0, cp.sum())

    def test_conditional_probability_key_generation(self):
        cp_map = {"bc": 0.4, "b~c": 0.3, "~bc": 0.2, "~b~c": 0.1}
        cp = Bayesian.ConditionalProbability(a, [b, c], cp_map)
        self.assertEqual("bc", cp.conditional_probability_key([c, b]))
        self.assertEqual("b~c", cp.conditional_probability_key([c_neg, b]))
        self.assertEqual("~bc", cp.conditional_probability_key([b_neg, c]))
        self.assertEqual("~b~c", cp.conditional_probability_key([b_neg, c_neg]))

    def test_conditional_probability_request(self):
        cp_map = {"bc": 0.4, "b~c": 0.3, "~bc": 0.2, "~b~c": 0.1}
        cp = Bayesian.ConditionalProbability(a, [b, c], cp_map)
        self.assertEqual(0.4, cp.p([b, c]))
        self.assertEqual(0.3, cp.p([b, c_neg]))
        self.assertEqual(0.2, cp.p([b_neg, c]))
        self.assertEqual(0.1, cp.p([b_neg, c_neg]))

    def test_invalid_conditional_probability_request(self):
        cp_map = {"bc": 0.4, "b~c": 0.3, "~bc": 0.2, "~b~c": 0.1}
        cp = Bayesian.ConditionalProbability(a, [b, c], cp_map)

        def invalid_request():
            return cp.p([b])

        self.assertRaises(Bayesian.InvalidConditionalProbabilityException, invalid_request)

    #  TODO: define validate() tests
    # def test_validate_conditional_probability(self):
    #     cp_map = {"bc": 0.4, "b~c": 0.3, "~bc": 0.2, "~b~c": 0.1}
    #     cp = Bayesian.ConditionalProbability(a, [b, c], cp_map)
    #     cp.validate()

    # def test_validate_invalid_conditional_probability(self):
    #     def invalid_cp():
    #         cp_map = {"bc": 0.5, "b~c": 0.3, "~bc": 0.2, "~b~c": 0.1}
    #         cp = Bayesian.ConditionalProbability(a, [b, c], cp_map)
    #         cp.validate()
    #
    #     self.assertRaises(Bayesian.InvalidConditionalProbabilityException, invalid_cp)

    def test_bayesian_network_with_conditional_probabilities(self):
        cp_map = {"bc": 0.3, "b~c": 0.6, "~bc": 0.5, "~b~c": 0.4}
        cp = Bayesian.ConditionalProbability(a, [b, c], cp_map)
        baysnet = Bayesian.BayesianNetwork({'a': cp, 'b': 0.7, 'c': 0.2})
        self.assertAlmostEqual(0.7, baysnet.p(b))
        self.assertAlmostEqual(0.2, baysnet.p(c))
        self.assertAlmostEqual(0.6, baysnet.p(a, [c_neg, b]))
        self.assertAlmostEqual(0.4, baysnet.p(a, [b_neg, c_neg]))
        self.assertAlmostEqual(0.6, baysnet.p(a_neg, [b_neg, c_neg]))
        self.assertAlmostEqual(0.336, baysnet.p_world([a, b, c_neg]))
        self.assertAlmostEqual(0.096, baysnet.p_world([a, b_neg, c_neg]))
        self.assertAlmostEqual(0.098, baysnet.p_world([a_neg, b, c]))
        self.assertAlmostEqual(0.144, baysnet.p_world([a_neg, b_neg, c_neg]))
