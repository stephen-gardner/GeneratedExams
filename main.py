from datetime import datetime

from question import gen_question


new_res = set([])
old_res = set([])
while len(new_res) < 1000:
    size = len(new_res)
    seed = datetime.utcnow().timestamp()


    question = gen_question(datetime.utcnow().timestamp())
    new_subject = question.qvars.get("subject")
    old_subject = question.qvars.get("old_subject")
    new_res.add(new_subject)
    if len(new_res) > size:
        filename = str(size + 1).zfill(4)
        file = open("samples_new/" + filename, "w+")
        file.write(new_subject)
        file.close()
        file = open("samples_old/" + filename, "w+")
        file.write(old_subject)
        file.close()
    del question
print("{} unique exercises".format(len(new_res)))


# def print_new_question():
#     q = gen_question(datetime.utcnow().timestamp())
#     #output = q.qvars.get("subject") + "\n\n" + q.qvars.get("examples")
#     #print("\n\t\t\t\t>> %s (%d) <<\n" % (q.qvars.get("prog_name"), q.qvars.get("seed")))
#     print(q.qvars.get("subject"), end='')
#
#
# print_new_question()
