"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: target_failure type & top 8 stack trace & branch execution
"""

import sys
import re

target_failure_type = "heap-buffer-overflow"
target_failure_stack_trace = [\
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

other_failure = {"out-of-memory" : [r"#0.*:95:"], \
		"use-of-uninitialized-value" : [r"#0.*:1208:"], \
		"heap-buffer-overflow" : [r"#0.*:1207:", r"#0.*:28:", r"#0.*:625:", r"#0.*:275:", \
					r"#0.*:51:", r"#0.*:624:", r"#0.*:19:", r"#0.*:580:", r"#0.*:81:"]}

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

if target_failure_type not in exec_result:
	print("This is different target_failure type")
	exit()

n_correct = 0
for st in target_failure_stack_trace:
	if re.search(st, exec_result):
		n_correct += 1

if n_correct == 8 and branch_execution in exec_result:
	print("This is a failure by a target bug")
else:
	for t in other_failure:
		if t in exec_result:
			for st in other_failure[t]:
				if re.search(other_failure[t], exec_result):
					print("This is a failure by an other bug")
					exit()
	print("This is an unkown failure")
