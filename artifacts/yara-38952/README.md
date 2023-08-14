### Failure information on yara-38952
- OSS-Fuzz issue: [38952](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=38952) (19 Sep 2021) 
- fuzz target: [pe_fuzzer.cc](https://github.com/VirusTotal/yara/blob/5cc28d24a251370218448100de4e9817e0d9233e/tests/oss-fuzz/pe_fuzzer.cc) which is the latest version before the oss-fuzz issue 38952 report time successfully reproduces a reported failure with a bug-revealing input (17 Sep 2021)
    - failure-observed commit: [5cc28d24a251370218448100de4e9817e0d9233e](https://github.com/VirusTotal/yara/commit/5cc28d24a251370218448100de4e9817e0d9233e) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=4884983219617792
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: heap-buffer-overflow  
    - stack trace:  
		```
		pe_get_section_full_name  
		pe__load  
		yr_modules_load 
		```

### Bug-inducing commit information
- bug-inducing commit: [5cc28d24a251370218448100de4e9817e0d9233e](https://github.com/VirusTotal/yara/commit/5cc28d24a251370218448100de4e9817e0d9233e) (17 Sep 2021)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `pe_parse_header(PE *, uint64_t, int)`
    - bug locations: [libyara/modules/pe/pe.c:1937-1938](https://github.com/VirusTotal/yara/commit/5cc28d24a251370218448100de4e9817e0d9233e#diff-a20bb88d25ed536935383bd979fdcd18dd1fb83b766eeccbddf3d1f4ed15514bR1937-R1938) 
- [seed_corpus.tar](https://drive.google.com/file/d/1-HGfAARLzsgXEC7EHWtoX_voMdBydecb/view?usp=share_link): initial seed corpus at bug-inducing commit (9 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 9
	- \# seed corpus at fix-inducing commit: 9
- the number of commits between failure-observed commit and BIC: 0 (the same commit)

### Bug-fixing commit information
- bug-fixing commit: [ae503e9671b274802cb07dc032b5e5cea28773bd](https://github.com/VirusTotal/yara/commit/ae503e9671b274802cb07dc032b5e5cea28773bd) (20 Sep 2021)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - reference [AFLChurn, CCS'21](https://dl.acm.org/doi/abs/10.1145/3460120.3484596)
- the number of commits between BIC and BFC: 0
	- BFC is a commit right after BIC
    - changed functions: undefined 
    - fix locations: [libyara/modules/pe/pe.c:1944](https://github.com/VirusTotal/yara/commit/5cc28d24a251370218448100de4e9817e0d9233e#diff-a20bb88d25ed536935383bd979fdcd18dd1fb83b766eeccbddf3d1f4ed15514bR1944) 

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
- failures by other bugs: 0 failures 

- target failure 
    - type: heap-buffer-overflow  
    - failure stack trace patterns for the expected failure:  
		```
		pe_get_section_full_name /src/yara/libyara/modules/pe/pe.c:1947:9  
		pe_parse_header /src/yara/libyara/modules/pe/pe.c:2215:37  
		pe__load /src/yara/libyara/modules/pe/pe.c:3962:9  
		yr_modules_load /src/yara/libyara/modules.c:158:16
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./pe_fuzzer failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 9 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer | 19308 |   no  |   no  |  3340 |  2941 |  4545 |  7012 |   no  |  8101 |    no  |
    |   AFL++   |  1418 |  5442 |  7543 |  3426 |  8721 |  3329 |  5739 |  3659 |  3341 |   4309 |

