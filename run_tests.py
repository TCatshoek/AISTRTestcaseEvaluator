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
if args.type == "KLEE":
    errors = klee(args.testdir, args.bin)
if args.type == "AFL":
    errors = afl(args.testdir, args.bin)

# Report results :)
print(f"{len(errors)} Errors found:")
for error in sorted(errors, key=lambda x: int(x.split("_")[1])):
    print(error)
