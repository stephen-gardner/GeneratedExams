from datetime import datetime

from question import gen_question


# res = set([])
# while len(res) < 1000:
#     size = len(res)
#     seed = datetime.utcnow().timestamp()
#
#     if random.getrandbits(1):
#         question = Question(seed, "test_program", "capitalizer").limit_args().load_params().build_subject().build_examples()
#     else:
#         question = Question(seed, "test_program", "capitalizer").load_params().build_subject().build_examples()
#     output = question.qvars.get("subject")
#     res.add(output)
#     if len(res) > size:
#         filename = str(size + 1).zfill(4)
#         file = open("samples/" + filename, "w+")
#         file.write(output)
#         file.close()
#     del question
# print("{} unique exercises".format(len(res)))


def print_new_question():
    q = gen_question(datetime.utcnow().timestamp())
    output = q.qvars.get("subject") + "\n\n" + q.qvars.get("examples")
    print("\n\t\t\t\t>> %s (%d) <<\n" % (q.qvars.get("prog_name"), q.qvars.get("seed")))
    print(output)


print_new_question()
