"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: target_failure type
"""

import sys
import rt

target_failure_type = "SEGV on unknown address 0x000000000000"
other_failure_type = "unsigned integer overflow"
other_failure_stack_trace = [r"#0.*:165:31:", r"#0.*:165:19:", r"#0.*:558:", \
				r"#0.*:1952:", r"#0.*:1206:", r"#0.*:153:", r"#0.*:3489:"]

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
