"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

failure_type = "AddressSanitizer: SEGV on unknown address 0x000000000000"
failure_stack_trace = [\
	"JBIG2SymbolDict::setBitmap(unsigned int, JBIG2Bitmap*) /src/poppler/poppler/JBIG2Stream.cc:968:74",
	"JBIG2Stream::readSymbolDictSeg(unsigned int, unsigned int, unsigned int*, unsigned int) /src/poppler/poppler/JBIG2Stream.cc:1840:25",
	"JBIG2Stream::readSegments() /src/poppler/poppler/JBIG2Stream.cc:1331:18"]

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
