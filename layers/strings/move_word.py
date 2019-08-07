import random

import util

qvars = None


def init(variables):
    global qvars
    qvars = variables
    random.seed(qvars.get("seed"))
    qvars["move_word.idx"] = random.randint(2, 42)
    qvars["move_word.dst"] = random.randint(0, 1)


def execute(argv):
    idx = qvars.get("move_word.idx")
    dest = qvars.get("move_word.dst")

    output = []
    for arg in argv:
        words = arg.replace('\t', ' ').split(' ')
        trimmed = []
        for w in words:
            if w != "":
                trimmed.append(w.strip())

        if len(trimmed) == 0:
            output.append("")
            continue

        idx = (idx - 1) % len(trimmed)
        if dest == 0:
            res = trimmed[idx:idx + 1] + trimmed[0:idx] + trimmed[idx + 1:]
        else:
            res = trimmed[0:idx] + trimmed[idx + 1:] + trimmed[idx:idx + 1]

        output.append(' '.join(res))
    return output


def get_substitutions():
    idx = qvars.get("move_word.idx")
    dst = qvars.get("move_word.dst")

    return [
        ("nth", util.ordinal(idx)),
        ("dst", "front" if dst == 0 else "end"),
        ("num_words", "%d %s" % (idx, "words" if idx > 1 else "word")),
    ]


def get_subject():
    return """
Outputs given strings with the %nth% word moved to the %dst% of the string, with each word separated by exactly one space.
If the string contains fewer than %num_words%, the program continues counting from the beginning of the string.
A word is a sequence of characters delimited by spaces/tabs.
"""


def get_examples():
    return [
        "abc   ",
        "Que la  \tlumiere soit et la lumiere fut",
        "\t AkjhZ zLKIJz , 23y",
        ["first", "2", "11000000"],
    ]
