import subprocess
from celery import shared_task
from apps.submissions.models import Submissions
from apps.problems.models import TestCase

@shared_task
def execute_submission(submission_id):
    submission = Submissions.objects.get(id = submission_id)
    test_cases = TestCase.objects.filter(problem = submission.problem)
    for test_case in test_cases:
        try:
            result = subprocess.run(
                ['python', '-c', submission.code], #command
                input=test_case.input,              # stdin
                capture_output=True,                # capture the output
                text=True,                          # in string format
                timeout=5                           # 5 seconds time limit
            )
            if result.returncode!=0:
                submission.verdict = "RE"
                submission.save()
                return

            if result.stdout.strip() !=test_case.expected_output.strip():
                submission.verdict = "WRONG_ANSWER"
                submission.save()
                return

        except subprocess.TimeoutExpired:
            submission.verdict = "TLE"
            submission.save()
            return

    submission.verdict ="ACCEPTED"
    submission.save()        
        
