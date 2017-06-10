import unittest

from PythonSemantics import ExampleFrameworks, Semantics
from PythonSemantics.Parsing import BABAProgramParser as Parser

program_1_string = "myAsm(a).\nmyAsm(b).\nmyAsm(c).\nmyAsm(d).\nmyAsm(e).\n" \
         "contrary(a, _a).\ncontrary(b, _b).\ncontrary(c, _c).\ncontrary(d, _d)." \
         "\ncontrary(e, _e).\nmyRule(_b, [c]).\nmyRule(_a, [b])." \
         "\nmyRule(_c, [d]).\nmyRule(_d, [e]).\nmyRule(_e, [d]).\nmyRV(t, 0.5)."


class TestIntegration(unittest.TestCase):

    def test_integration_stable_sets(self):
        parser = Parser.BABAProgramParser(string=program_1_string)
        baba = parser.parse()
        stable_sets = Semantics.stable(baba)
        self.assertEqual(2, len(stable_sets))
        self.assertTrue(
            all([(elem in stable_sets[0].elements or elem in stable_sets[1].elements) for elem in
                 [ExampleFrameworks.a, ExampleFrameworks.c, ExampleFrameworks.e]]))
        self.assertTrue(all([(elem in stable_sets[0].elements or elem in stable_sets[1].elements) for elem in
                             [ExampleFrameworks.b, ExampleFrameworks.d]]))

    def test_integration_complete_sets(self):
        parser = Parser.BABAProgramParser(filename='../PythonSemantics/Parsing/BABA_program_2')
        baba = parser.parse()
        complete_sets = Semantics.complete(baba)
        self.assertEqual(6, len(complete_sets))

    def test_integration_framework_with_random_variables(self):
        parser = Parser.BABAProgramParser(filename='../PythonSemantics/Parsing/BABA_program_3')
        baba = parser.parse()
        self.assertEqual(0.64, Semantics.semantic_probability(Semantics.GROUNDED, baba, [ExampleFrameworks.j]))
        self.assertEqual(0.64, Semantics.semantic_probability(Semantics.GROUNDED, baba, [ExampleFrameworks.a]))
        self.assertEqual(0.64, Semantics.semantic_probability(Semantics.GROUNDED, baba, [ExampleFrameworks.a, ExampleFrameworks.j]))
        self.assertEqual(0.6, Semantics.semantic_probability(Semantics.GROUNDED, baba, [ExampleFrameworks.b]))
        self.assertEqual(1.0, Semantics.semantic_probability(Semantics.GROUNDED, baba, [ExampleFrameworks.c]))

    def test_integration_framework_with_conditional_random_variables(self):
        parser = Parser.BABAProgramParser(filename='../PythonSemantics/Parsing/BABA_program_4')
        baba = parser.parse()
        lang_prob = Semantics.compute_semantic_probability(Semantics.GROUNDED, baba)
        self.assertAlmostEqual(0.775, lang_prob[ExampleFrameworks.b.symbol])
        self.assertAlmostEqual(0.6625, lang_prob[ExampleFrameworks.c.symbol])
        self.assertAlmostEqual(0.45, lang_prob['o'])
        self.assertAlmostEqual(0.75, lang_prob['p'])
        self.assertAlmostEqual(1.0, lang_prob[ExampleFrameworks.d.symbol])
        self.assertAlmostEqual(1.0, lang_prob[ExampleFrameworks.e.symbol])

    def test_integration_framework_with_one_conditional_random_variable(self):
        parser = Parser.BABAProgramParser(filename='../PythonSemantics/Parsing/BABA_program_5')
        baba = parser.parse()
        lang_prob = Semantics.compute_semantic_probability(Semantics.GROUNDED, baba)
        self.assertAlmostEqual(0.2, lang_prob[ExampleFrameworks.a.symbol])

    def test_integration_cow_framework(self):
        baba = Parser.BABAProgramParser(filename='../PythonSemantics/Parsing/BABA_cow_program').parse()
        lang_prob = Semantics.compute_semantic_probability(Semantics.GROUNDED, baba)
        self.assertAlmostEqual(0.72, lang_prob[ExampleFrameworks.HP.symbol])
