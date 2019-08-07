from enum import Flag, auto
import random


class Capital(Flag):
    UPPER_FIRST = auto()
    UPPER_LAST = auto()
    UPPER_ALL = auto()
    LOWER_ALL = auto()
    ALTERNATE_FIRST = auto()
    ALTERNATE_LAST = auto()


qvars = None


def init(variables):
    global qvars
    qvars = variables
    random.seed(qvars.get("seed"))
    qvars["capitalizer.type"] = Capital(1 << random.randint(0, 5))


def execute(argv):
    cap_type = qvars.get("capitalizer.type")

    output = []
    for arg in argv:
        if cap_type == Capital.UPPER_ALL:
            output.append(arg.upper())
        elif cap_type == Capital.LOWER_ALL:
            output.append(arg.lower())
        else:
            res = ""
            if cap_type == Capital.UPPER_FIRST:
                cap = True
                for c in arg:
                    res += c.upper() if cap else c.lower()
                    cap = not c.isalnum()
            elif cap_type == Capital.UPPER_LAST:
                for i, c in enumerate(arg):
                    res += c.upper() if i + 1 == len(arg) or not arg[i + 1].isalpha() else c.lower()
            else:
                cap = cap_type == Capital.ALTERNATE_FIRST
                for c in arg:
                    res += c.upper() if cap else c.lower()
                    cap = not cap if c.isalnum() else cap_type == Capital.ALTERNATE_FIRST
            output.append(res)
    return output


def get_substitutions():
    cap_type = qvars.get("capitalizer.type")

    if cap_type & (Capital.UPPER_FIRST | Capital.UPPER_LAST):
        case = "first" if cap_type == Capital.UPPER_FIRST else "last"
    elif cap_type & (Capital.UPPER_ALL | Capital.ALTERNATE_FIRST):
        case = "uppercase"
    else:
        case = "lowercase"

    return [
        ("case", case),
    ]


def get_subject():
    cap_type = qvars.get("capitalizer.type")

    if cap_type & (Capital.UPPER_FIRST | Capital.UPPER_LAST):
        return """
Outputs given strings with the %case% character of each word in uppercase, and the rest in lowercase.
A word is a sequence of characters delimited by spaces/tabs.
"""
    elif cap_type & (Capital.UPPER_ALL | Capital.LOWER_ALL):
        return """
Outputs given strings in all %case% characters.
"""
    else:
        return """
Output given strings with alternating uppercase and lowercase characters for each word, starting in %case%.
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
