"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: failure type
"""

import sys
import re

failure_type = r"negation .* cannot be represented in type 'int'; cast to an unsigned type to negate this value to itself"

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

if re.search(failure_type, exec_result):
	print("Find a failure by a target bug")
	exit()

print("This is different failure what we want to find")
