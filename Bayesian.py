import functools as tools


# A representation of the Bayesian Network governing
# the set of a random variables in a BABA network
class BayesianNetwork:

    def __init__(self, values):
        self.values = values  # dictionary: Semantic.Sentence.symbol : value
        self.validate()

    def validate(self):
        for _, value in self.values.items():
            if value < 0 or value > 1:
                raise InvalidRandomVariableException("Random Variable value must be within bound [0 <= value <= 1]")

    def p(self, sentence):
        if sentence.symbol not in self.values:
            raise InvalidRandomVariableException(str(sentence) + " is not random variable in this Bayesian network")

        rv_probability = self.values[sentence.symbol]
        return rv_probability if not sentence.negation else (1 - rv_probability)

    def p_world(self, random_variables):
        if not all([rv.symbol in self.values for rv in random_variables]):
            raise InvalidRandomVariableWorldException("This is not a valid world in this Bayesian network")

        return tools.reduce(lambda x, y: x*y, [self.p(sentence) for sentence in random_variables])


class InvalidRandomVariableException(Exception):
    def __init__(self, message):
        self.message = message


class InvalidRandomVariableWorldException(Exception):
    def __init(self, message):
        self.message = message
