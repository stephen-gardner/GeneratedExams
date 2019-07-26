import random

qvars = None


def init(variables):
    global qvars
    qvars = variables
    random.seed(qvars.get("seed"))
    qvars["capitalizer.type"] = random.randint(0, 5)


def execute():
    args = qvars.get("args")
    cap_type = qvars.get("capitalizer.type")

    for ac, arg in enumerate(args):
        res = []
        words = arg.replace('\t', ' ').split(' ')
        for w in words:
            if cap_type == 0:
                if len(w) > 1:
                    w = w[0].upper() + w[1:len(w)].lower()
                else:
                    w = w.upper()
            elif cap_type == 1:
                if len(w) > 1:
                    w = w[:len(w) - 1].lower() + w[len(w) - 1].upper()
                else:
                    w = w.lower()
            elif cap_type == 2:
                w = w.upper()
            elif cap_type == 3:
                w = w.lower()
            else:
                capitalized = ""
                cap = cap_type == 4
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
    if cap_type <= 1:
        return """
Outputs given strings with the {} character of each word in uppercase, and the
rest in lowercase, followed by a newline.
""".format("first" if cap_type == 0 else "last")
    elif cap_type <= 3:
        return """
Outputs given strings in all {}, followed by a newline.
""".format("uppercase" if cap_type == 2 else "lowercase")
    else:
        return """
Output given strings with alternating uppercase and lowercase characters,
starting in {}, followed by a newline.
""".format("uppercase" if cap_type == 4 else "lowercase")


def get_examples():
    return [
        "a FiRSt LiTTlE TESt",
        [
            "SecONd teST A LITtle BiT   Moar comPLEX",
            "\tBut... This iS not THAT COMPLEX",
            "   Okay, this is the last 1239809147801 but not\tthe least\tt",
        ],
    ]
