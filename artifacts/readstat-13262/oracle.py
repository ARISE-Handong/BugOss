"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: target_failure type & top 5 stack trace & branch execution
"""

import sys
import re

target_failure_type = "heap-buffer-overflow"
target_failure_stack_trace = [\
	"#0.*:86",
	"#1.*:744",
	"#2.*:969",
	"#3.*:1081",
	"#4.*:17",
	]
branch_execution = "[BugOSS] src/sas/readstat_sas7bdat_read.c:602"
other_failure = {"heap-buffer-overflow" : [r'(#0.*:92:)*(#1.*:695:)', r'(#0.*:92:)*(#1.*:762:)'],
			"SEGV on unknown address 0x000000000000" : [r'(#0.*:440:)*(#1.*:774:)', r'(#0.*:440:)*(#1.*:498:)']}

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

n_correct = 0
for st in target_failure_stack_trace:
	if re.search(st, exec_result):
		n_correct += 1

if target_failure_type in exec_result and n_correct == 5:
	if branch_execution in exec_result:
		print("Find a target_failure by a target bug")

	# other failure with the same stack trace as the target failure
	else:
		print("This is a failure by an other bug")
else:
	for t in other_failure:
		if t in exec_result:
			if re.search(other_failure[t], exec_result):
				print("This is a failure by an other bug")
				exit()

	print("This is an unknown failure")
