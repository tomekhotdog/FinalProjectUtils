import unittest
from Parsing import BABAProgramParser as Parser
import Semantics

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

    def test_extract_assumption(self):
        self.assertEqual(Parser.extract_assumption('myAsm(a).'), Semantics.Sentence('a'))
        self.assertEqual(Parser.extract_assumption('myAsm(myAsm).'), Semantics.Sentence('myAsm'))
        self.assertEqual(Parser.extract_assumption('myAsm(As09).'), Semantics.Sentence('As09'))
        self.assertEqual(Parser.extract_assumption('myAsm(abcde).'), Semantics.Sentence('abcde'))

    def test_extract_rule(self):
        self.assertEqual(Parser.extract_rule('myRule(a, [b,c]).'), Semantics.Rule(a, [b, c]))
        self.assertEqual(Parser.extract_rule('myRule(a,[b , c,    d]).'), Semantics.Rule(a, [b, c, d]))
        self.assertEqual(Parser.extract_rule('myRule(abc, [ab, bc, bd]).'), Semantics.Rule(abc, [ab, bc, bd]))
        self.assertEqual(Parser.extract_rule('myRule(t, [a, b, c]).'), Semantics.Rule(t, [a, b, c]))

    def test_extract_contrary(self):
        self.assertEqual(Parser.extract_contrary('contrary(a, _a).'), Semantics.Contrary(a, _a))
        self.assertEqual(Parser.extract_contrary('contrary(abc, t).'), Semantics.Contrary(abc, t))
        self.assertEqual(Parser.extract_contrary('contrary(sentence, _sentence).'), Semantics.Contrary(sentence, _sentence))
        self.assertEqual(Parser.extract_contrary('contrary(a    ,    _a).'), Semantics.Contrary(a, _a))

    def test_extract_random_variable(self):
        self.assertEqual(Parser.extract_random_variable('myRV(a, 0.5).'), Semantics.RandomVariable(a, 0.5))
        self.assertEqual(Parser.extract_random_variable('myRV(abc, 0.00001).'), Semantics.RandomVariable(abc, 0.00001))
        self.assertEqual(Parser.extract_random_variable('myRV(t, 1).'), Semantics.RandomVariable(t, 1))
        self.assertEqual(Parser.extract_random_variable('myRV(a,0.1).'), Semantics.RandomVariable(a, 0.1))

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
        self.assertIn(Semantics.RandomVariable(t, 0.5), baba.random_variables)
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
        self.assertIn(Semantics.RandomVariable(t, 0.5), baba.random_variables)
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
