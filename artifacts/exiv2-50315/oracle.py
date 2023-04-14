"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

failure_type = "UndefinedBehaviorSanitizer: undefined-behavior"
failure_message = "/usr/local/bin/../include/c++/v1/numeric:517:59: runtime error: negation of -2147483648 cannot be represented in type 'int'; cast to an unsigned type to negate this value to itself"
failure_stack_trace = [\
	"operator() /usr/local/bin/../include/c++/v1/numeric:517:59",
	"gcd<int, int> /usr/local/bin/../include/c++/v1/numeric:549:26",
	"Exiv2::floatToRationalCast(float) /src/exiv2/src/types.cpp:633:21"]

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
