"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

failure_type = "AddressSanitizer: heap-buffer-overflow"
failure_stack_trace = [\
		"grk::PacketIter::get_include(unsigned short) /src/grok/src/lib/jp2/codestream/PacketIter.cpp:1447:14",
		"grk::PacketIter::update_include() /src/grok/src/lib/jp2/codestream/PacketIter.cpp:1459:17",
		"grk::pi_next(grk::PacketIter*) /src/grok/src/lib/jp2/codestream/PacketIter.cpp:1414:11",
		"grk::T2Decompress::decompress_packets(unsigned short, grk::ChunkBuffer*, unsigned long*) /src/grok/src/lib/jp2/t2/T2Decompress.cpp:71:10"]

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())

if failure_type not in exec_result:
	print("This is different failure type")
	exit()

n_correct = 0
for st in failure_stack_trace:
	if st in exec_result:
		n_correct += 1

if n_correct == 4:
	print("Find a failure by a target bug")
else:
	print("This is different failure what we want to find")
