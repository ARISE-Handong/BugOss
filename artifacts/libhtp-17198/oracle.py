"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

failure_type = "AddressSanitizer: heap-buffer-overflow"
failure_stack_trace = [\
	"LzmaDec_WriteRem /src/libhtp/htp/lzma/LzmaDec.c:610:21",
	"LzmaDec_DecodeToDic /src/libhtp/htp/lzma/LzmaDec.c:917:3",
	"LzmaDec_DecodeToBuf /src/libhtp/htp/lzma/LzmaDec.c:1066:11"]

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
