"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: failure type & top 1 stack trace
"""

import sys
import re

failure_type = "heap-use-after-free"
failure_stack_trace = "#0.*:26"

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

if failure_type in exec_result and re.search(failure_stack_trace, exec_result):
	print("Find a failure by a target bug")
	exit()

print("This is different failure what we want to find")
