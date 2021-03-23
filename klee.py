from multiprocessing import Pool
from itertools import chain
import subprocess
import re
import os
import time
import datetime

# Use multiprocessing here since it is quite slow, and we can easily evaluate multiple testcases at the same time

def worker(args):
    testcase, problem_path, mtime = args
    found_errors = set()
    output = subprocess.run([f"KTEST_FILE={testcase} {problem_path}"], shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    errors = re.findall(r"error_\d+", output.stderr.decode())

    for error in errors:
        found_errors.add((error, mtime))
    return found_errors


def klee(testcases_path, problem_path):
    # Figure out start timestamp
    lowest_mtime = None
    with testcases_path.joinpath("info").open('r') as file:
        for line in file.readlines():
            match = re.match(r'Started: (\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)', line)
            if match:
                year = int(match.group(1))
                month = int(match.group(2))
                day = int(match.group(3))
                hour = int(match.group(4))
                minutes = int(match.group(5))
                seconds = int(match.group(6))

                d = datetime.datetime(year, month, day, hour, minutes, seconds)
                lowest_mtime = time.mktime(d.timetuple())

    assert lowest_mtime is not None, "Could not determine klee start time"

    testcases = [(x, problem_path, os.path.getmtime(x)) for x in testcases_path.glob("*.ktest")]
    n_testcases = len(testcases)

    print(f"Running {n_testcases} testcases, this might take a while...")

    with Pool(os.cpu_count()) as p:
        all_errors = p.map(worker, testcases)

    all_errors = set(chain(*all_errors))

    return lowest_mtime, all_errors
