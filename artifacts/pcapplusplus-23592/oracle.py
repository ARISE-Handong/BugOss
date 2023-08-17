"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: failure type & top 8 stack trace & branch execution
"""

import sys
import re

failure_type = "heap-buffer-overflow"
failure_stack_trace = [\
	"#0.*:1614",
	"#1.*:1118",
	"#2.*:153",
	"#3.*:52",
	"#4.*:349",
	"#5.*:63",
	"#6.*:109",
	"#7.*:52",
	]
branch_execution = "[BugOSS] Packet++/src/Packet.cpp:712"

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

if n_correct == 8 and branch_execution in exec_result:
	print("Find a failure by a target bug")
else:
	print("This is different failure what we want to find")
