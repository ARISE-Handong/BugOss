### Failure information on openssl-17715
- OSS-Fuzz issue: [17715](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=17715) (25 Sep 2019) 
- fuzz target: [x509.c](https://github.com/openssl/openssl/blob/5a2a2f66c5e79895400c6e895ce7f8d48db96bb8/fuzz/x509.c) which is the latest version before the oss-fuzz issue 17715 report time successfully reproduces a reported failure with a bug-revealing input (25 Sep 2019)
    - failure-observed commit: [5a2a2f66c5e79895400c6e895ce7f8d48db96bb8](https://github.com/openssl/openssl/commit/5a2a2f66c5e79895400c6e895ce7f8d48db96bb8) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=5652285425713152
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: heap-buffer-overflow  
    - stack trace:  
		```
		CRYPTO_strdup   
		X509V3_add_value   
		i2v_GENERAL_NAME 
		```

### Bug-inducing commit information
- bug-inducing commit: [4baee2d72e0c82bfd6de085df23a1bdc6af887ba](https://github.com/openssl/openssl/commit/4baee2d72e0c82bfd6de085df23a1bdc6af887ba) (24 Sep 2019)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
	- changed functions: `i2v_GENERAL_NAME(X509V3_EXT_METHOD *, GENERAL_NAME *, STACK_OF(CONF_VALUE) *)`, `GENERAL_NAME_print(BIO *, GENERAL_NAME *)`
- [seed_corpus.tar](https://drive.google.com/file/d/1Wi_-tVzGeIUPEE35EkSA2HYL0xoFsr_P/view?usp=share_link): initial seed corpus at bug-inducing commit (2240 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 2240
	- \# seed corpus at fix-inducing commit: 2241
- the number of commits between failure-observed commit and BIC: 9

### Bug-fixing commit information
- bug-fixing commit: [aec9667bd19a8ca9bdd519db3a231a95b9e92674](https://github.com/openssl/openssl/commit/aec9667bd19a8ca9bdd519db3a231a95b9e92674) (4 Nov 2019)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
	- developers explicitly mentioned the bug fixes [here](https://github.com/openssl/openssl/commit/aec9667bd19a8ca9bdd519db3a231a95b9e92674)
	- changed functions: `i2v_GENERAL_NAME(X509V3_EXT_METHOD *, GENERAL_NAME *, STACK_OF(CONF_VALUE) *)`, `GENERAL_NAME_print(BIO *, GENERAL_NAME *)`
- the number of commits between BIC and BFC: 267

### Failure samples
- failure by a target bug: 2 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
		- oss-fuzz issue [17715](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=17715), [17722](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=17722)
- failures by other bugs: 0 failures 

- target failure by issue-17715 (other failure symptom by issue-17722 written in `oracle.py`)
    - type: heap-buffer-overflow  
    - failure stack trace patterns for the expected failure:  
		```
		CRYPTO_strdup /src/openssl/crypto/o_str.c:21:25  
		X509V3_add_value /src/openssl/crypto/x509/v3_utl.c:46:28  
		i2v_GENERAL_NAME /src/openssl/crypto/x509/v3_alt.c:80:18
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./x509 failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 2240 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |  9395 | 12050 |  6979 | 11472 |  815  |  874  |   no  |   no  |  1991 |  5553  |
    |   AFL++   |   287 |  3662 | 17556 |  7291 | 19029 |   no  | 13262 |  4149 |   no  |    no  |

