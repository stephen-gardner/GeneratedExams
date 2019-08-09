import importlib
import pkgutil
import random

import layers.num_args as num_args


class Question:
    def __init__(self, seed, category, base_layers=None):
        path = "layers." + category

        self.qvars = {
            "layers": [],
            "path": path,
            "prog_name": category,
            "seed": seed,
        }

        main_layer = '.'.join([category, category])
        if base_layers is None or main_layer not in base_layers:
            base_layers = [main_layer] + base_layers if base_layers is not None else [main_layer]
        for layer_path in base_layers or []:
            self.load_layer("layers." + layer_path)

        self.available_layers = []
        pkg = importlib.import_module(path)
        for _, layer_name, _ in pkgutil.iter_modules(pkg.__path__):
            layer_path = '.'.join([category, layer_name])
            if base_layers is None or layer_path not in base_layers:
                self.available_layers.append("layers." + layer_path)

        random.seed(seed)

    def load_layer(self, path):
        split_path = path.split('.')
        if len(split_path) > 2:
            importlib.import_module('.'.join(split_path[0:2]))
        layer = importlib.import_module(path)
        layer.init(self.qvars)
        self.qvars.get("layers").append(layer)
        return layer

    def load_random_layers(self):
        """Loads a random number of applicable layers, and then initializes all active layers"""
        if len(self.available_layers) > 0:
            nlayers = random.randint(0, len(self.available_layers))
            for layer in random.sample(self.available_layers, nlayers):
                self.load_layer(layer)

        return self

    def limit_args(self, n=None, compare_type=None):
        """Enables num_args layer; by default, it sets the constraints to to print '\n' if the number of arguments is
        not 1
        """
        if n is not None:
            self.qvars["num_args.n"] = n
        if compare_type is not None:
            self.qvars["num_args.type"] = num_args.Compare[compare_type]

        num_args.init(self.qvars)
        self.qvars.get("layers").append(num_args)
        return self

    def execute(self, args):
        """Executes active layers' execute methods and returns result"""
        args = list(args) if type(args) is tuple else [args]
        for layer in self.qvars.get("layers"):
            args = layer.execute(args)
        return tuple(args)

    def format_example(self, arg, ex, cat):
        """Builds an I/O example string"""
        res = "$> ./{} \"{}\""

        if cat:
            res += " | cat -e"

        res += "\n{}"

        if cat:
            res += "$"

        return res.format(self.qvars.get("prog_name"), arg, ex)

    def build_examples(self):
        """Aggregates example sets of active layers, and builds an I/O example set"""
        examples = {""}
        for layer in self.qvars.get("layers"):
            for ex in layer.get_examples():
                examples.add(tuple(ex) if type(ex) is list else ex)

        res = []
        use_cat = True
        for ex in examples:
            original = "\" \"".join(ex) if type(ex) is tuple else ex
            res.append(self.format_example(original, '\n'.join(self.execute(ex)), use_cat))
            use_cat = random.randint(1, 100) > 90

        self.qvars["examples"] = "Examples:\n\n" + '\n'.join(res)
        return self

    def build_subject(self):
        """Aggregates subjects of active layers and removes non-empty, duplicate lines"""
        subject = """
The following operations must be performed in the order specified:
"""

        for layer in self.qvars.get("layers"):
            layer_sub = layer.get_subject()
            for sub in layer.get_substitutions():
                layer_sub = layer_sub.replace("%" + sub[0] + "%", sub[1])
            subject += layer_sub

        subject = subject.replace("\\%", "%").lstrip('\n').split('\n')
        present = set([])
        for line in subject:
            if line == "" or line not in present:
                present.add(line)
            else:
                subject.remove(line)
        self.qvars["subject"] = '\n'.join(subject)
        return self


def gen_question(seed):
    random.seed(seed)
    question = Question(seed, "move_word").load_random_layers()
    if random.getrandbits(1):
        question.limit_args()
    question.build_subject().build_examples()
    return question
