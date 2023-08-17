"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: failure type
"""

import sys

failure_type = "SEGV on unknown address 0x000000000000"

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

if failure_type in exec_result:
	print("Find a failure by a target bug")
	exit()

print("This is different failure what we want to find")
