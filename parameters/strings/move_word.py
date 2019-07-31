import random

qvars = None


def init(variables):
    global qvars
    qvars = variables
    random.seed(qvars.get("seed"))
    qvars["move_word.idx"] = random.randint(2, 42)
    qvars["move_word.dest"] = "front" if random.randint(0, 1) == 0 else "end"


def execute():
    args = qvars.get("args")
    idx = qvars.get("move_word.idx")
    dest = qvars.get("move_word.dest")

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
        if dest == "front":
            res = trimmed[idx:idx + 1] + trimmed[0:idx] + trimmed[idx + 1:]
        else:
            res = trimmed[0:idx] + trimmed[idx + 1:] + trimmed[idx:idx + 1]

        args[i] = ' '.join(res)


def get_subject():
    return """
Outputs given strings with word #%move_word.idx% moved to the %move_word.dest% of the string, with each word separated by exactly one space.
If the string contains fewer words than %move_word.idx%, the program continues counting from the front of the string.
A word is a sequence of characters delimited by spaces/tabs.
"""


def get_examples():
    return [
        "abc   ",
        "Que la  \tlumiere soit et la lumiere fut",
        "\t AkjhZ zLKIJz , 23y",
        ["first", "2", "11000000"],
    ]
