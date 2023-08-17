"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: specific failure types
"""

import sys

failure_type = "ABRT"

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

if failure_type not in exec_result:
	print("This is different failure type")
	exit()

print("Find a failure by a target bug")
