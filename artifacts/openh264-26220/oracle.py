"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: all crashes since there are no other failures in this artifact (i.e., general test oracle)
"""

import sys

f = open(sys.argv[1], 'r')
f.close()

print("Find a failure by a target bug")
