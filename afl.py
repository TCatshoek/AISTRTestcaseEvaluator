import subprocess
import re
import os


def afl(out_dir, problem_path):
    lowest_mtime = None

    # Check the "fuzzer_stats" file for start timestamp
    with out_dir.joinpath("fuzzer_stats").open('r') as file:
        for line in file.readlines():
            match = re.match(r'start_time\s*:\s*(\d+)', line)
            if match:
                lowest_mtime = int(match.group(1))

    assert lowest_mtime is not None, "Could not determine fuzzing start time"

    testcases_path = out_dir.joinpath("crashes")

    found_errors = set()

    testcases = [(x, os.path.getmtime(x)) for x in testcases_path.glob("**/*") if x.is_file()]

    for testcase, mtime in testcases:
        if lowest_mtime is None or mtime < lowest_mtime:
            lowest_mtime = mtime

        output = subprocess.run([f"cat {testcase} | {problem_path}"], shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        errors = re.findall(r"error_\d+", output.stderr.decode())
        for error in errors:
            found_errors.add((error, mtime))

    return lowest_mtime, found_errors
