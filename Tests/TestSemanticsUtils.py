import unittest
from PythonSemantics import SemanticsUtils as Utils, Semantics

list_a = ['a', 'b']
list_b = ['c', 'd']
list_c = ['e', 'f']
list_d = ['g', 'h']

a = Semantics.Sentence('a')
b = Semantics.Sentence('b')
c = Semantics.Sentence('c')
d = Semantics.Sentence('d')
e = Semantics.Sentence('e')
f = Semantics.Sentence('f')


class TestSemantics(unittest.TestCase):

    def test_list_combinations_empty(self):
        self.assertEqual([], Utils.list_combinations([], []))

    def test_list_combinations_one_empty(self):
        self.assertEqual(list_a, Utils.list_combinations(list_a, []))

    def test_list_combinations_both_non_empty(self):
        combinations = Utils.list_combinations(list_a, list_b)
        self.assertIn(['a', 'c'], combinations)
        self.assertIn(['a', 'd'], combinations)
        self.assertIn(['b', 'c'], combinations)
        self.assertIn(['b', 'd'], combinations)
        self.assertEqual(4, len(combinations))

    def test_list_combinations_lists_of_lists(self):
        combinations = Utils.list_combinations([list_a, list_b], [list_c, list_d])
        self.assertIn(['a', 'b', 'e', 'f'], combinations)
        self.assertIn(['a', 'b', 'g', 'h'], combinations)
        self.assertIn(['c', 'd', 'e', 'f'], combinations)
        self.assertIn(['c', 'd', 'g', 'h'], combinations)
        self.assertEqual(4, len(combinations))

    def test_list_combinations(self):
        product = Utils.list_combinations([[a]], [[b]])
        self.assertIn(a, product[0])
        self.assertIn(b, product[0])
        self.assertEqual(len(product[0]), 2)

        product = Utils.list_combinations([[a], [b]], [[c]])
        self.assertIn(a, product[0])
        self.assertIn(c, product[0])

        self.assertIn(b, product[1])
        self.assertIn(c, product[1])

        self.assertEqual(len(product[0]), 2)
        self.assertEqual(len(product[0]), 2)

        product = Utils.list_combinations([[a]], [[]])
        self.assertIn(a, product[0])
        self.assertEqual(len(product[0]), 1)

    def test_base_elements_trivial_case(self):
        base_elements = Utils.base_elements(list_a)
        self.assertIn('a', base_elements)
        self.assertIn('b', base_elements)
        self.assertEqual(2, len(base_elements))

    def test_base_elements_multi_level_list(self):
        base_elements = Utils.base_elements([list_a, list_b])
        all(self.assertIn(element, base_elements) for element in ['a', 'b', 'c', 'd'])
        self.assertEqual(4, len(base_elements))

    def test_powerset(self):
        test_set = [1,2,3]
        power_sets = Utils.powerset(test_set)
        self.assertIn([], power_sets)
        self.assertIn([1], power_sets)
        self.assertIn([2], power_sets)
        self.assertIn([3], power_sets)
        self.assertIn([1, 2], power_sets)
        self.assertIn([1, 3], power_sets)
        self.assertIn([2, 3], power_sets)
        self.assertIn([1, 2, 3], power_sets)
        self.assertEqual(8, len(power_sets))

    def test_group_intersection(self):
        set_a = Semantics.SemanticSet([a, b, c])
        set_b = Semantics.SemanticSet([a, b])
        set_c = Semantics.SemanticSet([c])

        intersection_a_b = Utils.group_intersection([set_a, set_b])
        self.assertIn(a, intersection_a_b.elements)
        self.assertIn(b, intersection_a_b.elements)
        self.assertEqual(2, len(intersection_a_b.elements))

        intersection_a_c = Utils.group_intersection([set_a, set_c])
        self.assertIn(c, intersection_a_c.elements)
        self.assertEqual(1, len(intersection_a_c.elements))

        intersection_b_c = Utils.group_intersection([set_b, set_c])
        self.assertEqual(0, len(intersection_b_c.elements))

    def test_minimal_set(self):
        set_a = Semantics.SemanticSet([a, b])
        set_b = Semantics.SemanticSet([c, d])
        set_c = Semantics.SemanticSet([b, d])
        set_d = Semantics.SemanticSet([a, b, d])
        set_e = Semantics.SemanticSet([a, c, d])
        set_f = Semantics.SemanticSet([a, b, c, d])

        minimal_sets = Utils.minimal_set(set([set_a, set_b, set_c, set_d, set_e, set_f]))

        self.assertIn(set_a, minimal_sets)
        self.assertIn(set_b, minimal_sets)
        self.assertIn(set_c, minimal_sets)
        self.assertNotIn(set_d, minimal_sets)
        self.assertNotIn(set_e, minimal_sets)
        self.assertNotIn(set_f, minimal_sets)

    def test_generate_worlds(self):
        a = Semantics.Sentence('a', random_variable=True)
        a_neg = Semantics.Sentence('a', random_variable=True, negation=True)
        b = Semantics.Sentence('b', random_variable=True)
        b_neg = Semantics.Sentence('b', random_variable=True, negation=True)
        c = Semantics.Sentence('c', random_variable=True)

        four_worlds = Utils.generate_worlds([a, b])
        self.assertEqual(4, len(four_worlds))
        for world in four_worlds:
            self.assertEqual(2, len(world))
            self.assertFalse(a in world and a_neg in world)
            self.assertFalse(b in world and b_neg in world)

        eight_worlds = Utils.generate_worlds([a, b, c])
        self.assertEqual(8, len(eight_worlds))

    def test_extensions_and_derivations_to_str_list(self):
        ext_deriv = [(Semantics.SemanticSet([a, b, c]), [d, e, f]),
                     (Semantics.SemanticSet([d, e, f]), [a, b, c])]
        string_representation = Utils.extensions_and_derivations_to_str_list(ext_deriv)
        # self.assertEqual(['{a, b, c} |- {d, e, f}', '{d, e, f} |- {a, b, c}'], string_representation)