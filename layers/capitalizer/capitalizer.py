from enum import Flag, auto
import inflect
import random


class CapitalType(Flag):
    UPPER_FIRST = auto()
    UPPER_LAST = auto()
    UPPER_ALL = auto()
    LOWER_ALL = auto()
    ALTERNATE_FIRST = auto()
    ALTERNATE_LAST = auto()


p = inflect.engine()
qvars = None


def init(variables):
    global qvars
    qvars = variables
    random.seed(qvars.get("seed"))
    qvars["capitalizer.type"] = CapitalType(1 << random.randint(0, 5))


def execute(argv):
    cap_type = qvars.get("capitalizer.type")

    output = []
    for arg in argv:
        if cap_type == CapitalType.UPPER_ALL:
            output.append(arg.upper())
        elif cap_type == CapitalType.LOWER_ALL:
            output.append(arg.lower())
        else:
            res = ""
            if cap_type == CapitalType.UPPER_FIRST:
                cap = True
                for c in arg:
                    res += c.upper() if cap else c.lower()
                    cap = not c.isalnum()
            elif cap_type == CapitalType.UPPER_LAST:
                for i, c in enumerate(arg):
                    res += c.upper() if i + 1 == len(arg) or not arg[i + 1].isalpha() else c.lower()
            else:
                cap = cap_type == CapitalType.ALTERNATE_FIRST
                for c in arg:
                    res += c.upper() if cap else c.lower()
                    cap = not cap if c.isalnum() else cap_type == CapitalType.ALTERNATE_FIRST
            output.append(res)
    return output


def get_substitutions():
    num_args = qvars.get("num_args.n")
    cap_type = qvars.get("capitalizer.type")

    if cap_type & (CapitalType.UPPER_FIRST | CapitalType.UPPER_LAST):
        case = "first" if cap_type == CapitalType.UPPER_FIRST else "last"
    elif cap_type & (CapitalType.UPPER_ALL | CapitalType.ALTERNATE_FIRST):
        case = "uppercase"
    else:
        case = "lowercase"

    return [
        ("string", p.plural_noun("string", num_args)),
        ("case", case),
    ]


def get_old_subject():
    cap_type = qvars.get("capitalizer.type")

    if cap_type == CapitalType.UPPER_FIRST or cap_type == CapitalType.UPPER_LAST:
        return """
Outputs given strings with the {} character of each word in uppercase, and the rest in lowercase.
A word is a sequence of characters delimited by spaces/tabs.
""".format("first" if cap_type == CapitalType.UPPER_FIRST else "last")
    elif cap_type == CapitalType.UPPER_ALL or cap_type == CapitalType.LOWER_ALL:
        return """
Outputs given strings in all {} characters.
""".format("uppercase" if cap_type == CapitalType.UPPER_ALL else "lowercase")
    else:
        return """
Output given strings with alternating uppercase and lowercase characters for each word, starting in {}.
A word is a sequence of characters delimited by spaces/tabs.
""".format("uppercase" if cap_type == CapitalType.ALTERNATE_FIRST else "lowercase")


def get_subject():
    cap_type = qvars.get("capitalizer.type")

    if cap_type & (CapitalType.UPPER_FIRST | CapitalType.UPPER_LAST):
        return """
Outputs given %string% with the %case% character of each word in uppercase, and the rest in lowercase.
A word is a sequence of characters delimited by spaces/tabs.
"""
    elif cap_type & (CapitalType.UPPER_ALL | CapitalType.LOWER_ALL):
        return """
Outputs given %string% in all %case% characters.
"""
    else:
        return """
Outputs given %string% with alternating uppercase and lowercase characters for each word, starting in %case%.
A word is a sequence of characters delimited by spaces/tabs.
"""


def get_examples():
    return [
        "a FiRSt LiTTlE TESt",
        [
            "SecONd teST A LITtle BiT   Moar comPLEX",
            "\tBut... This iS not THAT COMPLEX",
            "   Okay, this is the last 1239809147801 but not\tthe least\tt",
        ],
    ]
