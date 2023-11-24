"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: target_failure type & top 1 stack trace
"""

import sys
import re

target_failure_type = "heap-use-after-free"
target_failure_stack_trace = r"#0.*:26"
other_failure = {"heap-buffer-overflow" : r"#0.*:347", \
		"heap-use-after-free" : r"#0.*:2993"}

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

if target_failure_type in exec_result and re.search(target_failure_stack_trace, exec_result):
	print("Find a failure by a target bug")
	exit()
else:
	for t in other_failure:
		if t in exec_result:
			if re.search(other_failure[t], exec_result):
				print("This is a failure by an other bug")
				exit()

print("This is an unknown failure")
