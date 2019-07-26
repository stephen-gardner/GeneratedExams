from enum import Enum
import random


class Type(Enum):
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
    qvars["capitalizer.type"] = Type(random.randint(0, 5))


def execute():
    args = qvars.get("args")
    cap_type = qvars.get("capitalizer.type")

    for ac, arg in enumerate(args):
        res = []
        words = arg.replace('\t', ' ').split(' ')
        for w in words:
            if cap_type == Type.UPPER_FIRST:
                w = w[0].upper() + w[1:len(w)].lower() if len(w) > 1 else w.upper()
            elif cap_type == Type.UPPER_LAST:
                w = w[:len(w) - 1].lower() + w[len(w) - 1].upper() if len(w) > 1 else w.lower()
            elif cap_type == Type.UPPER_ALL:
                w = w.upper()
            elif cap_type == Type.LOWER_ALL:
                w = w.lower()
            else:
                capitalized = ""
                cap = cap_type == Type.ALTERNATE_FIRST
                for l in w:
                    if cap:
                        capitalized += l.upper()
                        cap = False
                    else:
                        capitalized += l.lower()
                        cap = True
                w = capitalized

            res.append(w)
        args[ac] = " ".join(res)


def get_subject():
    cap_type = qvars.get("capitalizer.type")

    if cap_type == Type.UPPER_FIRST or cap_type == Type.UPPER_LAST:
        return """
Outputs given strings with the {} character of each word in uppercase, and the
rest in lowercase, followed by a newline.
""".format("first" if cap_type == Type.UPPER_FIRST else "last")
    elif cap_type == Type.UPPER_ALL or cap_type == Type.LOWER_ALL:
        return """
Outputs given strings in all {}, followed by a newline.
""".format("uppercase" if cap_type == Type.UPPER_ALL else "lowercase")
    else:
        return """
Output given strings with alternating uppercase and lowercase characters,
starting in {}, followed by a newline.
""".format("uppercase" if cap_type == Type.ALTERNATE_FIRST else "lowercase")


def get_examples():
    return [
        "a FiRSt LiTTlE TESt",
        [
            "SecONd teST A LITtle BiT   Moar comPLEX",
            "\tBut... This iS not THAT COMPLEX",
            "   Okay, this is the last 1239809147801 but not\tthe least\tt",
        ],
    ]
