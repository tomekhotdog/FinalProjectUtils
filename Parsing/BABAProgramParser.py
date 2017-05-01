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
            self.parse_program(self.STRING.split('\n'))
        elif self.FILENAME:
            file = open(self.FILENAME, 'r')
            self.parse_program(file)
            file.close()

    def parse_program(self, program):
        self.reset_program_elements()

        for line in program:
            print(line)


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
# random_variable_regex = '\s*myRV\(\s*[\w]+\s*,\s*\d*\.?\d*\s*\)\.\s*'


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
    return None


def extract_contrary(contrary):
    return None


def extract_random_variable(random_variable):
    return Semantics.Sentence('a')


# Utility method that extracts the string from input of format: [\w]*\(<element>\)[\w]*
def extract_from_parentheses(input_string):
    return (input_string.split('(')[1]).split(')')[0].strip()

