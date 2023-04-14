"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

failure_type = "AddressSanitizer: SEGV on unknown address 0x000000000000"
failure_stack_trace = [\
	"ZSTD_copy16 /src/zstd/tests/fuzz/../../lib/common/zstd_internal.h:199:55",
	"ZSTD_execSequence /src/zstd/tests/fuzz/../../lib/decompress/zstd_decompress_block.c:731:5",
	"ZSTD_decompressSequences_body /src/zstd/tests/fuzz/../../lib/decompress/zstd_decompress_block.c:1020:39"]


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
