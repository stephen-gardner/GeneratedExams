import random

qvars = None


def init(variables):
    global qvars
    qvars = variables
    random.seed(qvars.get("seed"))
    qvars["rot.n"] = random.randint(1, 25)


def shift_chars(arg, n):
    res = ""
    for c in arg:
        if c.isalpha():
            if c.islower():
                c = chr((((ord(c) - ord('a')) + n) % 26) + ord('a'))
            else:
                c = chr((((ord(c) - ord('A')) + n) % 26) + ord('A'))
        res += c
    return res


def execute(argv):
    n = qvars.get("rot.n")

    output = []
    for arg in argv:
        output.append(shift_chars(arg, n))
    return output


def get_subject():
    n = qvars.get("rot.n")

    return """
Outputs given strings with each of its letters replaced by the letter %rot.n% spaces ahead in alphabetical order.
'{}' becomes '{}' and '{}' becomes '{}'.
""".format("z", shift_chars("z", n), "Z", shift_chars("Z", n))


def get_examples():
    return [
        "abc",
        "My horse is Amazing.",
        "AkjhZ zLKIJz , 23y ",
        shift_chars("This is a hidden message", -qvars.get("rot.n")),
    ]
