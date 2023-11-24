"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys
import re

target_failure_type = "null pointer"
other_failure_type = "unsigned integer overflow"
other_failure_stack_trace = [r"#0.*:275", r"#0.*:1147", r"#0.*:3047", r"#0.*:672", \
				r"#0.*:2996", r"#0.*:1809"]

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

if target_failure_type in exec_result:
	print("This is a failure by a target bug")
	exit()
elif other_failure_type in exec_result:
	for st in other_failure_stack_trace:
		if re.search(st, exec_result):
			print("This is a failure by an other bug")
			exit()

print("This is an unknown failure")
