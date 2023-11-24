"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: target_failure type & top 1 stack trace
"""

import sys
import re

target_failure_type = "SEGV on unknown address 0x000000000000"
target_failure_stack_trace = "#0.*:2536"
other_failure_type = "SEGV on unknown address 0x000000000000"
other_failure_stack_trace = "#0.*:3033"

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

if target_failure_type in exec_result and re.search(target_failure_stack_trace, exec_result):
	print("This is a failure by a target bug")
	exit()
elif other_failure_type in exec_result and re.search(other_failure_stack_trace, exec_result):
	print("This is a failure by an other bug")
	exit()

print("This is an unknown failure")
