from enum import Enum
import random


class Compare(Enum):
    EQUAL = "is equal to"
    NOT_EQUAL = "is not equal to"
    GREATER = "is greater than"
    GREATER_EQUAL = "is greater or equal to"
    LESSER = "is lesser than"
    LESSER_EQUAL = "is lesser or equal to"


qvars = None


def init(variables):
    global qvars
    qvars = variables
    random.seed(qvars.get("seed"))
    if "num_args.n" not in qvars:
        qvars["num_args.n"] = 1
    if "num_args.type" not in qvars:
        qvars["num_args.type"] = Compare.NOT_EQUAL


def execute(argv):
    n = qvars.get("num_args.n")
    condition = qvars.get("num_args.type")

    ac = len(argv)
    if (condition == Compare.EQUAL and ac == n) \
            or (condition == Compare.NOT_EQUAL and ac != n) \
            or (condition == Compare.GREATER and ac > n) \
            or (condition == Compare.GREATER_EQUAL and ac >= n) \
            or (condition == Compare.LESSER and ac < n) \
            or (condition == Compare.LESSER_EQUAL and ac <= n):
        return [""]
    return argv


def get_substitutions():
    n = qvars.get("num_args.n")
    compare_type = qvars.get("num_args.type")

    return [
        ("compare_type", compare_type.value),
        ("n", str(n)),
    ]


def get_subject():
    return """
If the number of args %compare_type% %n%, return '\\n'
"""


def get_examples():
    return []
