import unittest
import Semantics
import ExampleFrameworks

a = Semantics.Sentence('a')
b = Semantics.Sentence('b')
c = Semantics.Sentence('c')
d = Semantics.Sentence('d')
e = Semantics.Sentence('e')
f = Semantics.Sentence('f')
g = Semantics.Sentence('g')
h = Semantics.Sentence('h')
i = Semantics.Sentence('i')
j = Semantics.Sentence('j')

larger_baba = ExampleFrameworks.larger_framework()
venice_baba = ExampleFrameworks.venice_framework()
s_baba = ExampleFrameworks.s_framework()


class TestSemantics(unittest.TestCase):

    def test_rule_initialises_with_no_body(self):
        head = 0
        rule = Semantics.Rule(head)

        self.assertEqual(head, rule.head)
        self.assertEqual([], rule.body, [])

    def test_rule_initialises_with_body(self):
        head = 0
        body = [1, 2, 3]
        rule = Semantics.Rule(head, body)

        self.assertEqual(head, rule.head)
        self.assertEqual(body, rule.body)

    def test_contrary_initialisation(self):
        assumption = 1
        contrary_value = 2
        contrary = Semantics.Contrary(assumption, contrary_value)

        self.assertEqual(assumption, contrary.assumption)
        self.assertEqual(contrary_value, contrary.contrary)

    def test_self_contrary_raises_exception(self):
        def invalid_contrary():
            value = 0
            Semantics.Contrary(value, value)

        self.assertRaises(Semantics.InvalidContraryException, invalid_contrary)

    def test_random_variable_initialises_with_probability(self):
        rv = Semantics.Sentence('a', random_variable=True, negation=True)

        self.assertEqual('a', rv.symbol)
        self.assertEqual(True, rv.random_variable)
        self.assertEqual(True, rv.negation)

    def test_BABA_language_covers_all_sentences(self):
        ExampleFrameworks.valid_BABA_framework()
        self.assertRaises(Semantics.InvalidBABAException, ExampleFrameworks.invalid_BABA_framework)

    def test_BABA_framework_is_flat(self):
        ExampleFrameworks.valid_BABA_framework()
        self.assertRaises(Semantics.InvalidBABAException, ExampleFrameworks.invalid_non_flat_framework)

    def test_contraries(self):
        baba = ExampleFrameworks.valid_BABA_framework()
        contraries = Semantics.contraries(baba, [b, c])
        self.assertIn(d, contraries)
        self.assertIn(e, contraries)
        self.assertEqual(2, len(contraries))

    def test_empty_contraries(self):
        baba = ExampleFrameworks.with_no_contraries()
        contraries = Semantics.contraries(baba, [a, b, c, d, e, f])
        self.assertEqual(0, len(contraries))

    def test_derivable_trivially(self):
        baba = ExampleFrameworks.valid_BABA_framework()
        self.assertTrue(Semantics.derivable(baba, b, [b]))
        self.assertTrue(Semantics.derivable(baba, c, [c]))
        self.assertFalse(Semantics.derivable(baba, b, []))
        self.assertFalse(Semantics.derivable(baba, c, []))

    def test_derivable(self):
        baba = ExampleFrameworks.with_chaining()
        self.assertTrue(Semantics.derivable(baba, a, [b, d, f]))
        self.assertTrue(Semantics.derivable(baba, a, [b, d, f, g]))
        self.assertTrue(Semantics.derivable(baba, g, [c]))
        self.assertTrue(Semantics.derivable(baba, g, [d, f]))
        self.assertFalse(Semantics.derivable(baba, g, [d]))
        self.assertFalse(Semantics.derivable(baba, a, [b, d]))
        self.assertFalse(Semantics.derivable(baba, a, [b, f, g]))

    def test_derivable_with_random_variables(self):
        baba = ExampleFrameworks.r_framework()
        self.assertTrue(Semantics.derivable(baba, a, [a, b]))
        self.assertFalse(Semantics.derivable(baba, a, []))
        self.assertFalse(Semantics.derivable(baba, ExampleFrameworks._c, []))

    def test_derivable_with_empty_body_rules(self):
        baba = ExampleFrameworks.cow_framework()
        self.assertTrue(Semantics.derivable(baba, ExampleFrameworks.HOC, []))
        self.assertFalse(Semantics.derivable(baba, ExampleFrameworks.not_HOC, []))
        self.assertTrue(Semantics.derivable(baba, ExampleFrameworks.not_FM, [ExampleFrameworks.not_FM]))
        self.assertFalse(Semantics.derivable(baba, ExampleFrameworks.FM, [ExampleFrameworks.not_FM]))

    def test_derivable_set(self):
        baba = ExampleFrameworks.with_chaining()
        self.assertTrue(all([element in Semantics.derivable_set(baba, [b, c]) for element in [a, b, c, g]]))
        self.assertEqual(4, len(Semantics.derivable_set(baba, [b, c])))

        self.assertTrue(all([element in Semantics.derivable_set(baba, [b, d, f]) for element in [a, b, c, d, e, f, g]]))
        self.assertEqual(7, len(Semantics.derivable_set(baba, [b, d, f])))

        self.assertTrue(all([element in Semantics.derivable_set(baba, [a, d]) for element in [a, d]]))
        self.assertEqual(2, len(Semantics.derivable_set(baba, [a, d])))

    def test_defends(self):
        self.assertTrue(Semantics.defends(venice_baba, [e, c], a))
        self.assertTrue(Semantics.defends(venice_baba, [c], a))
        self.assertTrue(Semantics.defends(venice_baba, [d], b))
        self.assertFalse(Semantics.defends(venice_baba, [a, c], e))
        self.assertFalse(Semantics.defends(venice_baba, [a, b, c], d))
        self.assertFalse(Semantics.defends(venice_baba, [d, e], a))

        self.assertTrue(Semantics.defends(s_baba, [a, c, f], e))
        self.assertTrue(Semantics.defends(s_baba, [c], e))
        self.assertFalse(Semantics.defends(s_baba, [b, f], d))
        self.assertFalse(Semantics.defends(s_baba, [a, b], e))
        self.assertFalse(Semantics.defends(s_baba, [d, e, f], c))
        self.assertFalse(Semantics.defends(s_baba, [c, d, e, f], a))

    def test_defends_with_empty_body_rules(self):
        baba = ExampleFrameworks.cow_framework()
        self.assertFalse(Semantics.defends(baba, [], ExampleFrameworks.not_HOC))
        self.assertTrue(Semantics.defends(baba, [], ExampleFrameworks.not_FM))

    def test_conflict_free_trivially(self):
        baba = ExampleFrameworks.valid_BABA_framework()
        self.assertTrue(Semantics.conflict_free(baba, []))
        self.assertTrue(Semantics.conflict_free(baba, [a]))
        self.assertTrue(Semantics.conflict_free(baba, [a, b, c]))
        self.assertFalse(Semantics.conflict_free(baba, [b, d]))
        self.assertFalse(Semantics.conflict_free(baba, [a, b, c, d, e]))

    def test_conflict_free(self):
        baba = ExampleFrameworks.with_contraries()
        self.assertTrue(Semantics.conflict_free(baba, []), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [d, e]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [d, e, f, h]), "Expected: conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [d, e, f, g]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [d, e, h, i]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [d, e, f, g, h, i]), "Expected: NOT conflict free")

    def test_conflict_free_larger_framework(self):
        baba = ExampleFrameworks.larger_framework()
        self.assertTrue(Semantics.conflict_free(baba, []), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [b, e, f]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [b, b, e, f]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [b, b, i, f, g, h]), "Expected: conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [b, d, e, f]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [b, e, f, g, h]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [b, e, f, i]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [b, d, e, f, g, h, i]), "Expected: NOT conflict free")

    def test_conflict_free_venice_framework(self):
        baba = ExampleFrameworks.venice_framework()
        self.assertTrue(Semantics.conflict_free(baba, [a]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [b]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [c]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [d]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [e]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [a, c]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [a, d]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [a, e]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [b, d]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [b, e]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [c, e]), "Expected: conflict free")
        self.assertTrue(Semantics.conflict_free(baba, [a, c, e]), "Expected: conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [b, c]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [c, d]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [a, b, c]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [a, b, d]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [a, b, e]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [b, c, d]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [b, c, e]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [c, d, e]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [a, b, c, d]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [a, b, c, e]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [a, b, d, e]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [a, c, d, e]), "Expected: NOT conflict free")
        self.assertFalse(Semantics.conflict_free(baba, [a, b, c, d, e]), "Expected: NOT conflict free")

############################################################
# Testing of Semantic class object elements equality #
############################################################

    def test_Attack_equality(self):
        attack1 = Semantics.Attack(a, [b, c])
        attack2 = Semantics.Attack(a, [c, b])
        attack3 = Semantics.Attack(a, [b, d])

        self.assertTrue(attack1 == attack2)
        self.assertFalse(attack1 == attack3)
        self.assertFalse(attack2 == attack3)

    def test_SemanticSet_equality(self):
        s1 = Semantics.SemanticSet([a, b, c])
        s2 = Semantics.SemanticSet([c, a, b])
        s3 = Semantics.SemanticSet([a, b])

        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertNotEqual(s2, s3)

        self.assertTrue(s1 in set([s1]))

    def test_Rule_equality(self):
        rule1 = Semantics.Rule(a, [b, c, d])
        rule2 = Semantics.Rule(a, [d, b, c])
        rule3 = Semantics.Rule(b, [b, c, d])

        self.assertEqual(rule1, rule2)
        self.assertNotEqual(rule1, rule3)
        self.assertNotEqual(rule2, rule3)

    def test_Contrary_equality(self):
        contrary1 = Semantics.Contrary(a, b)
        contrary2 = Semantics.Contrary(a, b)
        contrary3 = Semantics.Contrary(a, c)

        self.assertEqual(contrary1, contrary2)
        self.assertNotEqual(contrary1, contrary3)
        self.assertNotEqual(contrary2, contrary3)

    def test_Random_Variables_equality(self):
        rv1 = Semantics.Sentence('a', random_variable=True)
        rv2 = Semantics.Sentence('a', random_variable=True)
        rv3 = Semantics.Sentence('b', random_variable=True)

        self.assertEqual(rv1, rv2)
        self.assertNotEqual(rv1, rv3)
        self.assertNotEqual(rv2, rv3)

############################################################

############################################################
# Testing of Semantic class object elements str() function #
############################################################

    def test_Sentence_str_function(self):
        self.assertEqual(str(a), "a")
        self.assertEqual(str(b), "b")
        self.assertEqual(str(c), "c")

    def test_Rule_str_function(self):
        rule1 = Semantics.Rule(a, [b, c])
        self.assertEqual(str(rule1), "a :- b, c")
        rule2 = Semantics.Rule(b, [c, d, e])
        self.assertEqual(str(rule2), "b :- c, d, e")
        rule3 = Semantics.Rule(a, [])
        self.assertEqual(str(rule3), "a :- ")

    def test_Contrary_str_function(self):
        self.assertEqual(str(Semantics.Contrary(a, b)), "~a = b")
        self.assertEqual(str(Semantics.Contrary(b, d)), "~b = d")
        self.assertEqual(str(Semantics.Contrary(c, a)), "~c = a")

    def test_RandomVariable_str_function(self):
        self.assertEqual(str(Semantics.Sentence('a', random_variable=True, negation=True)), "~a")
        self.assertEqual(str(Semantics.Sentence('b', random_variable=True, negation=False)), "b")
        self.assertEqual(str(Semantics.Sentence('c', random_variable=True, negation=True)), "~c")

    def test_SemanticSet_str_function(self):
        self.assertEqual(str(Semantics.SemanticSet([a, b, c, d])), "[a, b, c, d]")
        self.assertEqual(str(Semantics.SemanticSet([e])), "[e]")
        self.assertEqual(str(Semantics.SemanticSet([e, d, c, b, a])), "[e, d, c, b, a]")

############################################################

    def test_generate_attacks(self):
        baba = ExampleFrameworks.larger_framework()
        attacks = Semantics.generate_attacks(baba, [b])
        self.assertIn(Semantics.Attack(b, set([e, f, g, h])), attacks)
        self.assertIn(Semantics.Attack(b, set([e, f, i])), attacks)
        self.assertEqual(2, len(attacks))

    def test_required_to_derive(self):
        baba = ExampleFrameworks.larger_framework()
        required_to_derive_a = Semantics.required_to_derive(baba, a)
        self.assertIn([b], required_to_derive_a)
        self.assertIn([e, f], required_to_derive_a)
        self.assertEqual(2, len(required_to_derive_a))

        self.assertEqual(0, len(Semantics.required_to_derive(baba, j)))

        required_to_derive_c = Semantics.required_to_derive(baba, c)
        self.assertEqual(2, len(required_to_derive_c))
        first_derivation = required_to_derive_c[0]
        second_derivation = required_to_derive_c[1]
        all(self.assertIn(element, first_derivation) or self.assertIn(element, second_derivation)
            for element in [e, f, g, h])
        all(self.assertIn(element, first_derivation) or self.assertIn(element, second_derivation)
            for element in [e, f, i])

    def test_admissible_simple_framework(self):
        baba = ExampleFrameworks.valid_BABA_framework()
        self.assertTrue(Semantics.admissible(baba, [b, c]))

    def test_admissible_larger_framework(self):
        baba = ExampleFrameworks.larger_framework()
        self.assertTrue(Semantics.admissible(baba, [b, e, g, h]))
        self.assertTrue(Semantics.admissible(baba, [b, e, i]))
        self.assertTrue(Semantics.admissible(baba, [b, f, h, g, i]))
        self.assertFalse(Semantics.admissible(baba, [b, e, f, g, h]))
        self.assertFalse(Semantics.admissible(baba, [b, e, f, i]))

    def test_admissible_venice_framework(self):
        self.assertTrue(Semantics.admissible(venice_baba, [a, c, e]))
        self.assertTrue(Semantics.admissible(venice_baba, [b, d]))
        self.assertTrue(Semantics.admissible(venice_baba, [c, e]))
        self.assertTrue(Semantics.admissible(venice_baba, [e]))
        self.assertTrue(Semantics.admissible(venice_baba, [d]))
        self.assertFalse(Semantics.admissible(venice_baba, [a]))
        self.assertFalse(Semantics.admissible(venice_baba, [b]))
        self.assertFalse(Semantics.admissible(venice_baba, [c]))
        self.assertFalse(Semantics.admissible(venice_baba, [a, b]))
        self.assertFalse(Semantics.admissible(venice_baba, [a, c]))
        self.assertFalse(Semantics.admissible(venice_baba, [a, d]))
        self.assertFalse(Semantics.admissible(venice_baba, [a, e]))
        self.assertFalse(Semantics.admissible(venice_baba, [b, c]))
        self.assertFalse(Semantics.admissible(venice_baba, [b, e]))
        self.assertFalse(Semantics.admissible(venice_baba, [c, d]))
        self.assertFalse(Semantics.admissible(venice_baba, [d, e]))
        self.assertFalse(Semantics.admissible(venice_baba, [a, b, c]))
        self.assertFalse(Semantics.admissible(venice_baba, [a, b, d]))
        self.assertFalse(Semantics.admissible(venice_baba, [a, b, e]))
        self.assertFalse(Semantics.admissible(venice_baba, [a, c, d]))
        self.assertFalse(Semantics.admissible(venice_baba, [b, c, d]))
        self.assertFalse(Semantics.admissible(venice_baba, [b, c, e]))
        self.assertFalse(Semantics.admissible(venice_baba, [b, d, e]))
        self.assertFalse(Semantics.admissible(venice_baba, [c, d, e]))
        self.assertFalse(Semantics.admissible(venice_baba, [a, b, c, d]))
        self.assertFalse(Semantics.admissible(venice_baba, [a, b, c, e]))
        self.assertFalse(Semantics.admissible(venice_baba, [a, c, d, e]))
        self.assertFalse(Semantics.admissible(venice_baba, [b, c, d, e]))
        self.assertFalse(Semantics.admissible(venice_baba, [a, b, c, d, e]))

    def test_generate_admissible_larger_framework(self):
        baba = ExampleFrameworks.larger_framework()
        admissible_sets = Semantics.generate_admissible(baba)
        self.assertIn(Semantics.SemanticSet([b, e, i]), admissible_sets)
        self.assertIn(Semantics.SemanticSet([b, e, g, h]), admissible_sets)
        self.assertIn(Semantics.SemanticSet([b, f, g, h, i]), admissible_sets)

    def test_generate_admissible_venice_framework(self):
        admissible_sets = Semantics.generate_admissible(venice_baba)
        self.assertIn(Semantics.SemanticSet([]), admissible_sets)
        self.assertIn(Semantics.SemanticSet([a, c, e]), admissible_sets)
        self.assertIn(Semantics.SemanticSet([c, e]), admissible_sets)
        self.assertIn(Semantics.SemanticSet([e]), admissible_sets)
        self.assertIn(Semantics.SemanticSet([b, d]), admissible_sets)
        self.assertIn(Semantics.SemanticSet([d]), admissible_sets)
        self.assertEqual(6, len(admissible_sets))

    # Verified with http://rull.dbai.tuwien.ac.at:8080/ASPARTIX/index.faces
    def test_generate_admissible_s_framework(self):
        admissible_sets = Semantics.generate_admissible(s_baba)
        self.assertEqual(18, len(admissible_sets))

    def test_preferred_larger_framework(self):
        baba = ExampleFrameworks.larger_framework()
        preferred_sets = Semantics.preferred(baba)
        self.assertIn(Semantics.SemanticSet([b, f, g, h, i]), preferred_sets)

    def test_preferred_venice_framework(self):
        preferred_sets = Semantics.preferred(venice_baba)
        self.assertIn(Semantics.SemanticSet([a, c, e]), preferred_sets)
        self.assertIn(Semantics.SemanticSet([b, d]), preferred_sets)
        self.assertEqual(2, len(preferred_sets))

    def test_preferred_s_framework(self):
        preferred_sets = Semantics.preferred(s_baba)
        self.assertIn(Semantics.SemanticSet([b, e, f]), preferred_sets)
        self.assertIn(Semantics.SemanticSet([b, d, f]), preferred_sets)
        self.assertIn(Semantics.SemanticSet([a, c, e, f]), preferred_sets)
        self.assertEqual(3, len(preferred_sets))

    def test_complete_venice_framework(self):
        complete_sets = Semantics.complete(venice_baba)
        self.assertIn(Semantics.SemanticSet([]), complete_sets)
        self.assertIn(Semantics.SemanticSet([a, c, e]), complete_sets)
        self.assertIn(Semantics.SemanticSet([b, d]), complete_sets)
        self.assertEqual(3, len(complete_sets))

    def test_complete_s_framework(self):
        complete_sets = Semantics.complete(s_baba)
        self.assertIn(Semantics.SemanticSet([a, c, e, f]), complete_sets)
        self.assertIn(Semantics.SemanticSet([b, d, f]), complete_sets)
        self.assertIn(Semantics.SemanticSet([e, f]), complete_sets)
        self.assertIn(Semantics.SemanticSet([b, e, f]), complete_sets)
        self.assertIn(Semantics.SemanticSet([f]), complete_sets)
        self.assertIn(Semantics.SemanticSet([b, f]), complete_sets)
        self.assertEqual(6, len(complete_sets))

    def test_grounded_venice_framework(self):
        grounded_sets = Semantics.grounded(venice_baba)
        self.assertIn(Semantics.SemanticSet([]), grounded_sets)
        self.assertEqual(1, len(grounded_sets))

    def test_grounded_s_framework(self):
        grounded_sets = Semantics.grounded(s_baba)
        self.assertIn(Semantics.SemanticSet([f]), grounded_sets)
        self.assertEqual(1, len(grounded_sets))

    def test_ideal_venice_framework(self):
        ideal_sets = Semantics.ideal(venice_baba)
        self.assertIn(Semantics.SemanticSet([]), ideal_sets)
        self.assertEqual(1, len(ideal_sets))

    def test_ideal_s_framework(self):
        ideal_sets = Semantics.ideal(s_baba)
        self.assertIn(Semantics.SemanticSet([f]), ideal_sets)
        self.assertEqual(2, len(ideal_sets))

    def test_stable_venice_framework(self):
        stable_sets = Semantics.stable(venice_baba)
        self.assertIn(Semantics.SemanticSet([a, c, e]), stable_sets)
        self.assertIn(Semantics.SemanticSet([b, d]), stable_sets)
        self.assertEqual(2, len(stable_sets))

    def test_stable_s_framework(self):
        stable_sets = Semantics.stable(s_baba)
        self.assertIn(Semantics.SemanticSet([a, c, e, f]), stable_sets)
        self.assertIn(Semantics.SemanticSet([b, d, f]), stable_sets)
        self.assertIn(Semantics.SemanticSet([b, e, f]), stable_sets)
        self.assertEqual(3, len(stable_sets))

    def test_sceptically_preferred_venice_framework(self): #?
        sceptically_preferred_sets = Semantics.sceptically_preferred(venice_baba)
        self.assertEqual(1, len(sceptically_preferred_sets))

    def test_sceptically_preferred_s_framework(self):
        sceptically_preferred_sets = Semantics.sceptically_preferred(s_baba)
        self.assertIn(Semantics.SemanticSet([f]), sceptically_preferred_sets)
        self.assertEqual(1, len(sceptically_preferred_sets))

#############################################################
# BABA semantics testing (with random variables)

    def test_r_grounded_semantics(self):
        baba = ExampleFrameworks.r_framework()
        grounded = Semantics.grounded(baba)
        self.assertEqual(1, len(grounded))

        grounded_set = grounded.pop()
        self.assertEqual(3, len(grounded_set.elements))
        self.assertTrue(all([elem in grounded_set.elements for elem in [a, b, c]]))

    def test_r_grounded_semantics_with_random_variable_world(self):
        baba = ExampleFrameworks.r_framework()
        baba.rv_world = [Semantics.Sentence('s', random_variable=True)]
        grounded = Semantics.grounded(baba)
        self.assertEqual(1, len(grounded))

        grounded_set = grounded.pop()
        self.assertEqual(2, len(grounded_set.elements))
        self.assertTrue(all([elem in grounded_set.elements for elem in [b, c]]))

    def test_r_grounded_semantics_with_multiple_random_variables(self):
        baba = ExampleFrameworks.r_framework()
        baba.rv_world = [Semantics.Sentence('s', random_variable=True),
                         Semantics.Sentence('t', random_variable=True)]
        grounded = Semantics.grounded(baba)
        self.assertEqual(1, len(grounded))

        grounded_set = grounded.pop()
        self.assertEqual(2, len(grounded_set.elements))
        self.assertTrue(all([elem in grounded_set.elements for elem in [a, c]]))

    def test_r_grounded_semantics_with_negated_random_variable(self):
        baba = ExampleFrameworks.r_framework()
        baba.rv_world = [Semantics.Sentence('s', random_variable=True, negation=True),
                         Semantics.Sentence('t', random_variable=True, negation=False)]
        grounded = Semantics.grounded(baba)
        self.assertEqual(1, len(grounded))

        grounded_set = grounded.pop()
        self.assertEqual(2, len(grounded_set.elements))
        self.assertTrue(all([elem in grounded_set.elements for elem in [a, c]]))

    def test_grounded_probability(self):
        baba = ExampleFrameworks.r_framework()
        self.assertEqual(0.64, Semantics.semantic_probability(Semantics.GROUNDED, baba, [j]))
        self.assertEqual(0.64, Semantics.semantic_probability(Semantics.GROUNDED, baba, [a]))
        self.assertEqual(0.64, Semantics.semantic_probability(Semantics.GROUNDED, baba, [a, j]))
        self.assertEqual(0.6, Semantics.semantic_probability(Semantics.GROUNDED, baba, [b]))
        self.assertEqual(1.0, Semantics.semantic_probability(Semantics.GROUNDED, baba, [c]))

    def test_invalid_semantic_probability(self):
        baba = ExampleFrameworks.r_framework()

        def invalid_semantics():
            return Semantics.semantic_probability(-1, baba, [a])
        self.assertRaises(Semantics.InvalidSemanticsException, invalid_semantics)

        def invalid_sentences():
            return Semantics.semantic_probability(Semantics.GROUNDED, baba, [f])
        self.assertRaises(Semantics.InvalidBABAException, invalid_sentences)

    def test_valid_cow_framework_probabilities(self):
        baba = ExampleFrameworks.cow_framework()
        self.assertAlmostEqual(0.18, Semantics.semantic_probability(Semantics.GROUNDED, baba, [ExampleFrameworks.HP]))

        baba = ExampleFrameworks.conditional_cow_framework()
        self.assertAlmostEqual(0.02, baba.BN.p_world([ExampleFrameworks.cond_JN, ExampleFrameworks.JF, ExampleFrameworks.CM]))
        self.assertAlmostEqual(0.72, Semantics.semantic_probability(Semantics.GROUNDED, baba, [ExampleFrameworks.HP]))

    def test_compute_grounded_probability(self):
        baba = ExampleFrameworks.r_framework()
        grounded_probabilities = Semantics.compute_semantic_probability(Semantics.GROUNDED, baba)
        self.assertEqual(0.64, grounded_probabilities[ExampleFrameworks.a.symbol])
        self.assertEqual(0.36, grounded_probabilities[ExampleFrameworks._a.symbol])
        self.assertEqual(0.6, grounded_probabilities[ExampleFrameworks.b.symbol])
        self.assertEqual(0.4, grounded_probabilities[ExampleFrameworks._b.symbol])
        self.assertEqual(1.0, grounded_probabilities[ExampleFrameworks.c.symbol])
        self.assertEqual(0.0, grounded_probabilities[ExampleFrameworks._c.symbol])
        self.assertEqual(0.64, grounded_probabilities[ExampleFrameworks.j.symbol])

    def test_compute_ideal_probability(self):
        ideal_probabilities = Semantics.compute_semantic_probability(Semantics.IDEAL, ExampleFrameworks.r_framework())
        self.assertAlmostEqual(0.64, ideal_probabilities[ExampleFrameworks.a.symbol])
        self.assertAlmostEqual(0.36, ideal_probabilities[ExampleFrameworks._a.symbol])
        self.assertAlmostEqual(0.60, ideal_probabilities[ExampleFrameworks.b.symbol])
        self.assertAlmostEqual(0.40, ideal_probabilities[ExampleFrameworks._b.symbol])
        self.assertAlmostEqual(1.0, ideal_probabilities[ExampleFrameworks.c.symbol])
        self.assertAlmostEqual(0.0, ideal_probabilities[ExampleFrameworks._c.symbol])
        self.assertAlmostEqual(0.64, ideal_probabilities[ExampleFrameworks.j.symbol])
        self.assertAlmostEqual(0.6, ideal_probabilities[ExampleFrameworks.s.symbol])
        self.assertAlmostEqual(0.4, ideal_probabilities[ExampleFrameworks.t.symbol])

    def test_compute_semantic_probabilities(self):
        g, s, i = Semantics.compute_semantic_probabilities(ExampleFrameworks.r_framework())
        self.assertEqual(g, [('_a', '0.36'), ('_b', '0.40'), ('_c', '0.00'), ('a', '0.64'),
                             ('b', '0.60'), ('c', '1.00'), ('j', '0.64'), ('s', '0.60'), ('t', '0.40')])
        self.assertEqual(s, [('_a', '0.36'), ('_b', '0.40'), ('_c', '0.00'), ('a', '0.64'),
                             ('b', '0.60'), ('c', '1.00'), ('j', '0.64'), ('s', '0.60'), ('t', '0.40')])
        self.assertEqual(i, [('_a', '0.36'), ('_b', '0.40'), ('_c', '0.00'), ('a', '0.64'),
                             ('b', '0.60'), ('c', '1.00'), ('j', '0.64'), ('s', '0.60'), ('t', '0.40')])

