"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

failure_type = "UndefinedBehaviorSanitizer: SEGV on unknown address 0x000000000000"
failure_stack_trace = [\
	"trim_separator /src/file/src/funcs.c:262:13",
	"file_buffer /src/file/src/funcs.c:472:2",
	"magic_buffer /src/file/src/magic.c:542:6"]

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())

if failure_type not in exec_result:
	print("This is different failure type")
	exit()

n_correct = 0
for st in failure_stack_trace:
	if st in exec_result:
		n_correct += 1

if n_correct == 3:
	print("Find a failure by a target bug")
else:
	print("This is different failure what we want to find")
