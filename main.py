from datetime import datetime
from question import Question

seed = datetime.utcnow().timestamp()
question = Question(seed, "test_program", "strings").limit_args().load_params().build_subject().build_examples()
print(question.qvars.get("subject"), "\n\n", question.qvars.get("examples"), sep='')
