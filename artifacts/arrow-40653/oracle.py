"""
	- It receives an execution result of fuzzer with a failing test case
	- Bug-specific test oracles: specific target_failure types
"""

import sys
import re

target_failure_type = "ABRT"
other_failure_type = ["global-buffer-overflow", "signed integer overflow", "negation.*.cast to an unsigned tpe", "SEGV"]

other_failures = {"global-buffer-overflow" : "#0.*:109:",
		"signed integer overflow" : "#0.*:338:",
		"SEGV" : "#0.*arrow::internal::detail::FormatTwoDigits<long>(long, char**)",
		"negation .* cannot be represented in type 'std::chrono::duration<long long, std::ratio<.*>>::rep' (aka 'long long'); cast to an unsigned type to negate this value to itself" : "#0.*:1103:"
		}

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())
f.close()

if target_failure_type in exec_result:
	print("This is a failure by a target bug")
	exit()

print("Find a target_failure by a target bug")
