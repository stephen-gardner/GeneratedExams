from enum import Enum
import random


class Compare(Enum):
    EQUAL = 1
    NOT_EQUAL = 2
    GREATER = 3
    GREATER_EQUAL = 4
    LESSER = 5
    LESSER_EQUAL = 6


qvars = None


def init(variables):
    global qvars
    qvars = variables
    random.seed(qvars.get("seed"))
    if "num_args.n" not in qvars:
        qvars["num_args.n"] = 1
    if "num_args.type" not in qvars:
        qvars["num_args.type"] = Compare.NOT_EQUAL


def execute():
    args = qvars.get("args")
    n = qvars.get("num_args.n")
    condition = qvars.get("num_args.type")

    ac = len(args)
    if (condition == Compare.EQUAL and ac == n) \
            or (condition == Compare.NOT_EQUAL and ac != n) \
            or (condition == Compare.GREATER and ac > n) \
            or (condition == Compare.GREATER_EQUAL and ac >= n) \
            or (condition == Compare.LESSER and ac < n) \
            or (condition == Compare.LESSER_EQUAL and ac <= n):
        qvars["args"] = [""]


def get_subject():
    n = qvars.get("num_args.n")
    condition = qvars.get("num_args.type")

    type_str = ""
    if condition == Compare.EQUAL:
        type_str = "is "
    elif condition == Compare.NOT_EQUAL:
        type_str = "is not"
    elif condition == Compare.GREATER:
        type_str = "is greater than"
    elif condition == Compare.GREATER_EQUAL:
        type_str = "is greater or equal to"
    elif condition == Compare.LESSER:
        type_str = "is lesser than"
    elif condition == Compare.LESSER_EQUAL:
        type_str = "is lesser or equal to"

    return """
If the number of args {} {}, return '\\n'
""".format(type_str, n)


def get_examples():
    return []
