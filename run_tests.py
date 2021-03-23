import argparse
import pathlib
from afl import afl
from klee import klee

parser = argparse.ArgumentParser(description='Run AFL or KLEE testcases on a RERS problem')

parser.add_argument('type', choices=['KLEE', 'AFL'], help="Whether to run AFL or KLEE testcases")
parser.add_argument('testdir', type=pathlib.Path, help="The directory containing the testcases")
parser.add_argument('bin', type=pathlib.Path, help="The problem to run the testcases on")

args = parser.parse_args()

# Ensure directory and problem binary exist
assert args.testdir.is_dir(), f"Invalid testcase directory: {args.testdir}"
assert args.bin.is_file(), f"Invalid problem binary: {args.bin}"

# Run the testcases and look for errors
# We also record the first testcase creation time,
# and the timestamp for each error too.
# This gives us a set of (error, timestamp) tuples
if args.type == "KLEE":
    lowest_mtime, errors_w_time = klee(args.testdir, args.bin)
if args.type == "AFL":
    lowest_mtime, errors_w_time = afl(args.testdir, args.bin)

# Gather all timestamps for each error
errors_w_mtime_list = {}
for (error, mtime) in errors_w_time:
    if error not in errors_w_mtime_list:
        errors_w_mtime_list[error] = []
    errors_w_mtime_list[error].append(mtime)

# For each error, find the lowest mtime
# Also make the timestamp relative to the earliest seen mtime
errors_w_lowest_mtime = {}
for error, mtimes in errors_w_mtime_list.items():
    cur_lowest_mtime = min(mtimes)
    errors_w_lowest_mtime[error] = cur_lowest_mtime - lowest_mtime

# Report results :)
errors = errors_w_lowest_mtime.keys()
print(f"{len(errors)} Errors found:")
for error in sorted(errors, key=lambda x: int(x.split("_")[1])):
    print(error, "Timestamp:", errors_w_lowest_mtime[error])
