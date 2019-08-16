EXAM_IP=localhost
FINISHED=false

function examshell() {
  if [ ! -z "$INTRA_ID" ]; then
    echo "Already taking exam as user '$INTRA_ID'"
    return
  fi

  echo -n "Intra ID: "
  read -r INTRA_ID
  echo -n "Password: "
  read -rs PASSWORD
  export INTRA_ID
  echo

  rm -rf "$HOME/exam"
  mkdir -p "$HOME/exam"
  cd "$HOME/exam" || return

  clear
  echo "Exam session started."
  echo "Run all tests in '$HOME/exam/tests.txt' through your program."
  echo "Submit your output in '$HOME/exam/output.txt' with the command 'grademe'."
  echo "You can 'finish' to terminate the exam at any time."
  echo
  echo "Press any key to continue..."
  read -k1 -s

  gen_subject
  FINISHED=false
}

function finish() {
  if [ -z "$INTRA_ID" ]; then
    echo "No exam session is currently active"
    return
  fi

  FINISHED=true
  grademe
  echo "Exam session terminated."
  unset INTRA_ID
  rm -rf "$HOME/exam"
}

function gen_subject() {
  if [ -z "$INTRA_ID" ]; then
    echo "No exam session is currently active"
    return
  fi

  clear
  SUBJECT=$(curl -s "$EXAM_IP:4242/$INTRA_ID/generate")
  echo "$SUBJECT" >"$HOME/exam/subject.txt"
  curl -s "$EXAM_IP:4242/$INTRA_ID/tests" >"$HOME/exam/tests.txt"
  echo "$SUBJECT"
  echo
}

function cheat_exam() {
  if [ -z "$INTRA_ID" ]; then
    echo "No exam session is currently active"
    return
  fi

  ANSWERS=$(curl -s "$EXAM_IP:4242/$INTRA_ID/answers")
  echo "$ANSWERS" >"$HOME/exam/output.txt"
  echo "You're filthy!"
}

function grademe() {
  if [ -z "$INTRA_ID" ]; then
    echo "No exam session is currently active"
    return
  fi

  GRADE=$(curl -s "$EXAM_IP:4242/$INTRA_ID/grade" -X POST --data-binary "@$HOME/exam/output.txt")
  echo "Grade: $GRADE"
  echo
  echo "Press any key to continue..."
  read -k1 -s
  rm -f "$HOME/exam/output.txt"

  if [ "$FINISHED" = false ]; then
    gen_subject
  fi
}
