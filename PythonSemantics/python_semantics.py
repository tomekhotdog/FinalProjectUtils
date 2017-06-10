import PythonSemantics.Parsing.BABAProgramParser as Parser
import PythonSemantics.Semantics as Semantics


def create_framework(framework_string):
    return Parser.BABAProgramParser(string=framework_string).parse()


def compute_semantics(framework_string):
    framework = create_framework(framework_string)

    admissible = Semantics.admissible(framework)
    stable_ext = Semantics.stable(framework, admissibles=admissible)
    grounded_ext = Semantics.grounded(framework, admissibles=admissible)
    complete_ext = Semantics.complete(framework, admissibles=admissible)
    preferred_ext = Semantics.preferred(framework, admissibles=admissible)
    ideal_ext = Semantics.stable(framework, admissibles=admissible)

    return stable_ext, grounded_ext, complete_ext, preferred_ext, ideal_ext


def compute_admissible(framework_string):
    framework = create_framework(framework_string)
    return Semantics.admissible(framework)


def compute_stable(framework_string, admissibles=None):
    framework = create_framework(framework_string)
    return Semantics.stable(framework, admissibles=admissibles)


def compute_grounded(framework_string, admissibles=None):
    framework = create_framework(framework_string)
    return Semantics.grounded(framework, admissibles=admissibles)


def compute_complete(framework_string, admissibles=None):
    framework = create_framework(framework_string)
    return Semantics.complete(framework, admissibles=admissibles)


def compute_preferred(framework_string, admissibles=None):
    framework = create_framework(framework_string)
    return Semantics.preferred(framework, admissibles=admissibles)


def compute_ideal(framework_string, admissibles=None):
    framework = create_framework(framework_string)
    return Semantics.ideal(framework, admissibles=admissibles)