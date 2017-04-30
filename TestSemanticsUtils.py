import unittest
import SemanticsUtils as Utils
import Semantics

list_a = ['a', 'b']
list_b = ['c', 'd']
list_c = ['e', 'f']
list_d = ['g', 'h']

a = Semantics.Sentence('a')
b = Semantics.Sentence('b')
c = Semantics.Sentence('c')
d = Semantics.Sentence('d')


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

        minimal_sets = Semantics.Utils.minimal_set(set([set_a, set_b, set_c, set_d, set_e, set_f]))

        self.assertIn(set_a, minimal_sets)
        self.assertIn(set_b, minimal_sets)
        self.assertIn(set_c, minimal_sets)
        self.assertNotIn(set_d, minimal_sets)
        self.assertNotIn(set_e, minimal_sets)
        self.assertNotIn(set_f, minimal_sets)
