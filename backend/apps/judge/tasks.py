import subprocess
import tempfile
import os
from celery import shared_task
from apps.submissions.models import Submissions
from apps.problems.models import TestCase

def get_command(submission):
    if submission.language =='python':
        return ['python', '-c',submission.code], None, None
    
    elif submission.language == 'cpp':
        with tempfile.NamedTemporaryFile(suffix='.cpp', mode = 'w', delete=False) as f:
            f.write(submission.code)
            source_file = f.name
        compiled_file = source_file.replace('.cpp', '')
        compile_result = subprocess.run(['g++',source_file, '-o',compiled_file], capture_output=True, text=True)
        if compile_result.returncode!=0:
            return None, None, "CE"
        return [compiled_file], source_file, compiled_file 

    elif submission.language == 'c':   
        with tempfile.NamedTemporaryFile(suffix='.c', mode = 'w', delete=False) as f:
            f.write(submission.code)
            source_file = f.name  ## "/tmp/tmpAbc123.cpp"
        compiled_file = source_file.replace('.c', '') #this will become - "/tmp/tmpAbc123"
        compile_result = subprocess.run(['gcc',source_file, '-o',compiled_file], capture_output=True, text=True)
        if compile_result.returncode!=0:
            return None, None, "CE"
        return [compiled_file], source_file, compiled_file 

@shared_task
def execute_submission(submission_id):
    submission = Submissions.objects.get(id = submission_id)
    test_cases = TestCase.objects.filter(problem = submission.problem)
    cmd, source_file, compiled_file = get_command(submission)
    if compiled_file == "CE":
        submission.verdict = "CE"
        submission.save()
        return
    
    
    def cleanup():
        if source_file:
            os.remove(source_file)
        if compiled_file and compiled_file !="CE":
            os.remove(compiled_file) 


    for test_case in test_cases:
        try:
            result = subprocess.run(
                cmd,                                #command from get_command
                input=test_case.input,              # stdin
                capture_output=True,                # capture the output
                text=True,                          # in string format
                timeout=5                           # 5 seconds time limit
            )
            if result.returncode!=0:
                submission.verdict = "RE"
                submission.save()
                cleanup()
                return

            if result.stdout.strip() !=test_case.expected_output.strip():
                submission.verdict = "WRONG_ANSWER"
                submission.save()
                cleanup()
                return

        except subprocess.TimeoutExpired:
            submission.verdict = "TLE"
            submission.save()
            cleanup()
            return

    submission.verdict ="ACCEPTED"
    submission.save() 
    import subprocess
import tempfile
import os
from celery import shared_task
from apps.submissions.models import Submissions
from apps.problems.models import TestCase

def get_command(submission):
    if submission.language =='python':
        return ['python', '-c',submission.code], None, None
    
    elif submission.language == 'cpp':
        with tempfile.NamedTemporaryFile(suffix='.cpp', mode = 'w', delete=False) as f:
            f.write(submission.code)
            source_file = f.name
        compiled_file = source_file.replace('.cpp', '')
        compile_result = subprocess.run(['g++',source_file, '-o',compiled_file], capture_output=True, text=True)
        if compile_result.returncode!=0:
            return None, None, "CE"
        return [compiled_file], source_file, compiled_file 

    elif submission.language == 'c':   
        with tempfile.NamedTemporaryFile(suffix='.c', mode = 'w', delete=False) as f:
            f.write(submission.code)
            source_file = f.name  ## "/tmp/tmpAbc123.cpp"
        compiled_file = source_file.replace('.c', '') #this will become - "/tmp/tmpAbc123"
        compile_result = subprocess.run(['gcc',source_file, '-o',compiled_file], capture_output=True, text=True)
        if compile_result.returncode!=0:
            return None, None, "CE"
        return [compiled_file], source_file, compiled_file 

@shared_task
def execute_submission(submission_id):
    submission = Submissions.objects.get(id = submission_id)
    test_cases = TestCase.objects.filter(problem = submission.problem)
    cmd, source_file, compiled_file = get_command(submission)
    if compiled_file == "CE":
        submission.verdict = "CE"
        submission.save()
        return
    
    
    def cleanup():
        if source_file:
            os.remove(source_file)
        if compiled_file and compiled_file !="CE":
            os.remove(compiled_file) 


    for test_case in test_cases:
        try:
            result = subprocess.run(
                cmd,                                #command from get_command
                input=test_case.input,              # stdin
                capture_output=True,                # capture the output
                text=True,                          # in string format
                timeout=5                           # 5 seconds time limit
            )
            if result.returncode!=0:
                submission.verdict = "RE"
                submission.save()
                cleanup()
                return

            if result.stdout.strip() !=test_case.expected_output.strip():
                submission.verdict = "WRONG_ANSWER"
                submission.save()
                cleanup()
                return

        except subprocess.TimeoutExpired:
            submission.verdict = "TLE"
            submission.save()
            cleanup()
            return

    submission.verdict ="ACCEPTED"
    submission.save()        
    cleanup()       

       
