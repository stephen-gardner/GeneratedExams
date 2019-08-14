from enum import Flag, auto
import inflect
import random


class RotType(Flag):
    ALPHA_ONLY = auto()
    NUMBERS_ONLY = auto()
    BOTH = auto()


p = inflect.engine()
qvars = None


def init(variables):
    global qvars
    qvars = variables
    random.seed(qvars.get("seed"))
    qvars["rot.type"] = RotType(1 << random.randint(0, 2))
    qvars["rot.alpha.n"] = random.randint(1, 25)
    qvars["rot.numbers.n"] = random.randint(1, 9)


def shift_chars(arg, alpha_n=0, num_n=0):
    rot_type = qvars.get("rot.type")

    res = ""
    for c in arg:
        if rot_type & (RotType.ALPHA_ONLY | RotType.BOTH) and c.isalpha():
            if c.islower():
                c = chr((((ord(c) - ord('a')) + alpha_n) % 26) + ord('a'))
            else:
                c = chr((((ord(c) - ord('A')) + alpha_n) % 26) + ord('A'))
        if rot_type & (RotType.NUMBERS_ONLY | RotType.BOTH) and c.isnumeric():
            c = chr((((ord(c) - ord('0')) + num_n) % 10) + ord('0'))
        res += c
    return res


def execute(argv):
    alpha_n = qvars.get("rot.alpha.n")
    num_n = qvars.get("rot.numbers.n")

    output = []
    for arg in argv:
        output.append(shift_chars(arg, alpha_n, num_n))
    return output


def get_substitutions():
    num_args = qvars.get("num_args.n")
    alpha_n = qvars.get("rot.alpha.n")
    num_n = qvars.get("rot.numbers.n")

    return [
        ("string", p.plural_noun("string", num_args)),
        ("alpha_n", str(alpha_n)),
        ("num_n", str(num_n)),
        ("z", shift_chars("z", alpha_n, num_n)),
        ("Z", shift_chars("Z", alpha_n, num_n)),
        ("9", shift_chars("9", alpha_n, num_n)),
        ("42", shift_chars("42", alpha_n, num_n))
    ]


def get_old_subject():
    rot_type = qvars.get("rot.type")

    if rot_type & RotType.ALPHA_ONLY:
        return """
Outputs given strings with each of its letters replaced by the letter %alpha_n% spaces ahead in alphabetical order.
'z' becomes '%z%' and 'Z' becomes '%Z%'.
"""
    elif rot_type & RotType.NUMBERS_ONLY:
        return """
Outputs given strings with each of its numerical digits replaced by the digit %num_n% characters ahead.
'9' becomes '%9%' and '42' becomes '%42%'.
"""
    else:
        return """
Outputs given strings with each of its letters replaced by the letter %alpha_n% spaces ahead in alphabetical order.
'z' becomes '%z%' and 'Z' becomes '%Z%'.
        
Outputs given strings with each of its numerical digits replaced by the digit %num_n% characters ahead.
'9' becomes '%9%' and '42' becomes '%42%'.
        """


def get_subject():
    rot_type = qvars.get("rot.type")

    subject = """
Outputs given %string% with {}{}{}. {}{}
"""
    alpha = "each letter replaced by the letter %alpha_n% characters ahead in alphabetical order"
    alpha_ex = "\n'z' becomes '%z%' and 'Z' becomes '%Z%'."
    num = "each numerical digit replaced by the digit %num_n% characters ahead"
    num_ex = "\n'9' becomes '%9%' and '42' becomes '%42%'."

    if rot_type & RotType.ALPHA_ONLY:
        return subject.format(alpha, "", "", alpha_ex, "")
    elif rot_type & RotType.NUMBERS_ONLY:
        return subject.format(num, "", "", num_ex, "")
    else:
        return subject.format(alpha, ", and ", num, alpha_ex, num_ex)


def get_examples():
    return [
        "abc",
        "My horse is Amazing.",
        "AkjhZ zLKIJz , 23y ",
        shift_chars("42 This is a hidden message 42", -qvars.get("rot.alpha.n"), -qvars.get("rot.numbers.n")),
    ]
