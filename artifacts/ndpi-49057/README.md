### Failure information on ndpi-49057
- OSS-Fuzz issue: [49057](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=49057) (12 Jul 2022) 
- fuzz target: [fuzz_process_packet.c](https://github.com/ntop/nDPI/blob/9c235796af60977ba316c612d4a02014896127f8/fuzz/fuzz_process_packet.c) which is the latest version before the oss-fuzz issue 49057 report time successfully reproduces a reported failure with a bug-revealing input (12 Jul 2022)
    - failure-observed commit: [9c235796af60977ba316c612d4a02014896127f8](https://github.com/ntop/nDPI/commit/9c235796af60977ba316c612d4a02014896127f8)
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=4842970968358912
- sanitizer: undefined
    - `$CFLAGS -fsanitize=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unsigned-integer-overflow,unreachable,vla-bound,vptr -fno-sanitize-recover=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unreachable,vla-bound,vptr`
    - `$CXXFLAGS -fsanitize=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unsigned-integer-overflow,unreachable,vla-bound,vptr -fno-sanitize-recover=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unreachable,vla-bound,vptr`
- reported failure symptom 
    - type: integer-overflow 
    - stack trace:  
		```
		ndpi_search_snmp   
		check_ndpi_detection_func   
		ndpi_check_flow_func 
		```

### Bug-inducing commit information
- bug-inducing commit: [2edfaeba4ada90ca8771a44132d2b9cc85e45570](https://github.com/ntop/nDPI/commit/2edfaeba4ada90ca8771a44132d2b9cc85e45570) (11 Jul 2022)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
	- changed functions: `get_int(const unsigned char *, int, u_int16_t *)`, `ndpi_search_snmp(struct ndpi_detection_module_struct *, struct ndpi_flow_struct *)`
- [seed_corpus.tar](https://drive.google.com/file/d/1IPe1pzOZhsPjvNRa75NmvvpzNfu4yyZS/view?usp=share_link): initial seed corpus at bug-inducing commit (351 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 352
	- \# seed corpus at fix-inducing commit: 352
- the number of commits between failure-observed commit and BIC: 4

### Fix-inducing commit information
- fix-inducing commit: [407155755da29734e9b8a8e7a6960c568b1d3188](https://github.com/ntop/nDPI/commit/407155755da29734e9b8a8e7a6960c568b1d3188) (13 Jul 2022)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
	- developers explicitly mentioned the bug fixes [here](https://github.com/ntop/nDPI/commit/407155755da29734e9b8a8e7a6960c568b1d3188)
	- changed functions: `ndpi_asn1_ber_decode_length(const unsigned char *, int, u_int16_t *)`, `krb_decode_asn1_length(ndpi_detection_module_struct *, size_t *)`, `ndpi_search_ldap(struct ndpi_detection_module_struct *, struct ndpi_flow_struct *)`, `ndpi_search_snmp(struct ndpi_detection_module_struct *, struct ndpi_flow_struct *)`
- the number of commits between BIC and FIC: 5

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and FIC date, which appears from BIC until FIC
- failures by other bugs: 16 failures in `other_failures/`
    - failures detected by AFL++ for 48 hours on a clean version (i.e., commit right before BIC)
		- 16 failures are collected

- target failure  
    - type: integer-overflow
    - crash message: protocols/snmp_proto.c:77:23: runtime error: signed integer overflow: 6 + 2147483647 cannot be represented in type 'int'
    - failure stack trace patterns for the expected failure:  
		```
		ndpi_search_snmp /src/ndpi/src/lib/protocols/snmp_proto.c:77:23  
		check_ndpi_detection_func /src/ndpi/src/lib/ndpi_main.c:5211:4  
		ndpi_check_flow_func /src/ndpi/src/lib/ndpi_main.c
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	UBSAN_OPTIONS=print_stacktrace=1 
	./fuzz_process_packet failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 351 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no   |
    |   AFL++   |   no  |   no  |   no  |   no  |   no  |   no  |   no  |  2189 |   no  |  8076  |

