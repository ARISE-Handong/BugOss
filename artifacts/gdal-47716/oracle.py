"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

failure_type = "AddressSanitizer: heap-buffer-overflow"
failure_stack_trace = [\
	"RMFDataset::WriteHeader() /src/gdal/frmts/rmf/rmfdataset.cpp:990:9",
	"RMFDataset::FlushCache(bool) /src/gdal/frmts/rmf/rmfdataset.cpp:1070:5",
	"RMFDataset::~RMFDataset() /src/gdal/frmts/rmf/rmfdataset.cpp:766:17"]

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
