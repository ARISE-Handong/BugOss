"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: failure type & top 2 stack trace
"""

import sys
import re

failure_type = "memory leaks"
failure_stack_trace = ["#0.*:98", "#1.*:1447"]

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

if n_correct == 2:
	print("Find a failure by a target bug")
else:
	print("This is different failure what we want to find")
