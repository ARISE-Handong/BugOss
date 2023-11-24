"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: target_failure type
"""

import sys
import re

target_failure_type = "signed integer overflow"
other_failure_type = "unsigned integer overflow"
other_failure_stack_trace = [r"#0.*:5075", r"#0.*:54", r"#0.*:64", r"#0.*:146", r"#0.*:77", \
				r"#0.*:157", r"#0.*:65", r"#0.*:80", r"#0.*:131", r"#0.*206", \
				r"#0.*:91", r"#0.*:855", r"#0.*:154", r"#0.*:62", r"#0.*:138", \
				r"#0.*get_stun_lru_key"]

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

if target_failure_type in exec_result and other_failure_type not in exec_result:
	print("This is a failure by a target bug")
	exit()
elif other_failure_type in exec_result:
	for st in other_failure_stack_trace:
		if re.search(st, exec_result):
			print("This is a failure by an other bug")

print("This is an unknown failure")
