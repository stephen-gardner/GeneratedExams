import random
import string

from question import gen_question


def generate_tests(seed):
    random.seed(seed)
    question = gen_question(seed)
    num_args = question.qvars.get("num_args.n")
    if num_args is None:
        num_args = 5

    tests = []
    for _ in range(100):
        args = []
        nargs = random.randint(0, num_args + 1)
        for _ in range(nargs):
            words = []
            nwords = random.randint(0, 9)
            for _ in range(nwords):
                length = random.randint(3, 17)
                words.append("".join(random.sample(string.ascii_letters + string.digits, length)))
            args.append(" ".join(words))
        tests.append(tuple(args))
    return tuple(tests)


def validate_output(seed, tests):
    output_file = open("output.txt", "r")
    output = output_file.read()
    output_file.close()
    print(output)

    q = gen_question(seed)

    correct = []
    for test in tests:
        correct.append('\n'.join(q.execute(test)))
    if output == '\n'.join(correct):
        print("\nResult: OK")
    else:
        print("\nResult: KO")


def test_tests(seed):
    tests = generate_tests(seed)
    q = gen_question(seed)

    print("Input:\n------")
    output = []
    for test in tests:
        print('"%s"' % '" "'.join(test))
        output.append('\n'.join(q.execute(test)))

    print("\nOutput:\n-------")
    output = '\n'.join(output)
    output_file = open("output.txt", "w")
    output_file.write(output)
    output_file.close()

    validate_output(seed, tests)


test_tests(1565433327)
