# AISTRTestcaseEvaluator
Example scripts to see what errors have been reached in the RERS problems by AFL and KLEE. The script will also try to
determine when the AFL and KLEE runs started, and calculates relative timestamps for when each error was first reached.
Requires python 3 (>= 3.6?). Tested on linux, might work on mac, for windows you probably want to use WSL.

## Usage
### KLEE:
Make sure you follow the guide at https://github.com/apanichella/JavaInstrumentation/blob/main/docs/symbolic_rers.md

Especially ensure that you can successfully run test files like this:
`KTEST_FILE=klee-out-1/test000001.ktest ./Problem10.bc`

Then, run:

```shell
python run_tests.py KLEE /path/to/klee-out-n /path/to/ProblemX
```
Where `/path/to/klee-out-n` is the path to your klee output folder, and `/path/to/ProblemX` is the path to the binary 
compiled with `-lkleeRuntest`. Running this can take a while, but eventually you should see some output telling you how many
and which errors were found, including their timestamps.

### AFL:
Similar to above:
```shell
python run_tests.py AFL /path/to/afl-out-dir /path/to/ProblemX
```
Where `/path/to/afl-out-dir` is the output dir of AFL, and `/path/to/ProblemX` is a compiled version
of the corresponding RERS problem.

### Sample output:
```
18 Errors found:
error_0 Timestamp: 3.7867119312286377
error_9 Timestamp: 3.8500452041625977
error_13 Timestamp: 11.783378601074219
error_24 Timestamp: 10.130045175552368
error_26 Timestamp: 3.8000452518463135
error_39 Timestamp: 4.306711912155151
error_42 Timestamp: 7.670045375823975
error_48 Timestamp: 3.890045166015625
error_52 Timestamp: 10.363378524780273
error_60 Timestamp: 1.773378610610962
error_62 Timestamp: 1.1033785343170166
error_74 Timestamp: 5.143378496170044
error_75 Timestamp: 7.666712045669556
error_82 Timestamp: 1.9167118072509766
error_91 Timestamp: 14.906712055206299
error_93 Timestamp: 4.630045175552368
error_94 Timestamp: 3.8533785343170166
error_95 Timestamp: 1.703378677368164
```