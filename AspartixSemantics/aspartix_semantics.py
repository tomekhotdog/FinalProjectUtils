from AspartixSemantics.abap_parser import *
from AspartixSemantics.aspartix_interface import *
from AspartixSemantics.aba_plus_ import *

SOLVER_INPUT = "input_for_solver.lp"
TURNSTILE = "&#x22a2;"
R_ARROW = "&rarr;"
L_ARROW = "&larr;"
OVERLINE = "<span style=\"text-decoration: overline\">{}</span>"

BOTH_ATTACKS = 3

STABLE = 1
GROUNDED = 2
COMPLETE = 3
PREFERRED = 4
IDEAL = 5


extension_type_names = {STABLE: "stable", GROUNDED: "grounded",
                      COMPLETE: "complete", PREFERRED: "preferred", IDEAL: "ideal"}

attack_type_names = {NORMAL_ATK: "normal attack", REVERSE_ATK: "reverse attack", BOTH_ATTACKS: "both attacks"}


def create_aba_framework(framework_string):
    rules_added = None
    res = generate_aba_plus_framework(framework_string)
    abap = res[0]

    return abap


def compute_semantics(framework_string):
    rules_added = None
    res = generate_aba_plus_framework(framework_string)
    abap = res[0]

    # reverse dictionary to map sentences to contraries
    contr_map = dict((v, k) for k, v in res[1].items())

    res = abap.generate_arguments_and_attacks_for_contraries()
    attacks = res[1]
    deductions = res[2]

    set_attacks = convert_to_attacks_between_sets(res[1])

    asp = ASPARTIX_Interface(abap)
    asp.generate_input_file_for_clingo(SOLVER_INPUT)

    stable_ext = asp.calculate_stable_arguments_extensions(SOLVER_INPUT)
    grounded_ext = asp.calculate_grounded_arguments_extensions(SOLVER_INPUT)
    complete_ext = asp.calculate_complete_arguments_extensions(SOLVER_INPUT)
    preferred_ext = asp.calculate_preferred_arguments_extensions(SOLVER_INPUT)
    ideal_ext = asp.calculate_ideal_arguments_extensions(SOLVER_INPUT)

    stable_list = [ext for (ext, _) in stable_ext.items()]
    grounded_list = [ext for (ext, _) in grounded_ext.items()]
    complete_list = [ext for (ext, _) in complete_ext.items()]
    preferred_list = [ext for (ext, _) in preferred_ext.items()]
    ideal_list = [ext for (ext, _) in ideal_ext.items()]

    return stable_list, grounded_list, complete_list, preferred_list, ideal_list


def compute_stable(framework_string):
    rules_added = None
    res = generate_aba_plus_framework(framework_string)
    abap = res[0]

    # reverse dictionary to map sentences to contraries
    contr_map = dict((v, k) for k, v in res[1].items())

    res = abap.generate_arguments_and_attacks_for_contraries()
    attacks = res[1]
    deductions = res[2]

    set_attacks = convert_to_attacks_between_sets(res[1])

    asp = ASPARTIX_Interface(abap)
    asp.generate_input_file_for_clingo(SOLVER_INPUT)

    stable_ext = asp.calculate_stable_arguments_extensions(SOLVER_INPUT)

    return [ext for (ext, _) in stable_ext.items()]


def sets_to_str(sets, contr_map={}):
    """
    :param sets: set of sets of Sentences to format
    :param contr_map: dictionary mapping symbols of contraries to symbols of assumptions (default empty)
    :return: formatted string representation of sets
    """
    str = ""

    it = iter(sets)
    first_set = next(it, None)
    if first_set is not None:
        str += set_to_str(first_set, contr_map)
    for set in it:
        str += ", "
        str += set_to_str(set, contr_map)

    return str

def set_to_str(set, contr_map={}):
    """
    :param set: set of Sentences to format
    :param contr_map: dictionary mapping symbols of contraries to symbols of assumptions (default empty)
    :return: formatted string representation of sets
    """
    str = "{"

    it = iter(set)
    first_sentence = next(it, None)
    if first_sentence is not None:
        str += sentence_to_str(first_sentence, contr_map)
    for sentence in it:
        str += ", "
        str += sentence_to_str(sentence, contr_map)

    str += "}"

    return str

def sentence_to_str(sentence, contr_map={}):
    """
    :param sentence: Sentence to format
    :param contr_map: dictionary mapping symbols of contraries to symbols of assumptions (default empty)
    :return: formatted string representation of sentence
    """
    if sentence.is_contrary:
        if sentence.symbol in contr_map:
            return contr_map[sentence.symbol]
        return OVERLINE.format(sentence.symbol)
    else:
        return sentence.symbol

def set_atk_to_str(atk):
    """
    :param atk: tuple with 3 elements representing an attack between 2 sets:
                1: attacking set of Sentences
                2: attack type
                3: attacked set of Sentences
    :return: formatted string representation of atk
    """
    str = ""

    type = atk[2]
    if type == NORMAL_ATK:
        str = "Normal Attack: "
    elif type == REVERSE_ATK:
        str = "Reverse Attack: "

    str += set_to_str(atk[0])
    str += " {} ".format(R_ARROW)
    str += set_to_str(atk[1])

    return str

def arguments_extensions_to_str_list(extensions_dict, contr_map={}):
    """
    :param extensions_dict: dictionary mapping sets to their conclusions
    :param contr_map: dictionary mapping symbols of contraries to symbols of assumptions (default empty)
    :return: list of formatted arguments(deductions)
    """
    res = []

    for extension, conclusions in extensions_dict.items():
        res.append(argument_to_str(extension, conclusions, contr_map))

    return res

def argument_to_str(premise, conclusion, contr_map={}):
    """
    :param premise: set of Sentences representing the premise
    :param conclusion: set of Sentences representing the conclusion
    :param contr_map: dictionary mapping symbols of contraries to symbols of assumptions (default empty)
    :return: formatted argument(deduction)
    """
    str = ""
    str += set_to_str(premise)
    str += " {} ".format(TURNSTILE)
    str += set_to_str(conclusion, contr_map)
    return str

def rules_to_str(rules, contr_map):
    """
    :param rules: collection of Rules to format
    :param contr_map: dictionary mapping symbols of contraries to symbols of assumptions (default empty)
    :return: formatted string representation of rules
    """
    str = ""

    for rule in rules:
        str += rule_to_str(rule, contr_map)

    return str

def rule_to_str(rule, contr_map):
    """
    :param rule: Rule to format
    :param contr_map: dictionary mapping symbols of contraries to symbols of assumptions (default empty)
    :return: formatted string representation of rule
    """
    str = ""

    str += sentence_to_str(rule.consequent, contr_map)
    str += " {} ".format(L_ARROW)
    str += set_to_str(rule.antecedent)

    str += "<br/>"

    return str


