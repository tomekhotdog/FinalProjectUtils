

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
        if sentence not in self.values:
            raise InvalidRandomVariableException(str(sentence) + " is not random variable in this Bayesian Network")

        return self.values[sentence]


class InvalidRandomVariableException(Exception):
    def __init__(self, message):
        self.message = message

