"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: failure type & top 5 stack trace & branch execution
"""

import sys
import re

failure_type = "heap-buffer-overflow"
failure_stack_trace = [\
	"#0.*:86",
	"#1.*:744",
	"#2.*:969",
	"#3.*:1081",
	"#4.*:17",
	]
branch_execution = "[BugOSS] src/sas/readstat_sas7bdat_read.c:602"

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

if failure_type not in exec_result:
	print("This is different failure type")
	exit()

n_correct = 0
for st in failure_stack_trace:
	if re.search(st, exec_result):
		n_correct += 1

if n_correct == 5 and branch_execution in exec_result:
	print("Find a failure by a target bug")
else:
	print("This is different failure what we want to find")
