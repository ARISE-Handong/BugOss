"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

failure_type = "AddressSanitizer: heap-use-after-free"
failure_stack_trace = [\
	"sctp_fill_hmac_digest_m /src/usrsctp/usrsctplib/netinet/sctp_auth.c:1549:2",
	"sctp_lowlevel_chunk_output /src/usrsctp/usrsctplib/netinet/sctp_output.c:4174:3",
	"sctp_med_chunk_output /src/usrsctp/usrsctplib/netinet/sctp_output.c:9360:17"]

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
