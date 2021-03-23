from multiprocessing import Pool
from itertools import chain
import subprocess
import re
import os

# Use multiprocessing here since it is quite slow, and we can easily evaluate multiple testcases at the same time

def worker(args):
    testcase, problem_path = args
    found_errors = set()
    output = subprocess.run([f"KTEST_FILE={testcase} {problem_path}"], shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    errors = re.findall(r"error_\d+", output.stderr.decode())

    for error in errors:
        found_errors.add(error)
    return found_errors


def klee(testcases_path, problem_path):
    testcases = [(x, problem_path) for x in testcases_path.glob("*.ktest")]
    n_testcases = len(testcases)

    print(f"Running {n_testcases} testcases, this might take a while...")

    with Pool(os.cpu_count()) as p:
        all_errors = p.map(worker, testcases)

    return set(chain(*all_errors))
