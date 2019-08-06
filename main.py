from datetime import datetime
from question import Question
# import random
#
# res = set([])
# while len(res) < 1000:
#     size = len(res)
#     seed = datetime.utcnow().timestamp()
#
#     if random.getrandbits(1):
#         question = Question(seed, "test_program", "strings").limit_args().load_params().build_subject().build_examples()
#     else:
#         question = Question(seed, "test_program", "strings").load_params().build_subject().build_examples()
#     output = question.qvars.get("subject")
#     res.add(output)
#     if len(res) > size:
#         filename = str(size + 1).zfill(4)
#         file = open("samples/" + filename, "w+")
#         file.write(output)
#         file.close()
#     del question
# print("{} unique exercises".format(len(res)))

seed = datetime.utcnow().timestamp()
question = Question(seed, "test_program", "strings").limit_args().load_layers().build_subject().build_examples()
output = question.qvars.get("subject") + "\n\n" + question.qvars.get("examples")
print(output)
