import random

qvars = None


def init(variables):
    global qvars
    qvars = variables
    random.seed(qvars.get("seed"))
    qvars["move_word.idx"] = random.randint(2, 42)


def execute():
    args = qvars.get("args")
    idx = qvars.get("move_word.idx")

    if len(args) > 1:
        qvars["args"] = [""]
        return

    for i, arg in enumerate(args):
        words = arg.replace('\t', ' ').split(' ')
        trimmed = []
        for w in words:
            if w != "":
                trimmed.append(w.strip())

        if len(trimmed) == 0:
            args[i] = ""
            continue

        idx = (idx - 1) % len(trimmed)
        res = trimmed[idx:idx + 1] + trimmed[0:idx] + trimmed[idx + 1:]

        args[i] = " ".join(res)


def get_subject():
    idx = qvars.get("move_word.idx")

    return """
Outputs given string with word #{} moved to the front of the string, with each
word separated by exactly one space.

If the string contains fewer words than {}, the program continues counting from
the front of the string.

If the number of args is not 1, outputs a '\\n'
""".format(idx, idx)


def get_examples():
    return [
        "abc   ",
        "Que la  \tlumiere soit et la lumiere fut",
        "\t AkjhZ zLKIJz , 23y",
        ["first", "2", "11000000"],
    ]
