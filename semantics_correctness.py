import time

import AspartixSemantics.aspartix_semantics as aspartix_semantics
import PythonSemantics.python_semantics as python_semantics
from PythonSemantics.Semantics import Sentence, SemanticSet


def compare_frameworks(framework_string):
    aspartix_aba =  aspartix_semantics.compute_semantics(framework_string)
    python_aba = python_semantics.create_framework(framework_string)

    return 0


def compare_semantics(framework_name, framework_string):
    a_stable, a_grounded, a_complete, a_preferred, a_ideal = aspartix_semantics.compute_semantics(framework_string)
    p_stable, p_grounded, p_complete, p_preferred, p_ideal = python_semantics.compute_semantics(framework_string)

    compare_extensions(framework_name, 'stable', a_stable, p_stable)
    compare_extensions(framework_name, 'grounded', a_grounded, p_grounded)
    compare_extensions(framework_name, 'complete', a_complete, p_complete)
    compare_extensions(framework_name, 'preferred', a_preferred, p_preferred)
    # compare_extensions(framework_name, 'ideal', a_ideal, p_ideal)


def compare_execution_times(framework_name, framework_string):
    asp_stable_time = time_function_execution(lambda: aspartix_semantics.compute_stable(framework_string))
    py_stable_time = time_function_execution(lambda: python_semantics.compute_stable(framework_string))

    with open('semantics_time_test.txt', 'a') as file:
        file.write(framework_name + ': \n')
        file.write('Stable. Aspartix: ' + str(asp_stable_time) + '. Python: ' + str(py_stable_time) + '\n')


def compare_stable(framework_name, framework_string):
    a_stable = aspartix_semantics.compute_stable(framework_string)
    p_stable = python_semantics.compute_stable(framework_string)

    compare_extensions(framework_name, 'stable', a_stable, p_stable)


def compare_extensions(framework_name, semantics_name, aspartix_exts, python_exts):
    aspartix_semantic_sets = []
    for ext in aspartix_exts:
        elements = [Sentence(s.symbol, negation=False, random_variable=False) for s in ext]
        aspartix_semantic_sets.append(SemanticSet(elements))

    equal = all(a_set in python_exts for a_set in aspartix_semantic_sets) and \
        len(aspartix_semantic_sets) == len(python_exts)

    if not equal:
        with open('semantics_correctness_test.txt', 'a') as file:
            aspartix_ext_string = ' '.join([str(ext) for ext in aspartix_semantic_sets])
            python_ext_string = ' '.join([str(ext) for ext in python_exts])
            file.write('extension difference observed: ' + framework_name + ', ' + semantics_name + ', aspartix_exts: ' +
                       aspartix_ext_string + '. python exts: ' + python_ext_string + '\n')


def time_function_execution(function_to_call):
    start_time = time.process_time()
    function_to_call()
    end_time = time.process_time()

    return end_time - start_time

framework_1 = "myAsm(a).\n myAsm(b).\n myAsm(c).\n myAsm(d).\n contrary(a, _a).\n contrary(b, _b).\n" \
              "contrary(c, _c).\n contrary(d, _d).\n myRule(_a, [b]).\n myRule(_b, [c]).\n" \
              "myRule(_c, [d]).\n myRule(_d, [c])."

framework_2 = "myAsm(a).\n myAsm(b).\n myAsm(c).\n myAsm(d).\n myAsm(e).\n myAsm(f).\n contrary(a, _a).\n " \
              "contrary(b, _b).\n contrary(c, _c).\n contrary(d, _d).\n contrary(e, _e).\n contrary(f, _f).\n" \
              "myRule(_a, [b]).\n myRule(_b, [c]).\n myRule(_c, [d]).\n myRule(_d, [c]).\n myRule(_d, [e]).\n" \
              "myRule(_e, [d]).\n myRule(_e, [f]).\n myRule(_f, [e])."


# compare_semantics('Framework_1', framework_1)
# compare_semantics('Framework_2', framework_2)

compare_execution_times('Framework_1', framework_2)
compare_execution_times('Framework_2', framework_2)
