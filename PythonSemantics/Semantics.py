from PythonSemantics.SemanticsUtils import *
import multiprocessing as mp
import copy

GROUNDED = 1
SCEPTICALLY_PREFERRED = 2
IDEAL = 3


# Bayesian Assumption-Based Argumentation
class BABA:
    # BABA = (F^A, BN, RV) where F^A = ABA framework: (L, R, A, _) (Language, Rules, Assumptions, Contraries),
        # BN = Bayesian network,
        # RV = Random variables
    # rules = [Rule(Sentence, [Sentence])...]
    # contraries = {Sentence (assumption) : Contrary}
    # random_variables = [RandomVariable(Sentence, Probability)...]
    def __init__(self, language, rules, assumptions, contraries, random_variables, BN):
        self.language = set(language)
        self.rules = rules
        self.assumptions = set(assumptions)
        self.contraries = contraries
        self.random_variables = set(random_variables)
        self.BN = BN
        self.rv_world = []

        self.validate()

        self.derivable_dictionary = {}
        self.derived_claims = {}
        self.attacks = {}

        self.compute_derivable_dictionary()
        self.compute_attacks()

    # Validates BABA framework
    def validate(self):
        self.validate_language_covers_all_sentences()
        self.validate_is_flat()
        self.validate_random_variables()

    # Sets the world of random variables for semantics calculations
    def set_random_variable_world(self, random_variable_world):
        self.rv_world = random_variable_world

    # Checks whether all atoms defined in rules, assumptions,
    # contraries and random variables are included in the language
    def validate_language_covers_all_sentences(self):
        exception_message = "Language must include all sentences defined in network"
        for rule in self.rules:
            if rule.head not in self.language:
                raise InvalidBABAException(exception_message)
            for element in rule.body:
                if element not in self.language:
                    raise InvalidBABAException(exception_message)

        for assumption in self.assumptions:
            if assumption not in self.language:
                raise InvalidBABAException(exception_message)

        for assumption, contrary in self.contraries.items():
            if assumption not in self.language or contrary.contrary not in self.language:
                raise InvalidBABAException(exception_message)

        for random_variable in self.random_variables:
            if random_variable not in self.language:
                raise InvalidBABAException(exception_message)

    # Checks if underlying ABA network is flat
    def validate_is_flat(self):
        for rule in self.rules:
            if rule.head in self.assumptions:
                raise InvalidBABAException("Framework is not flat")

    # Ensures no random variables as heads of rules
    def validate_random_variables(self):
        for rule in self.rules:
            if rule.head in self.random_variables:
                raise InvalidBABAException("Random variables cannot be in the heads of rules")

#################################################################################

    def compute_derivable_dictionary(self):
        for sentence in self.language:
            self.derivable_dictionary[sentence] = []

        for rule in self.rules:
            if len(rule.body) == 0:
                self.derivable_dictionary[rule.head] = [[]]
                self.derived_claims[rule.head] = True
            else:
                self.derivable_dictionary[rule.head].append(list(rule.body))

    # Returns a list of lists of sentences required to derive the claim
    def compute_required_to_derive(self, claim):
        if claim in self.derived_claims:
            return self.derivable_dictionary[claim]  # Memoisation

        required_to_derive_sets = []
        for required_set in self.derivable_dictionary[claim]:
            required_to_derive_required_set = [[]]
            for required_elem in required_set:
                if required_elem in self.assumptions or required_elem in self.random_variables:
                    required_to_derive_required_set = list_combinations(required_to_derive_required_set, [[required_elem]])

                else:
                    required_to_derive_elem = self.compute_required_to_derive(required_elem)
                    required_to_derive_elem.append([required_elem])  # Can derive an elem if elem is present
                    required_to_derive_required_set = list_combinations(required_to_derive_required_set, required_to_derive_elem)

            for item in required_to_derive_required_set:
                required_to_derive_sets.append(item)

        required_to_derive_sets.append([claim])
        self.derivable_dictionary[claim] = required_to_derive_sets
        self.derived_claims[claim] = True
        return required_to_derive_sets

    def derivable(self, claim, sentences):
        sets_that_derive_claim = self.compute_required_to_derive(claim)
        for deriving_set in sets_that_derive_claim:
            if frozenset(deriving_set).issubset(frozenset(sentences)):
                return True
        return False

    def compute_attacks(self):
        for assumption in self.assumptions:
            attacks = set()
            if assumption in self.contraries:

                contrary = self.contraries[assumption].contrary
                required_to_derive_contrary_lists = self.compute_required_to_derive(contrary)
                for required_list in required_to_derive_contrary_lists:
                    attacks.add(Attack(assumption, set(required_list)))

            self.attacks[assumption] = attacks

    # def compute_counter_attacks(self):
    #     for assumption in self.assumptions:
    #         attacks = self.attacks[assumption]
    #         for attack in attacks:
    #             counter_attacks = set()
    #             for elem in attack.support:
    #                 required_to_derive_support_elem_lists = self.compute_required_to_derive(elem)
    #                 for required_list in required_to_derive_support_elem_lists:
    #                     counter_attacks.add(Attack(elem, set(required_list)))
    #             self.counter_attacks[attack] = counter_attacks

###################################


class Sentence:
    def __init__(self, symbol, random_variable=False, negation=False):
        self.symbol = symbol
        self.random_variable = random_variable
        self.negation = negation

    def __hash__(self):
        return hash(self.symbol) + hash(self.random_variable) + hash(self.negation)

    def __eq__(self, other):
        return self.symbol == other.symbol and self.random_variable == other.random_variable\
           and self.negation == other.negation

    def __str__(self):
        return self.symbol if not self.negation else "~" + self.symbol


class Rule:
    def __init__(self, head, body=[]):
        self.head = head
        self.body = body

    def __hash__(self):
        return hash(self.head) + sum([hash(item) for item in self.body])

    def __eq__(self, other):
        head_equal = self.head == other.head
        body_equal = all([elem in other.body for elem in self.body]) and len(self.body) == len(other.body)
        return head_equal and body_equal

    def __str__(self):
        return str(self.head) + " :- " + ', '.join([str(elem) for elem in self.body])


class Contrary:
    def __init__(self, assumption, contrary):
        if assumption == contrary:
            raise InvalidContraryException(
                "An assumption cannot be a contrary of itself")

        self.assumption = assumption
        self.contrary = contrary

    def __hash__(self):
        return hash(self.assumption) + hash(self.contrary)

    def __eq__(self, other):
        return self.assumption == other.assumption and self.contrary == other.contrary

    def __str__(self):
        return "~" + str(self.assumption) + " = " + str(self.contrary)


# A set of sentences, 'support', derives the contrary of the 'attacked' sentence
class Attack:
    def __init__(self, attacked, support):
        self.attacked = attacked
        self.support = support

    def __hash__(self):
        return hash(self.attacked) + sum([hash(item) for item in self.support])

    def __eq__(self, other):
        return (self.attacked == other.attacked and
                all([s in other.support for s in self.support]) and
                len(self.support) == len(other.support))


# A container class for a list of sentences
class SemanticSet:
    def __init__(self, elements):
        self.elements = frozenset(elements)

    def __hash__(self):
        return sum([hash(item) for item in self.elements])

    def __eq__(self, other):
        return all([elem in other.elements for elem in self.elements]) \
               and len(self.elements) == len(other.elements)

    def __str__(self):
        return "[" + ', '.join([str(elem) for elem in self.elements]) + "]"


class InvalidBABAException(Exception):
    def __init__(self, message):
        self.message = message


class InvalidContraryException(Exception):
    def __init__(self, message):
        self.message = message


class InvalidSemanticsException(Exception):
    def __init__(self, message):
        self.message = message


# Returns whether a claim is derivable in a BABA framework from a set of sentences
def derivable(baba, claim, sentences):
    return baba.derivable(claim, set(sentences).union(set(baba.rv_world)))


# Returns the complete set of sentences derivable from the BABA framework given a set of sentences
def derivable_set(baba, sentences):
    for sentence in baba.language:
        if sentence not in sentences and derivable(baba, sentence, sentences):
            return derivable_set(baba, sentences + [sentence])
    return sentences


# Returns a set of contraries to the given set of sentences in the BABA framework
def contraries(baba, sentences):
    contrary_set = set()
    for sentence in sentences:
        if sentence in baba.contraries:
            contrary_set.add(baba.contraries[sentence].contrary)
    return contrary_set


# Returns a set of all potential Attacks against elements of attacked
def get_attacks(baba, attacked):
    attacks = set()
    for element in attacked:
        if element in baba.attacks:
            attacks_for_element = baba.attacks[element]
            attacks = attacks.union(attacks_for_element)

    return attacks


# Returns whether the given attack holds in the given baba framework and random variable world
def valid_attack(baba, attack):
    return all([(elem in baba.assumptions or elem in baba.rv_world) for elem in attack.support])


# Returns whether the set of assumptions defends the claim -
# where A defends a iff A attacks all sets of assumptions that attack a)
def defends(baba, assumptions, claim):
    attacks = baba.attacks[claim]
    for attack in attacks:

        if not valid_attack(baba, attack):
            continue

        support_contraries = contraries(baba, attack.support)
        if len(attack.support) == 0:  # Attack cannot be countered
            is_counter_attacked = False
        elif len(support_contraries) == 0:  # Attack support has no contrary
            is_counter_attacked = False
        else:
            is_counter_attacked = any([derivable(baba, elem, assumptions) for elem in support_contraries])

        if not is_counter_attacked:
            return False

    return True


# Returns whether the list of assumptions is conflict free
# (Implementation: derivable() is lazily evaluated and memoised.)
def conflict_free(baba, assumptions, attacks=None):
    attacks = attacks if attacks is not None else get_attacks(baba, assumptions)
    for attack in attacks:
        if attack.support.issubset(assumptions):
            return False

    return True


# Returns whether the list of assumptions is admissible in the BABA framework
def is_admissible(baba, assumptions):
    attacks = get_attacks(baba, assumptions)

    for attack in attacks:
        if attack.support.issubset(assumptions):  # Check if conflict free
            return False

        if not valid_attack(baba, attack):
            continue

        support_contraries = contraries(baba, attack.support)
        if not any(derivable(baba, s, assumptions) for s in support_contraries)\
                and len(support_contraries) > 0:
            return False

    return True


# Generates the complete set of admissible sets of assumptions
def admissible(baba):
    ps = powerset(baba.assumptions)
    return set([SemanticSet(elem) for elem in ps if is_admissible(baba, elem)])


############################################################
# The following methods generate all lists of assumptions
# that satisfy the corresponding semantics

def preferred(baba, admissibles=None):
    admissible_sets = admissibles if admissibles is not None else admissible(baba)
    preferred_sets = []

    for ad_set in admissible_sets:
        remaining_sets = admissible_sets - set([ad_set])

        if not any([all([elem in current.elements for elem in ad_set.elements])
                    for current in remaining_sets]):
            preferred_sets.append(ad_set)

    return preferred_sets


def sceptically_preferred(baba, admissibles=None):
    admissible_sets = admissibles if admissibles is not None else admissible(baba)
    preferred_sets = preferred(baba, admissible_sets)
    return set([group_intersection(preferred_sets)])


def complete(baba, admissibles=None):
    admissible_sets = admissibles if admissibles is not None else admissible(baba)
    complete_sets = []

    for ad_set in admissible_sets:
        elements_not_in_set = [elem for elem in baba.assumptions if elem not in ad_set.elements]
        if not any([defends(baba, ad_set.elements, element) for element in elements_not_in_set]):
            complete_sets.append(ad_set)

    return complete_sets


def grounded(baba, admissibles=None):
    admissible_sets = admissibles if admissibles is not None else admissible(baba)
    return set(minimal_set(complete(baba, admissible_sets)))


def ideal(baba, admissibles=None):
    admissible_sets = admissibles if admissibles is not None else admissible(baba)
    preferred_sets = preferred(baba, admissible_sets)
    return [p for p in admissible_sets if
            all([elem in other.elements for elem in p.elements for other in preferred_sets])]


def stable(baba, admissibles=None):
    admissible_sets = admissibles if admissibles is not None else admissible(baba)
    stable_sets = []
    for admissible_set in admissible_sets:
        not_in_set = [elem for elem in baba.assumptions if elem not in admissible_set.elements]
        contraries_to_derive = contraries(baba, not_in_set)

        # Not all assumptions have defined contraries (cannot be attacked)
        if len(contraries_to_derive) != len(not_in_set):
            continue

        if all([derivable(baba, contrary, admissible_set.elements) for contrary in contraries_to_derive]):
            stable_sets.append(admissible_set)

    return stable_sets

############################################################


# Definition of BABA semantics: acceptance probability
# of a set of sentences (w.r.t. to a given semantics)
def semantic_probability(semantics, baba, sentences):
    if not all([s in baba.language for s in sentences]):
        raise InvalidBABAException("Semantic probability enquired for invalid set of sentences")

    worlds = generate_worlds(baba.random_variables)
    acceptability_probability = 0.0

    for world in worlds:
        baba.set_random_variable_world(world)

        if semantics == GROUNDED:
            semantic_sets = grounded(baba)
        elif semantics == SCEPTICALLY_PREFERRED:
            semantic_sets = sceptically_preferred(baba)
        elif semantics == IDEAL:
            semantic_sets = ideal(baba)
        else:
            raise InvalidSemanticsException("Invalid semantics chosen: " + str(semantics))

        can_derive_sentence = False

        for a_set in semantic_sets:
            can_derive_sentence = all([derivable(baba, s, a_set.elements) for s in sentences])

        if can_derive_sentence:
            acceptability_probability += baba.BN.p_world(world)

    return acceptability_probability


# Returns a dictionary of {symbol : semantic probability}
def compute_semantic_probability(semantics, baba):
    language_probability = {}
    for sentence in baba.language:
        language_probability[sentence.symbol] = 0.0

    worlds = generate_worlds(baba.random_variables)
    worlds = [[]] if len(worlds) == 0 else worlds

    for world in worlds:
        baba.set_random_variable_world(world)

        if semantics == GROUNDED:
            semantic_sets = grounded(baba)
        elif semantics == SCEPTICALLY_PREFERRED:
            semantic_sets = sceptically_preferred(baba)
        elif semantics == IDEAL:
            semantic_sets = ideal(baba)
        else:
            raise InvalidSemanticsException("Invalid semantics chosen: " + str(semantics))

        world_probability = baba.BN.p_world(world) if len(world) > 0 else 1.0

        for sentence in baba.language:
            if any(derivable(baba, sentence, a_set.elements) for a_set in semantic_sets):
                language_probability[sentence.symbol] += world_probability

    return language_probability


# Returns semantic probabilities for a BABA framework for given semantics
def compute_semantic_probabilities_for_semantics(baba, semantics):
    probabilities = compute_semantic_probability(semantics, baba)
    tuples = [(sentence, "{0:.3f}".format(probability)) for sentence, probability in probabilities.items()]
    tuples = sorted(tuples, key=lambda item: item[0])

    return tuples


# Returns a tuple of the semantic probabilities for a BABA
# (probabilities given as lists of (sentence, probability) string tuple
def compute_semantic_probabilities(baba):
    grounded_tuples = compute_semantic_probabilities_for_semantics(baba, GROUNDED)
    s_preferred_tuples = compute_semantic_probabilities_for_semantics(baba, SCEPTICALLY_PREFERRED)
    ideal_tuples = compute_semantic_probabilities_for_semantics(baba, IDEAL)

    return grounded_tuples, s_preferred_tuples, ideal_tuples


##############################################################################
# Computes the semantic probability in parallel
def compute_parallel_semantic_probability(semantics, baba):
    output = mp.Queue()

    language_probability = {}
    for sentence in baba.language:
        language_probability[sentence.symbol] = 0.0

    worlds = generate_worlds(baba.random_variables)
    worlds = [[]] if len(worlds) == 0 else worlds

    # Setup processes
    processes = [mp.Process(target=compute_parallel_semantic_probability_for_world,
                            args=(copy.deepcopy(baba), semantics, world, output))
                 for world in worlds]

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

    # Get process results from the output queue
    results = [output.get() for p in processes]

    # Sum marginal probabilities
    for probability_dictionary in results:
        for key, value in probability_dictionary.items():
            language_probability[key] += value

    return language_probability


def compute_parallel_semantic_probability_for_world(baba, semantics, world, output):
    language_probability = {}
    baba.set_random_variable_world(world)

    if semantics == GROUNDED:
        semantic_sets = grounded(baba)
    elif semantics == SCEPTICALLY_PREFERRED:
        semantic_sets = sceptically_preferred(baba)
    elif semantics == IDEAL:
        semantic_sets = ideal(baba)
    else:
        raise InvalidSemanticsException("Invalid semantics chosen: " + str(semantics))

    world_probability = baba.BN.p_world(world)

    for sentence in baba.language:
        if any(derivable(baba, sentence, a_set.elements) for a_set in semantic_sets):
            language_probability[sentence.symbol] = world_probability

    output.put(language_probability)
