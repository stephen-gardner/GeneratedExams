from enum import Flag, auto


class ArgsType(Flag):
    CMD = auto()
    FILE = auto()


class ArgSubtype(Flag):
    DATA = auto()
    LINES = auto()


class Args:
    def __init__(self, args, args_type, args_subtype):
        self.args = args
        self.args_type = args_type
        self.args_subtype = args_subtype

    def get_arg(self):
        if self.args_type == ArgsType.CMD:
            return self.args
        else:
            input_file = open(self.args, "r")
            if self.args_subtype == ArgSubtype.LINES:
                res = input_file.readlines()
            else:
                res = input_file.read()
            input_file.close()
            return res
