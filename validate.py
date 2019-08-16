import random
import string
from itertools import zip_longest

from question import gen_question

ALPHANUM = string.ascii_letters + string.digits
MIN_ARG_LENGTH = 1
MAX_ARG_LENGTH = 25
NUM_TESTS = 175


def random_arg(charset, min_arglen, max_arglen):
    n = random.randint(min_arglen, max_arglen)
    return ''.join(random.sample(charset, n))


def random_argv(charset, min_arglen, max_arglen, size):
    args = []
    for _ in range(size):
        rarg = random_arg(charset, min_arglen, max_arglen)
        args.append('\t' + rarg if random.randint(0, size) == size else rarg)
    return ' '.join(args)


def generate_tests(seed):
    random.seed(seed)
    q = gen_question(seed)
    max_args = q.qvars.get("num_args.n")
    if max_args is None:
        max_args = 5

    tests = []
    for _ in range(NUM_TESTS):
        nargs = random.randint(0, max_args + 1)
        tests.append(random_argv(ALPHANUM, MIN_ARG_LENGTH, MAX_ARG_LENGTH, nargs))
    return tuple(tests)


def validate_output(seed, tests, output):
    q = gen_question(seed)

    correct = 0
    total = 0
    for out, test in zip_longest(output, tests):
        if test is None:
            correct -= 1
            continue
        if out is not None:
            answer = '\n'.join(q.execute(test))
            if out == answer:
                correct += 1
        total += 1

    if correct < 0:
        correct = 0
    return "%.2f" % ((correct / total) * 100)

# def test_tests(seed):
#     tests = generate_tests(seed)
#     q = gen_question(seed)
#
#     print("Input:\n------\n", '\n'.join(tests))
#     # output_file = open("output.txt", "w")
#     # for test in tests:
#     #     output_file.write('\n'.join(q.execute(test)) + '\n')
#     # output_file.close()
#
#     print("\nOutput:\n-------")
#     output_file = open("output.txt", "r")
#     output = output_file.read().splitlines()
#     output_file.close()
#     print('\n'.join(output))
#     validate_output(seed, tests, output)
#
#
# from datetime import datetime
#
# test_tests(1337)
