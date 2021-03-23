import subprocess
import re

def afl(testcases_path, problem_path):
    found_errors = set()
    testcases = [x for x in testcases_path.glob("**/*") if x.is_file()]
    for testcase in testcases:
        output = subprocess.run([f"cat {testcase} | {problem_path}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        errors = re.findall(r"error_\d+", output.stderr.decode())
        for error in errors:
            found_errors.add(error)
    return found_errors
