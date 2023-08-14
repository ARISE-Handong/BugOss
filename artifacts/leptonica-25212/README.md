### Failure information on leptonica-25212
- OSS-Fuzz issue: [25212](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=25212) (26 Aug 2020) 
- fuzz target: [pix4_fuzzer.cc](https://github.com/DanBloomberg/leptonica/blob/dfde88c09a37ccced3c2e08b2db971145f4ac279/prog/fuzzing/pix4_fuzzer.cc) which is the latest version before the oss-fuzz issue 25212 report time successfully reproduces a reported failure with a bug-revealing input (26 Aug 2020)
    - failure-observed commit: [dfde88c09a37ccced3c2e08b2db971145f4ac279](https://github.com/DanBloomberg/leptonica/commit/dfde88c09a37ccced3c2e08b2db971145f4ac279) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=5650690016542720
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: null-dereference  
    - stack trace:  
		```
		pixGetBinnedComponentRange
		```

### Bug-inducing commit information
- bug-inducing commit: [8fc49016cf44ecbbab28979442e2781bd064584e](https://github.com/DanBloomberg/leptonica/commit/8fc49016cf44ecbbab28979442e2781bd064584e) (25 Aug 2020)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `pixGetBinnedColor(PIX *, PIX *, l_int32, l_int32, NUMA *, l_uint32 **, PIXA *)`
    - bug locations: [src/pix4.c:2803-2805](https://github.com/DanBloomberg/leptonica/commit/8fc49016cf44ecbbab28979442e2781bd064584e#diff-4af4b9f67a672e1ea1a119e5d96ec4be38ec64d9b6ac338497c5a18d8fbaa076R2803-R2805) 
- [seed_corpus.tar](https://drive.google.com/file/d/1l4r5b3JWadhv4rRJld9zz-z8wZJnYkrj/view?usp=share_link): initial seed corpus at bug-inducing commit (10 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 10 
	- \# seed corpus at fix-inducing commit: 10
- the number of commits between failure-observed commit and BIC: 2

### Bug-fixing commit information
- bug-fixing commit: [f301010cd4495a11d96504642737a85c386e6618](https://github.com/DanBloomberg/leptonica/commit/f301010cd4495a11d96504642737a85c386e6618) (29 Aug 2020)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://github.com/DanBloomberg/leptonica/commit/f301010cd4495a11d96504642737a85c386e6618)
    - changed functions: `pixGetBinnedComponentRange(PIX *, l_int32, l_int32, l_int32, l_int32 *, l_int32 *, l_uint32 **, l_int32)`, `pixGetRankColorArray(PIX *, l_int32, l_int32, l_int32, l_uint32 **, PIXA *, l_int32)`, `pixGetBinnedColor(PIX *, PIX *, l_int32, l_int32, NUMA *, l_uint32 **, PIXA *)`
    - fix locations: [src/pix4.c:2813-2814](https://github.com/DanBloomberg/leptonica/commit/f301010cd4495a11d96504642737a85c386e6618#diff-4af4b9f67a672e1ea1a119e5d96ec4be38ec64d9b6ac338497c5a18d8fbaa076R2813-R2814) 
- the number of commits between BIC and BFC: 5 

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
- failures by other bugs: 1 failures in `other_failures/`
	- oss-fuzz issue [25202](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=25202)

- target failure 
    - type: null-dereference  
    - failure stack trace patterns for the expected failure:  
		```
		pixGetBinnedComponentRange /src/leptonica/src/pix4.c
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./pix4_fuzzer failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 10 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |    no  |
    |   AFL++   |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |    no  |

