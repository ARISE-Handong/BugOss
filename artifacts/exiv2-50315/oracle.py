"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: target_failure type
"""

import sys
import re

target_failure_type = r"negation .* cannot be represented in type 'int'; cast to an unsigned type to negate this value to itself"
other_failure_type = "unsigned integer overflow"
other_failure_stack_trace = [r'#0.*Exiv2::MemIo::seek\(long, Exiv2::BasicIo::Position\)', \
				r"#0.*:523:", r"#0.*:1276:", r"#0.*:1276:33", r"#0.*:1276:67", \
				r"#0.*:1307:", r"#0.*:445:", r"#0.*:2491:", r"#0.*:1082:", \
				r"#0.*:91:", r"#0.*:1259:", r"#0.*:755:", r"#0.*:385:", r"#0.*:192:"]

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

if re.search(target_failure_type, exec_result):
	print("This is a failure by a target bug")
	exit()
elif other_failure_type in exec_result:
	for st in other_failure_stack_trace:
		if re.search(st, exec_result):
			print("This is a failure by an other bug")
			exit()

print("This is an unknwon failure")
