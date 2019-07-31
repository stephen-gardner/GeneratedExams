import importlib
import pkgutil
import random
import parameters.num_args as num_args


class Question:
    def __init__(self, seed, prog_name, category, base_params=None):
        params = []
        path = "parameters." + category
        for param_name in base_params or []:
            params.append(importlib.import_module(path + "." + param_name))

        self.qvars = {
            "params": params,
            "path": path,
            "prog_name": prog_name,
            "seed": seed,
        }

        self.available_params = []
        sub_pkg = importlib.import_module(path)
        for _, param_name, _ in pkgutil.iter_modules(sub_pkg.__path__):
            if base_params is None or param_name not in base_params:
                self.available_params.append(importlib.import_module(path + "." + param_name))

        random.seed(seed)

    def limit_args(self, n=None, compare_type=None):
        """Enables num_args parameter; by default, it sets the constraints to to print '\n' if the number of arguments
        is not 1
        """
        if n is not None:
            self.qvars["num_args.n"] = n
        if compare_type is not None:
            self.qvars["num_args.type"] = num_args.Compare[compare_type]
        self.qvars.get("params").append(num_args)
        return self

    def load_params(self):
        """Loads a random number of applicable parameters, and then initializes all active parameters"""
        if len(self.available_params) > 1:
            nparams = random.randint(1, len(self.available_params))
            for param in random.sample(self.available_params, nparams):
                self.qvars.get("params").append(param)

        for param in self.qvars.get("params"):
            param.init(self.qvars)
        return self

    def execute(self):
        """Executes active parameters' execute methods and returns result"""
        for param in self.qvars.get("params"):
            param.execute()
        return self.qvars.get("args")

    def expand_vars(self, data):
        """Replaces %variables% in strings with their values in qvars"""
        for key, value in self.qvars.items():
            data = data.replace("%" + key + "%", str(value))
        return data.replace("\\%", "%")

    def build_examples(self):
        """Aggregates example sets of active parameters, and builds an I/O example set"""
        examples = [""]
        for param in self.qvars.get("params"):
            examples += param.get_examples()

        processed = set([])
        use_cat = True
        for ex in examples:
            if type(ex) is list:
                original = "\" \"".join(ex)
                self.qvars["args"] = ex
            else:
                original = ex
                self.qvars["args"] = [ex]
            processed.add(format_example(original, '\n'.join(self.execute()), use_cat))
            use_cat = random.randint(1, 100) > 90

        processed = self.expand_vars("Examples:\n\n" + '\n'.join(processed))
        self.qvars["examples"] = processed
        return self

    def build_subject(self):
        """Aggregates subjects of active parameters and removes non-empty, duplicate lines"""
        subject = ""

        for param in self.qvars.get("params"):
            subject += param.get_subject()

        subject = subject.split('\n')
        present = set([])
        for line in subject:
            if line == "" or line not in present:
                present.add(line)
            else:
                subject.remove(line)
        self.qvars["subject"] = self.expand_vars('\n'.join(subject))
        return self


def format_example(arg, ex, cat):
    """Builds an I/O example string"""
    res = "$>./%prog_name% \"{}\""

    if cat:
        res += " | cat -e"

    res += "\n{}"

    if cat:
        res += "$"

    return res.format(arg, ex)
