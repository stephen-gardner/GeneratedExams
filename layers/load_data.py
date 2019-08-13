from enum import Flag, auto
import random


class LoadType(Flag):
    LINE = auto()


qvars = None


def init(variables):
    global qvars
    qvars = variables
    random.seed(qvars.get("seed"))
    if "load_data.type" not in qvars:
        qvars["load_data.type"] = LoadType.LINE


def execute(argv):
    load_type = qvars.get("load_data.type")

    output = []
    for arg in argv:
        input_file = open(arg, "r")
        if load_type == LoadType.LINE:
            output.append(input_file.readlines())
        input_file.close()
    return output


def get_substitutions():
    return []


def get_subject():
    return ""


def get_examples():
    return None
