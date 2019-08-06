from enum import Enum
import random


class Capital(Enum):
    UPPER_FIRST = 0
    UPPER_LAST = 1
    UPPER_ALL = 2
    LOWER_ALL = 3
    ALTERNATE_FIRST = 4
    ALTERNATE_LAST = 5


qvars = None


def init(variables):
    global qvars
    qvars = variables
    random.seed(qvars.get("seed"))
    qvars["capitalizer.type"] = Capital(random.randint(0, 5))


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


def get_subject():
    cap_type = qvars.get("capitalizer.type")

    if cap_type == Capital.UPPER_FIRST or cap_type == Capital.UPPER_LAST:
        return """
Outputs given strings with the {} character of each word in uppercase, and the rest in lowercase.
A word is a sequence of characters delimited by spaces/tabs.
""".format("first" if cap_type == Capital.UPPER_FIRST else "last")
    elif cap_type == Capital.UPPER_ALL or cap_type == Capital.LOWER_ALL:
        return """
Outputs given strings in all {} characters.
""".format("uppercase" if cap_type == Capital.UPPER_ALL else "lowercase")
    else:
        return """
Output given strings with alternating uppercase and lowercase characters for each word, starting in {}.
A word is a sequence of characters delimited by spaces/tabs.
""".format("uppercase" if cap_type == Capital.ALTERNATE_FIRST else "lowercase")


def get_examples():
    return [
        "a FiRSt LiTTlE TESt",
        [
            "SecONd teST A LITtle BiT   Moar comPLEX",
            "\tBut... This iS not THAT COMPLEX",
            "   Okay, this is the last 1239809147801 but not\tthe least\tt",
        ],
    ]
