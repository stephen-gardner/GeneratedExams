from datetime import datetime
from bottle import route, run, request

from question import gen_question
from validate import generate_tests, validate_output

users = {}


@route("/<login>/generate", method="get")
def generate_subject(login):
    user_data = users.get(login)
    if user_data is None:
        seed = datetime.utcnow().timestamp()
        q = gen_question(seed).build_subject().build_examples()
        tests = generate_tests(seed)
        user_data = {"question": q, "tests": tests}
        users[login] = user_data
    q = user_data.get("question")
    header = "\t\t\t\t>> %s (%d) <<\n" % (q.qvars.get("prog_name"), q.qvars.get("seed"))
    content = "%s\n%s\n\n%s" % (header, q.qvars.get("subject"), q.qvars.get("examples"))
    return content


@route("/<login>/tests", method="get")
def get_tests(login):
    user_data = users.get(login)
    if user_data is None:
        return "No active exam session\n"
    return '\n'.join(user_data.get("tests"))


@route("/<login>/grade", method="post")
def grade_submission(login):
    user_data = users.get(login)
    if user_data is None:
        return "No active exam session\n"
    submission = request.body.read().decode("UTF-8").splitlines()
    seed = user_data.get("question").qvars.get("seed")
    result = validate_output(seed, user_data.get("tests"), submission)
    del users[login]
    return result


@route("/<login>/answers", method="get")
def get_answer(login):
    """This function exists solely for testing purposes, and should be disabled/removed for production"""
    user_data = users.get(login)
    if user_data is None:
        return "No active exam session\n"
    q = user_data.get("question")
    tests = user_data.get("tests")
    answers = []
    for test in tests:
        answers.append('\n'.join(q.execute(test)))
    return '\n'.join(answers)


run(host='localhost', port=4242)
