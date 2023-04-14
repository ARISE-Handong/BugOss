"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

failure_type = "AddressSanitizer: heap-buffer-overflow"
failure_stack_trace = [\
	"sas_read8 /src/readstat/src/sas/readstat_sas.c:86:5",
	"sas7bdat_parse_subheader_pointer /src/readstat/src/sas/readstat_sas7bdat_read.c:680:24",
	"sas7bdat_parse_page_pass2 /src/readstat/src/sas/readstat_sas7bdat_read.c:792:27"]
failure_logging = "[BugOSS] src/sas/readstat_sas7bdat_read.c:602"

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())

if failure_type not in exec_result:
	print("This is different failure type")
	exit()

if failure_logging not in exec_result:
	print("The additional branch is not executed")
	exit()

n_correct = 0
for st in failure_stack_trace:
	if st in exec_result:
		n_correct += 1

if n_correct == 3:
	print("Find a failure by a target bug")
else:
	print("This is different failure what we want to find")
