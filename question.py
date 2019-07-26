import importlib
import random
from datetime import datetime


def init():
    seed = datetime.utcnow().timestamp()
    random.seed(seed)
    qvars["seed"] = seed

    params = qvars["params"]

    for p in params:
        p.init(qvars)


def execute():
    params = qvars["params"]

    for p in params:
        p.execute()


def format_example(arg, ex, cat):
    res = "$>./{} \"{}\""

    if cat:
        res += " | cat -e"

    res += "\n{}"

    if cat:
        res += "$"

    return res.format(qvars["prog_name"], arg, ex)


def build_examples():
    params = qvars.get("params")

    examples = [""]
    for p in params:
        examples += p.get_examples()

    res = []
    cat = True
    for e in examples:
        qvars["args"] = [e] if isinstance(e, str) else e
        execute()
        if not isinstance(e, str):
            e = "\" \"".join(e)
        res.append(format_example(e, "\n".join(qvars.get("args")), cat))
        cat = random.randint(1, 100) > 90

    qvars["examples"] = "\nExamples:\n\n" + "\n".join(res)


def build_subject():
    params = qvars["params"]

    subject = """
A word is a sequence of characters delimited by spaces/tabs.
"""

    for p in params:
        subject += p.get_subject()

    qvars["subject"] = subject


qvars = {"prog_name": "test_question",
         "params":
             [
                 importlib.import_module("move_word"),
                 importlib.import_module("capitalizer"),
             ],
         }

init()
build_subject()
build_examples()
print(qvars.get("subject"))
print(qvars.get("examples"))
