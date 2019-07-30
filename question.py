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
        if n is not None:
            self.qvars["num_args.n"] = n
        if compare_type is not None:
            self.qvars["num_args.type"] = num_args.Compare[compare_type]
        self.qvars.get("params").append(num_args)
        return self

    def load_params(self):
        if len(self.available_params) > 1:
            nparams = random.randint(1, len(self.available_params))
            for param in random.sample(self.available_params, nparams):
                self.qvars.get("params").append(param)

        for param in self.qvars.get("params"):
            param.init(self.qvars)
        return self

    def execute(self):
        for param in self.qvars.get("params"):
            param.execute()
        return self.qvars.get("args")

    def expand_vars(self, data):
        for key, value in self.qvars.items():
            data = data.replace("%" + key + "%", str(value))
        return data.replace("\\%", "%")

    def build_examples(self):
        examples = [""]
        for param in self.qvars.get("params"):
            examples += param.get_examples()

        processed = set([])
        use_cat = True
        for ex in examples:
            multi = type(ex) is list
            self.qvars["args"] = ex if multi else [ex]
            res = self.execute()
            if multi:
                ex = "\" \"".join(ex)
            processed.add(format_example(ex, "\n".join(res), use_cat))
            use_cat = random.randint(1, 100) > 90

        processed = self.expand_vars("Examples:\n\n" + "\n".join(processed))
        self.qvars["examples"] = processed
        return self

    def build_subject(self):
        subject = ""

        for param in self.qvars.get("params"):
            subject += param.get_subject()

        subject = self.expand_vars(subject)
        self.qvars["subject"] = subject
        return self


def format_example(arg, ex, cat):
    res = "$>./%prog_name% \"{}\""

    if cat:
        res += " | cat -e"

    res += "\n{}"

    if cat:
        res += "$"

    return res.format(arg, ex)
