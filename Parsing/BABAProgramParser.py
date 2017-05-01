import Semantics
import re

FILENAME = 'filename'
STRING = 'string'


# Class for parsing an BABA program from string or file
# The String or File is provided in the constructor (precedence for String)
# Example usage:
#    1) BABAProgramParser(string='~program input as string~')
#    2) BABAProgramParser(filename='file_location')
class BABAProgramParser:
    def __init__(self, *args, **kwargs):
        self.reset_program_elements()

        if STRING in kwargs:
            self.STRING = kwargs[STRING]
            self.FILENAME = None
        elif FILENAME in kwargs:
            self.FILENAME = kwargs[FILENAME]
            self.STRING = None

    def reset_program_elements(self):
        self.language = []
        self.assumptions = []
        self.rules = []
        self.contraries = {}
        self.random_variables = []

    def parse(self):
        if self.STRING:
            return self.parse_program(self.STRING.split('\n'))
        elif self.FILENAME:
            file = open(self.FILENAME, 'r')
            baba = self.parse_program(file)
            file.close()
            return baba

    def parse_program(self, program):
        self.reset_program_elements()

        rules = [] # Parse rules at the end

        for line in program:
            print(line)
            if matches_rule_declaration(line):
                rules.append(line)

            elif matches_assumption_declaration(line):
                assumption = extract_assumption(line)
                self.assumptions.append(assumption)
                self.language.append(assumption)

            elif matches_contrary_declaration(line):
                contrary = extract_contrary(line)
                self.contraries[contrary.assumption] = contrary
                self.language.append(contrary.contrary)

            elif matches_random_variable_declaration(line):
                rv = extract_random_variable(line)
                self.random_variables.append(rv)
                self.language.append(rv)

        for rule in rules:
            extracted_rule = extract_rule(rule)
            self.rules.append(extracted_rule)

        return Semantics.BABA(self.language, self.rules, self.assumptions, self.contraries, self.random_variables)


class ProgramParseException(Exception):
    def __init__(self, message):
        self.message = message


#########################################################################################
# The following boolean method return matches to the corresponding program element syntax
#########################################################################################

decimal_number_regex = '\d*\.?\d*'
assumption_regex = '\s*myAsm\([\w]+\)\.\s*$'
rule_regex = '\s*myRule\(\s*[\w]+\s*,\s*\[([\w]|,|\s*)+\]\)\.\s*$'
contrary_regex = '\s*contrary\(\s*[\w]+\s*,\s*[\w]+\s*\)\.\s*$'
random_variable_regex = '\s*myRV\(\s*[\w]+\s*,\s*' + decimal_number_regex + '\s*\)\.\s*'


# myAsm(sentence).
def matches_assumption_declaration(assumption):
    return True if(re.match(assumption_regex, assumption)) else False


# myRule(sentence, [sentences]).
def matches_rule_declaration(rule):
    return True if re.match(rule_regex, rule) else False


# contrary(sentence, contrary).
def matches_contrary_declaration(contrary):
    return True if re.match(contrary_regex, contrary) else False


# myRV(sentence).
def matches_random_variable_declaration(random_variable):
    return True if re.match(random_variable_regex, random_variable) else False


############################################################################
# The following methods extract and return the corresponding program element
############################################################################

def extract_assumption(assumption):
    if not matches_assumption_declaration(assumption):
        raise ProgramParseException("Provided assumption does not match required format")
    return Semantics.Sentence(extract_from_parentheses(assumption))


def extract_rule(rule):
    if not matches_rule_declaration(rule):
        raise ProgramParseException("Provided rule does not match required format")

    extracted = extract_from_parentheses(rule).split(',', 1)
    head = Semantics.Sentence(extracted[0].strip())
    body = [Semantics.Sentence(elem.strip()) for elem in extract_from_square_brackets(extracted[1].strip()).split(',')]
    return Semantics.Rule(head, body)


def extract_contrary(contrary):
    if not matches_contrary_declaration(contrary):
        raise ProgramParseException("Provided contrary does not match required format")

    extracted = extract_from_parentheses(contrary).split(',')
    assumption = Semantics.Sentence(extracted[0].strip())
    contrary = Semantics.Sentence(extracted[1].strip())
    return Semantics.Contrary(assumption, contrary)


def extract_random_variable(random_variable):
    if not matches_random_variable_declaration(random_variable):
        raise ProgramParseException("Provided random variable does not match required format")

    extracted = extract_from_parentheses(random_variable).split(',')
    rv = Semantics.Sentence(extracted[0].strip())
    probability = float(extracted[1].strip())
    return Semantics.RandomVariable(rv, probability)


# Utility method that extracts the string from input of format: [\w]*\(<element>\)[\w]*
def extract_from_parentheses(input_string):
    return (input_string.split('(')[1]).split(')')[0].strip()


# Utility method that extracts the string from input of format: [\w]*[(<element>\][\w]*
def extract_from_square_brackets(input_string):
    return (input_string.split('[')[1]).split(']')[0].strip()