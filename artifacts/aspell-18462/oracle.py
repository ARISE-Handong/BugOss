"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

failure_type = "AddressSanitizer: heap-buffer-overflow"
failure_stack_trace = [\
	"acommon::ObjStack::dup_top(acommon::ParmString) /src/aspell/./common/objstack.hpp:95:20",
	"acommon::ObjStack::dup(acommon::ParmString) /src/aspell/./common/objstack.hpp:103:38",
	"acommon::StringMap::add(acommon::ParmString const&) /src/aspell/./common/string_map.hpp:78:35"]

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
