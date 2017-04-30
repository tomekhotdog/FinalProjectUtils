import Semantics

a = Semantics.Sentence('a')
b = Semantics.Sentence('b')
c = Semantics.Sentence('c')
d = Semantics.Sentence('d')
e = Semantics.Sentence('e')
f = Semantics.Sentence('f')
g = Semantics.Sentence('g')
h = Semantics.Sentence('h')
i = Semantics.Sentence('i')

_a = Semantics.Sentence('_a')
_b = Semantics.Sentence('_b')
_c = Semantics.Sentence('_c')
_d = Semantics.Sentence('_d')
_e = Semantics.Sentence('_e')
_f = Semantics.Sentence('_f')

def valid_BABA_framework():
    language = [a, b, c, d, e, f]
    rules = [Semantics.Rule(a, [b, c])]
    assumptions = [b, c]
    contraries = {b: Semantics.Contrary(b, d), c: Semantics.Contrary(c, e)}
    random_variables = [Semantics.RandomVariable(f, 0.8)]
    return Semantics.BABA(language, rules, assumptions, contraries, random_variables)


def with_no_contraries():
    language = [a, b, c, d, e, f]
    rules = [Semantics.Rule(a, [b, c])]
    assumptions = [b, c]
    return Semantics.BABA(language, rules, assumptions, {}, [])


def with_chaining():
    language = [a, b, c, d, e, f, g]
    rules = [Semantics.Rule(a, [b, c]), Semantics.Rule(c, [d, e]), Semantics.Rule(e, [f]), Semantics.Rule(g, [c])]
    assumptions = [b, d, f]
    return Semantics.BABA(language, rules, assumptions, {}, [])


def with_contraries():
    language = [a, b, c, d, e, f, g, h, i]
    rules = [Semantics.Rule(a, [d, e]), Semantics.Rule(b, [f, g]), Semantics.Rule(c, [h, i])]
    assumptions = [d, e, f, g, h, i]
    contraries = {b: Semantics.Contrary(b, d), c: Semantics.Contrary(c, e)}
    return Semantics.BABA(language, rules, assumptions, contraries, [])


def larger_framework():
    language = [a, b, c, d, e, f, g, h, i]
    rules = [Semantics.Rule(a, [b]), Semantics.Rule(a, [e, f]),
             Semantics.Rule(c, [d, e, f]), Semantics.Rule(d, [g,  h]),
             Semantics.Rule(d, [i])]
    assumptions = [b, e, f, g, h, i]
    contraries = {b: Semantics.Contrary(b, c)}
    return Semantics.BABA(language, rules, assumptions, contraries, [])


########################################################################################
#  __Venice framework__
#  Typical non trivial framework. Visual representation (for AA equivalent):
#
#                  a  <--  b  <--  c  <--  d  <---> e
#
# With two stable / semi-stable / complete / preferred extensions: {a, c, e} and {b, d}
# With one grounded / ideal extensions: {}
#
def venice_framework():
    language = [a, _a, b, _b, c, _c, d, _d, e, _e]
    rules = [Semantics.Rule(_a, [b]), Semantics.Rule(_b, [c]),
             Semantics.Rule(_c, [d]), Semantics.Rule(_d, [e]),
             Semantics.Rule(_e, [d])]
    assumptions = [a, b, c, d, e]
    contraries = {a: Semantics.Contrary(a, _a), b: Semantics.Contrary(b, _b),
                  c: Semantics.Contrary(c, _c), d: Semantics.Contrary(d, _d),
                  e: Semantics.Contrary(e, _e)}
    return Semantics.BABA(language, rules, assumptions, contraries, [])

########################################################################################


########################################################################################
# __s_framework__
# Non trivial framework with sceptical solutions.
# Visual representation (for AA equivalent):
#
#      a <---> b --> c --> d <---> e       f.
#
def s_framework():
    language = [a, _a, b, _b, c, _c, d, _d, e, _e, f, _f]
    rules = [Semantics.Rule(_a, [b]), Semantics.Rule(_b, [a]),
             Semantics.Rule(_c, [b]), Semantics.Rule(_d, [c]),
             Semantics.Rule(_e, [d]), Semantics.Rule(_d, [e])]
    assumptions = [a, b, c, d, e, f]
    contraries = {a: Semantics.Contrary(a, _a), b: Semantics.Contrary(b, _b),
                  c: Semantics.Contrary(c, _c), d: Semantics.Contrary(d, _d),
                  e: Semantics.Contrary(e, _e), f: Semantics.Contrary(f, _f)}
    return Semantics.BABA(language, rules, assumptions, contraries, [])

########################################################################################

# Language property does not cover framework
def invalid_BABA_framework():
    language = []
    rules = [Semantics.Rule(a, [b, c])]
    assumptions = [b, c]
    contraries = {b: Semantics.Contrary(b, d), c: Semantics.Contrary(c, e)}
    random_variables = [Semantics.RandomVariable(f, 0.8)]
    return Semantics.BABA(language, rules, assumptions, contraries, random_variables)


# Framework is not flat
def invalid_non_flat_framework():
    language = [a, b, c]
    rules = [Semantics.Rule(a, [b, c])]
    assumptions = [a, b, c]
    contraries = {}
    random_variables = []
    return Semantics.BABA(language, rules, assumptions, contraries, random_variables)
