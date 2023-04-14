"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

def check(exec_result, failure_type, failure_stack_trace):
	if failure_type not in exec_result:
		return False

	n_correct = 0
	for st in failure_stack_trace:
		if st in exec_result:
			n_correct += 1

	if n_correct == 3:
		print("Find a failure by a target bug")
		return True
	return False



f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())

failure17715_type = "AddressSanitizer: heap-buffer-overflow"
failure17715_stack_trace = [\
	"CRYPTO_strdup /src/openssl/crypto/o_str.c:21:25",
	"X509V3_add_value /src/openssl/crypto/x509/v3_utl.c:46:28",
	"i2v_GENERAL_NAME /src/openssl/crypto/x509/v3_alt.c:80:18"]

failure17722_type = "AddressSanitizer: SEGV on unknown address 0x000000000000"
failure17722_stack_trace = [\
	"GENERAL_NAME_print /src/openssl/crypto/x509/v3_alt.c:178:92",
	"do_i2r_name_constraints /src/openssl/crypto/x509/v3_ncons.c:184:13",
	"i2r_NAME_CONSTRAINTS /src/openssl/crypto/x509/v3_ncons.c:159:5"]


if check(exec_result, failure17715_type, failure17715_stack_trace) == False:
	if check(exec_result, failure17722_type, failure17722_stack_trace) == False:
		print("This is different failure what we want to find")
