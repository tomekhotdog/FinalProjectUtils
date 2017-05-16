import Semantics
import Bayesian

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

s = Semantics.Sentence('s', random_variable=True)
t = Semantics.Sentence('t', random_variable=True)

_a = Semantics.Sentence('_a')
_b = Semantics.Sentence('_b')
_c = Semantics.Sentence('_c')
_d = Semantics.Sentence('_d')
_e = Semantics.Sentence('_e')
_f = Semantics.Sentence('_f')

HP = Semantics.Sentence('HP')
not_HP = Semantics.Sentence('not_HP')
HOC = Semantics.Sentence('HOC')
not_HOC = Semantics.Sentence('not_HOC')
CCA = Semantics.Sentence('CCA')
not_CCA = Semantics.Sentence('not_CCA')
FM = Semantics.Sentence('FM')
not_FM = Semantics.Sentence('not_FM')
JF = Semantics.Sentence('JF', random_variable=True, negation=False)
CM = Semantics.Sentence('CM', random_variable=True, negation=False)


def valid_BABA_framework():
    f = Semantics.Sentence('f', random_variable=True)
    language = [a, b, c, d, e, f]
    rules = [Semantics.Rule(a, [b, c])]
    assumptions = [b, c]
    contraries = {b: Semantics.Contrary(b, d), c: Semantics.Contrary(c, e)}
    random_variables = [f]
    return Semantics.BABA(language, rules, assumptions, contraries, random_variables, None)


def with_no_contraries():
    language = [a, b, c, d, e, f]
    rules = [Semantics.Rule(a, [b, c])]
    assumptions = [b, c]
    return Semantics.BABA(language, rules, assumptions, {}, [], None)


def with_chaining():
    language = [a, b, c, d, e, f, g]
    rules = [Semantics.Rule(a, [b, c]), Semantics.Rule(c, [d, e]), Semantics.Rule(e, [f]), Semantics.Rule(g, [c])]
    assumptions = [b, d, f]
    return Semantics.BABA(language, rules, assumptions, {}, [], None)


def with_contraries():
    language = [a, b, c, d, e, f, g, h, i]
    rules = [Semantics.Rule(a, [d, e]), Semantics.Rule(b, [f, g]), Semantics.Rule(c, [h, i])]
    assumptions = [d, e, f, g, h, i]
    contraries = {b: Semantics.Contrary(b, d), c: Semantics.Contrary(c, e)}
    return Semantics.BABA(language, rules, assumptions, contraries, [], None)


def larger_framework():
    language = [a, b, c, d, e, f, g, h, i, j]
    rules = [Semantics.Rule(a, [b]), Semantics.Rule(a, [e, f]),
             Semantics.Rule(c, [d, e, f]), Semantics.Rule(d, [g,  h]),
             Semantics.Rule(d, [i]), Semantics.Rule(j, [])]
    assumptions = [b, e, f, g, h, i]
    contraries = {b: Semantics.Contrary(b, c)}
    return Semantics.BABA(language, rules, assumptions, contraries, [], None)


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
    return Semantics.BABA(language, rules, assumptions, contraries, [], None)

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
    return Semantics.BABA(language, rules, assumptions, contraries, [], None)

########################################################################################


########################################################################################
# cow_framework
# Example 3 BABA framework as described in ['On Probabilistic Argumentation', 2016, Thang et al.]
def cow_framework():
    JN = Semantics.Sentence('JN')
    not_JN = Semantics.Sentence('not_JN')
    language = [HP, not_HP, HOC, not_HOC, CCA, not_CCA, FM, not_FM, JN, not_JN, JF, CM]
    rules = [Semantics.Rule(HP, [HOC, CCA, not_FM]), Semantics.Rule(HOC, []),
             Semantics.Rule(FM, [CM]), Semantics.Rule(CCA, [not_JN]), Semantics.Rule(JN, [JF])]
    assumptions = [not_HP, not_HOC, not_CCA, not_FM, not_JN]
    contraries = {not_HP: Semantics.Contrary(not_HP, HP), not_HOC: Semantics.Contrary(not_HOC, HOC),
                  not_CCA: Semantics.Contrary(not_CCA, CCA), not_FM: Semantics.Contrary(not_FM, FM),
                  not_JN: Semantics.Contrary(not_JN, JN)}
    random_variables = [JF, CM]
    BN = Bayesian.BayesianNetwork({CM.symbol: 0.1, JF.symbol: 0.8})
    return Semantics.BABA(language, rules, assumptions, contraries, random_variables, BN)

########################################################################################


########################################################################################

cond_JN = Semantics.Sentence('JN', random_variable=True)
cond_neg_JN = Semantics.Sentence('JN', random_variable=True, negation=True)


# conditional_cow_framework
# Example 6 BABA framework as described in ['On Probabilistic Argumentation', 2016, Thang et al.]
def conditional_cow_framework():
    language = [HP, not_HP, HOC, not_HOC, CCA, not_CCA, FM, not_FM, cond_JN, cond_neg_JN, JF, CM]
    rules = [Semantics.Rule(HP, [HOC, CCA, not_FM]), Semantics.Rule(HOC, []),
             Semantics.Rule(FM, [CM]), Semantics.Rule(CCA, [cond_neg_JN])]
    assumptions = [not_HP, not_HOC, not_CCA, not_FM]
    contraries = {not_HP: Semantics.Contrary(not_HP, HP), not_HOC: Semantics.Contrary(not_HOC, HOC),
                  not_CCA: Semantics.Contrary(not_CCA, CCA), not_FM: Semantics.Contrary(not_FM, FM)}
    random_variables = [cond_JN, JF, CM]
    BN = Bayesian.BayesianNetwork({cond_JN.symbol: Bayesian.ConditionalProbability(cond_JN.symbol, [JF], {"JF": 0.8, "~JF": 0.0}),
                                   JF.symbol: 0.25, CM.symbol: 0.1})
    return Semantics.BABA(language, rules, assumptions, contraries, random_variables, BN)

########################################################################################


########################################################################################
# BABA framework with random variables as body of rules
# Visual representation:
#
#    a   <-- {b, s} <-- {c, t}
#
def r_framework():
    language = [a, _a, b, _b, c, _c, j, t, s]
    rules = [Semantics.Rule(j, [a]), Semantics.Rule(_a, [b, s]), Semantics.Rule(_b, [c, t])]
    assumptions = [a, b, c]
    contraries = {a: Semantics.Contrary(a, _a), b: Semantics.Contrary(b, _b),
                  c: Semantics.Contrary(c, _c)}
    random_variables = [s, t]
    bayes_net = Bayesian.BayesianNetwork({s.symbol: 0.6, t.symbol: 0.4})
    return Semantics.BABA(language, rules, assumptions, contraries, random_variables, bayes_net)

########################################################################################


# Language property does not cover framework
def invalid_BABA_framework():
    language = []
    rules = [Semantics.Rule(a, [b, c])]
    assumptions = [b, c]
    contraries = {b: Semantics.Contrary(b, d), c: Semantics.Contrary(c, e)}
    random_variables = [Semantics.Sentence(f, random_variable=True, negation=True)]
    return Semantics.BABA(language, rules, assumptions, contraries, random_variables, None)


# Framework is not flat
def invalid_non_flat_framework():
    language = [a, b, c]
    rules = [Semantics.Rule(a, [b, c])]
    assumptions = [a, b, c]
    contraries = {}
    random_variables = []
    return Semantics.BABA(language, rules, assumptions, contraries, random_variables, None)
