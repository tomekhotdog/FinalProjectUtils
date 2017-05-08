import unittest
from Parsing import BABAProgramParser as Parser
import Semantics
import ExampleFrameworks
import Bayesian

program_1_string = "myAsm(a).\nmyAsm(b).\nmyAsm(c).\nmyAsm(d).\nmyAsm(e).\n" \
         "contrary(a, _a).\ncontrary(b, _b).\ncontrary(c, _c).\ncontrary(d, _d)." \
         "\ncontrary(e, _e).\nmyRule(_b, [c]).\nmyRule(_a, [b])." \
         "\nmyRule(_c, [d]).\nmyRule(_d, [e]).\nmyRule(_e, [d]).\nmyRV(t, 0.5)."

a = Semantics.Sentence('a')
b = Semantics.Sentence('b')
c = Semantics.Sentence('c')
d = Semantics.Sentence('d')
e = Semantics.Sentence('e')
_a = Semantics.Sentence('_a')
_b = Semantics.Sentence('_b')
_c = Semantics.Sentence('_c')
_d = Semantics.Sentence('_d')
_e = Semantics.Sentence('_e')
t = Semantics.Sentence('t')
_a = Semantics.Sentence('_a')
abc = Semantics.Sentence('abc')
ab = Semantics.Sentence('ab')
bc = Semantics.Sentence('bc')
bd = Semantics.Sentence('bd')
sentence = Semantics.Sentence('sentence')
_sentence = Semantics.Sentence('_sentence')
rv_a = Semantics.Sentence('a', random_variable=True)
rv_b = Semantics.Sentence('b', random_variable=True)
rv_c = Semantics.Sentence('c', random_variable=True)


class TestBABAProgramParser(unittest.TestCase):

    def test_string_constructor(self):
        Parser.BABAProgramParser(string=program_1_string)

    def test_file_constructor(self):
        Parser.BABAProgramParser(filename='BABA_program_1')

    def test_matches_assumption_declaration(self):
        self.assertTrue(Parser.matches_assumption_declaration('myAsm(a). '))
        self.assertTrue(Parser.matches_assumption_declaration('myAsm(myAsm).'))
        self.assertTrue(Parser.matches_assumption_declaration('myAsm(As09).'))
        self.assertTrue(Parser.matches_assumption_declaration(' myAsm(abcde).'))
        self.assertFalse(Parser.matches_assumption_declaration('myAs(a).'))
        self.assertFalse(Parser.matches_assumption_declaration('myAsm().'))
        self.assertFalse(Parser.matches_assumption_declaration('MyAsm(a)'))
        self.assertFalse(Parser.matches_assumption_declaration('myAsm(a).myRule(a, [b,c])'))

    def test_matches_rule_declaration(self):
        self.assertTrue(Parser.matches_rule_declaration('myRule(a, [b,c]).'))
        self.assertTrue(Parser.matches_rule_declaration('myRule(a,[b , c,    d]).'))
        self.assertTrue(Parser.matches_rule_declaration('myRule(abc, [ab, bc, bd]).'))
        self.assertTrue(Parser.matches_rule_declaration('myRule(t, [a1, a2, a3]).'))
        self.assertFalse(Parser.matches_rule_declaration('MyRule(a, [b,c]).'))
        self.assertFalse(Parser.matches_rule_declaration('myRule([a,b], c).'))
        self.assertFalse(Parser.matches_rule_declaration('myRule(a, [b, c]'))
        self.assertFalse(Parser.matches_rule_declaration('myRule(a,b,c).'))

    def test_matches_contrary_declaration(self):
        self.assertTrue(Parser.matches_contrary_declaration('contrary(a, _a).'))
        self.assertTrue(Parser.matches_contrary_declaration('contrary(abc, bca).'))
        self.assertTrue(Parser.matches_contrary_declaration('contrary(sentence, _sentence).'))
        self.assertTrue(Parser.matches_contrary_declaration('contrary(a    ,    _a).'))
        self.assertFalse(Parser.matches_contrary_declaration('Contrary(a, b).'))
        self.assertFalse(Parser.matches_contrary_declaration('contrary(a, b, c).'))
        self.assertFalse(Parser.matches_contrary_declaration('contrary((A), (B)).'))
        self.assertFalse(Parser.matches_contrary_declaration('contrary(a, b'))

    def test_matches_random_variable_declaration(self):
        self.assertTrue(Parser.matches_random_variable_declaration('myRV(a, 0.5).'))
        self.assertTrue(Parser.matches_random_variable_declaration('myRV(abc, 0.00001).'))
        self.assertTrue(Parser.matches_random_variable_declaration('myRV(rv, 1).'))
        self.assertTrue(Parser.matches_random_variable_declaration('myRV(a,0.1).'))
        self.assertFalse(Parser.matches_random_variable_declaration('MyRV(a, 0.1).'))
        self.assertFalse(Parser.matches_random_variable_declaration('myRV(a, b, 0.4'))
        self.assertFalse(Parser.matches_random_variable_declaration('myRv(a, 0.4).'))
        self.assertFalse(Parser.matches_random_variable_declaration('myRV(abc, 0.9)'))

    def test_matches_conditional_random_variable_declaration(self):
        self.assertFalse(Parser.matches_random_variable_declaration('myRV(a, [b], [(b): 0.4, (~b): 0.3]).'))
        self.assertTrue(Parser.matches_conditional_random_variable_declaration('myRV(a, [b], [(b): 0.4, (~b): 0.3]).'))
        self.assertFalse(Parser.matches_random_variable_declaration(
            'myRV(a, [b, c], [(b,c): 0.2, (b,~c): 0.4, (~b, c): 0.1, (~b, ~c): 0.7)]).'))
        self.assertTrue(Parser.matches_conditional_random_variable_declaration(
            'myRV(a, [b, c], [(b,c): 0.2, (b,~c): 0.4, (~b, c): 0.1, (~b, ~c): 0.7)]).'))
        self.assertFalse(Parser.matches_random_variable_declaration(
            'myRV( a , [ c ] , [(~c) : 0.3, (c): 0.2]).'))
        self.assertTrue(Parser.matches_conditional_random_variable_declaration(
            'myRV( a , [ c ] , [(~c) : 0.3, (c): 0.2]).'))

    def test_extract_assumption(self):
        self.assertEqual(Parser.extract_assumption('myAsm(a).'), Semantics.Sentence('a'))
        self.assertEqual(Parser.extract_assumption('myAsm(myAsm).'), Semantics.Sentence('myAsm'))
        self.assertEqual(Parser.extract_assumption('myAsm(As09).'), Semantics.Sentence('As09'))
        self.assertEqual(Parser.extract_assumption('myAsm(abcde).'), Semantics.Sentence('abcde'))

    def test_extract_rule(self):
        self.assertEqual(Parser.extract_rule('myRule(a, [b,c]).', []), Semantics.Rule(a, [b, c]))
        self.assertEqual(Parser.extract_rule('myRule(a,[b , c,    d]).', []), Semantics.Rule(a, [b, c, d]))
        self.assertEqual(Parser.extract_rule('myRule(abc, [ab, bc, bd]).', []), Semantics.Rule(abc, [ab, bc, bd]))
        self.assertEqual(Parser.extract_rule('myRule(t, [a, b, c]).', []), Semantics.Rule(t, [a, b, c]))

    def test_extract_contrary(self):
        self.assertEqual(Parser.extract_contrary('contrary(a, _a).'), Semantics.Contrary(a, _a))
        self.assertEqual(Parser.extract_contrary('contrary(abc, t).'), Semantics.Contrary(abc, t))
        self.assertEqual(Parser.extract_contrary('contrary(sentence, _sentence).'), Semantics.Contrary(sentence, _sentence))
        self.assertEqual(Parser.extract_contrary('contrary(a    ,    _a).'), Semantics.Contrary(a, _a))

    def test_extract_random_variable(self):
        self.assertEqual((Semantics.Sentence('a', random_variable=True), 0.5),
                         Parser.extract_random_variable('myRV(a, 0.5).'))
        self.assertEqual((Semantics.Sentence('abc', random_variable=True), 0.00001),
                         Parser.extract_random_variable('myRV(abc, 0.00001).'))
        self.assertEqual((Semantics.Sentence('t', random_variable=True), 1),
                         Parser.extract_random_variable('myRV(t, 1).'))
        self.assertEqual((Semantics.Sentence('a', random_variable=True), 0.1),
                         Parser.extract_random_variable('myRV(a,0.1).'))

    def test_extract_conditional_variables(self):
        variables = '[a, b]'
        extracted_variables = Parser.extract_conditional_variables(variables)
        self.assertEqual(2, len(extracted_variables))
        self.assertTrue(all([elem in [Semantics.Sentence('a', random_variable=True),
                                      Semantics.Sentence('b', random_variable=True)]
                             for elem in extracted_variables]))

        variables = '[a  ,  c, b  ]'
        extracted_variables = Parser.extract_conditional_variables(variables)
        self.assertEqual(3, len(extracted_variables))
        self.assertTrue(all([elem in [Semantics.Sentence('a', random_variable=True),
                                      Semantics.Sentence('b', random_variable=True),
                                      Semantics.Sentence('c', random_variable=True)]
                             for elem in extracted_variables]))

        variables = '[c  ,  a ]'
        extracted_variables = Parser.extract_conditional_variables(variables)
        self.assertEqual(2, len(extracted_variables))
        self.assertTrue(all([elem in [Semantics.Sentence('a', random_variable=True),
                                      Semantics.Sentence('c', random_variable=True)]
                             for elem in extracted_variables]))

        rv_a = Semantics.Sentence('a', random_variable=True)
        rv_b = Semantics.Sentence('b', random_variable=True)
        rv_c = Semantics.Sentence('c', random_variable=True)
        self.assertTrue(rv_a in Parser.extract_conditional_variables("[ a]"))
        self.assertTrue(all(elem in [rv_a, rv_b, rv_c] for elem in Parser.extract_conditional_variables("[b, c , a]")))

    def test_extract_conditional_probability(self):
        test_map = {"b": 0.4, "~b": 0.3}
        extracted_map = Parser.extract_conditional_probabilities('[b: 0.4, ~b: 0.3]')
        self.assertEqual(len(test_map), len(extracted_map))
        self.assertEqual(test_map['b'], extracted_map['b'])
        self.assertEqual(test_map['~b'], extracted_map['~b'])

        test_map = {"bc": 0.2, "b~c": 0.4, "~bc": 0.1, "~b~c": 0.7}
        extracted_map = Parser.extract_conditional_probabilities(
            '[bc: 0.2, b~c: 0.4, ~bc: 0.1, ~b~c: 0.7]')
        self.assertEqual(len(test_map), len(extracted_map))
        self.assertEqual(test_map['bc'], extracted_map['bc'])
        self.assertEqual(test_map['bc'], extracted_map['bc'])
        self.assertEqual(test_map['~bc'], extracted_map['~bc'])
        self.assertEqual(test_map['~b~c'], extracted_map['~b~c'])

        test_map = {"~c": 0.3, "c": 0.2}
        extracted_map = Parser.extract_conditional_probabilities('[~c : 0.3, c: 0.2]')
        self.assertEqual(len(test_map), len(extracted_map))
        self.assertEqual(test_map['c'], extracted_map['c'])
        self.assertEqual(test_map['~c'], extracted_map['~c'])

    def test_extract_conditional_random_variable(self):
        cond_prob = Bayesian.ConditionalProbability(rv_a, [rv_b], {'b': 0.4, '~b': 0.3})
        parsed_rv, parsed_probability = Parser.extract_conditional_random_variable(
            'myRV(a, [b], [b: 0.4, ~b: 0.3]).')
        self.assertEqual(Semantics.Sentence('a', random_variable=True), parsed_rv)
        self.assertTrue(cond_prob == parsed_probability)

        cond_prob = Bayesian.ConditionalProbability(rv_a, [rv_b, rv_c], {'bc': 0.2, 'b~c': 0.4, '~bc': 0.1, '~b~c': 0.7})
        parsed_rv, parsed_probability = Parser.extract_conditional_random_variable(
            'myRV(a, [b, c], [bc: 0.2, b~c: 0.4, ~bc: 0.1, ~b~c: 0.7]).')
        self.assertEqual(Semantics.Sentence('a', random_variable=True), parsed_rv)
        self.assertTrue(cond_prob == parsed_probability)

        cond_prob = Bayesian.ConditionalProbability(rv_a, [rv_c], {'c': 0.2, '~c': 0.3})
        parsed_rv, parsed_probability = Parser.extract_conditional_random_variable(
            'myRV( a , [ c ] , [~c : 0.3, c: 0.2]).')
        self.assertEqual(Semantics.Sentence('a', random_variable=True), parsed_rv)
        self.assertTrue(cond_prob == parsed_probability)

    def test_extract_from_parentheses(self):
        self.assertEqual(Parser.extract_from_parentheses('myAsm(abcde).'), 'abcde')
        self.assertEqual(Parser.extract_from_parentheses('myAsm(a123b).'), 'a123b')
        self.assertEqual(Parser.extract_from_parentheses('myAsm(  abc  ).'), 'abc')
        self.assertEqual(Parser.extract_from_parentheses('myAsm(arg).'), 'arg')
        self.assertEqual(Parser.extract_from_parentheses('myAsm(ARG).'), 'ARG')

    def test_extract_from_square_brackets(self):
        self.assertEqual(Parser.extract_from_square_brackets(' [ a ] '), 'a')
        self.assertEqual(Parser.extract_from_square_brackets('[abcd].'), 'abcd')
        self.assertEqual(Parser.extract_from_square_brackets('[ abb]'), 'abb')
        self.assertEqual(Parser.extract_from_square_brackets('[]'), '')

    def test_parse_program_from_string(self):
        parser = Parser.BABAProgramParser(string=program_1_string)
        baba = parser.parse()
        self.assertTrue(all([elem in baba.language for elem in [a, _a, b, _b, c, _c, d, _d, e, _e]]))
        self.assertEqual(11, len(baba.language))
        self.assertTrue(all([elem in baba.assumptions for elem in [a, b, c, d, e]]))
        self.assertEqual(5, len(baba.assumptions))
        self.assertTrue(all([elem in baba.contraries for elem in [a, b, c, d, e]]))
        self.assertEqual(5, len(baba.contraries))
        self.assertIn(Semantics.Sentence('t', random_variable=True), baba.random_variables)
        self.assertEqual(1, len(baba.random_variables))
        self.assertEqual(5, len(baba.rules))

    def test_parse_program_from_file(self):
        parser = Parser.BABAProgramParser(filename='BABA_program_1')
        baba = parser.parse()
        self.assertTrue(all([elem in baba.language for elem in [a, _a, b, _b, c, _c, d, _d, e, _e]]))
        self.assertEqual(11, len(baba.language))
        self.assertTrue(all([elem in baba.assumptions for elem in [a, b, c, d, e]]))
        self.assertEqual(5, len(baba.assumptions))
        self.assertTrue(all([elem in baba.contraries for elem in [a, b, c, d, e]]))
        self.assertEqual(5, len(baba.contraries))
        self.assertIn(Semantics.Sentence('t', random_variable=True), baba.random_variables)
        self.assertEqual(1, len(baba.random_variables))
        self.assertEqual(5, len(baba.rules))

    def test_integration_stable_sets(self):
        parser = Parser.BABAProgramParser(string=program_1_string)
        baba = parser.parse()
        stable_sets = Semantics.stable(baba)
        self.assertEqual(2, len(stable_sets))
        self.assertTrue(all([(elem in stable_sets[0].elements or elem in stable_sets[1].elements) for elem in [a, c, e]]))
        self.assertTrue(all([(elem in stable_sets[0].elements or elem in stable_sets[1].elements) for elem in [b, d]]))

    def test_integration_complete_sets(self):
        parser = Parser.BABAProgramParser(filename='BABA_program_2')
        baba = parser.parse()
        complete_sets = Semantics.complete(baba)
        self.assertEqual(6, len(complete_sets))

    def test_integration_framework_with_random_variables(self):
        parser = Parser.BABAProgramParser(filename='BABA_program_3')
        baba = parser.parse()
        self.assertEqual(0.64, Semantics.semantic_probability(Semantics.GROUNDED, baba, [ExampleFrameworks.j]))
        self.assertEqual(0.64, Semantics.semantic_probability(Semantics.GROUNDED, baba, [a]))
        self.assertEqual(0.64, Semantics.semantic_probability(Semantics.GROUNDED, baba, [a, ExampleFrameworks.j]))
        self.assertEqual(0.6, Semantics.semantic_probability(Semantics.GROUNDED, baba, [b]))
        self.assertEqual(1.0, Semantics.semantic_probability(Semantics.GROUNDED, baba, [c]))

    def test_integration_framework_with_conditional_random_variables(self):
        parser = Parser.BABAProgramParser(filename='BABA_program_4')
        baba = parser.parse()
        a_prob = Semantics.semantic_probability(Semantics.GROUNDED, baba, [ExampleFrameworks.a])
        self.assertTrue(True)
