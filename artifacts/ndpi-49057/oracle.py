"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

failure_type = "UndefinedBehaviorSanitizer: undefined-behavior"
failure_message = "protocols/snmp_proto.c:77:23: runtime crash: signed integer overflow: 6 + 2147483647 cannot be represented in type 'int'"
failure_stack_trace = [\
	"ndpi_search_snmp /src/ndpi/src/lib/protocols/snmp_proto.c:77:23",
	"check_ndpi_detection_func /src/ndpi/src/lib/ndpi_main.c:5211:4",
	"ndpi_check_flow_func /src/ndpi/src/lib/ndpi_main.c"]

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())

if failure_type not in exec_result:
	print("This is different failure type")
	exit()

if failure_message not in exec_result:
	print("The crash message is different")
	exit()

n_correct = 0
for st in failure_stack_trace:
	if st in exec_result:
		n_correct += 1

if n_correct == 3:
	print("Find a failure by a target bug")
else:
	print("This is different failure what we want to find")
