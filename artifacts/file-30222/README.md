### Failure information on file-30222
- OSS-Fuzz issue: [30222](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=30222) (3 Feb 2021)
- fuzz target: [magic_fuzzer.cc](https://github.com/file/file/blob/6de3683de955277c4be4be350ec683b3203d3f31/fuzz/magic_fuzzer.c) which is the latest version before the oss-fuzz issue 30222 report time successfully reproduces a reported failure with a bug-revealing input (2 Feb 2021) 
    - failure-observed commit: [6de3683de955277c4be4be350ec683b3203d3f31](https://github.com/file/file/commit/6de3683de955277c4be4be350ec683b3203d3f31)
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=4885213098409984
- sanitizer: undefined
    - `$CFLAGS -fsanitize=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unsigned-integer-overflow,unreachable,vla-bound,vptr -fno-sanitize-recover=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unreachable,vla-bound,vptr`
    - `$CXXFLAGS -fsanitize=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unsigned-integer-overflow,unreachable,vla-bound,vptr -fno-sanitize-recover=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unreachable,vla-bound,vptr`
- reported failure symptom
    - type: null-dereference  
    - stack trace:  
		```
        trim_separator   
        file_buffer  
        magic_buffer
		```

### Bug-inducing commit information 
- bug-inducing commit: [6de3683de955277c4be4be350ec683b3203d3f31](https://github.com/file/file/commit/6de3683de955277c4be4be350ec683b3203d3f31) (2 Feb 2021)
    - search the oldest commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `file_seperator(magic_set *)`, `file_buffer(magic_set *, int, stat *, const char *, const void *, size_t)`
- [seed_corpus.tar](https://drive.google.com/file/d/1L9mPefcGuZsHUbZF54EXx6gwIvBi-zNc/view?usp=share_link): initial seed corpus at bug-inducing commit (34 initial seeds in `seed_corpus/`)
    - \# seed corpus at failure-observed commit: 34
    - \# seed corpus at fix-inducing commit: 34
- the number of commits between failure-observed commit and BIC: 0 (the same commit)

### Fix-inducing commit information 
- fix-inducing commit: [9c74f7b258cfe17b8c7f6eaaf6bbbf4ed14017d0](https://github.com/file/file/commit/9c74f7b258cfe17b8c7f6eaaf6bbbf4ed14017d0) (4 Feb 2021) 
    - search the first commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://github.com/file/file/commit/9c74f7b258cfe17b8c7f6eaaf6bbbf4ed14017d0)
    - changed functions: `trim_separator(magic_set *)`
- the number of commits between BIC and FIC: 0
    - FIC is a commit right after BIC

### Failure samples
- failure by a target bug: 1 failure in `failures/target/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and FIC date, which appears from BIC until FIC
- failures by other bugs: 7 failures in `failures/others/`
    - failures detected by AFL++ for 48 hours on a clean version (i.e., commit right before BIC)
        - 7 failures are collected

- target failure 
    - type: null-dereference  
    - failure stack trace patterns for the expected failure:  
		```
        trim_separator /src/file/src/funcs.c:262:13  
        file_buffer /src/file/src/funcs.c:472:2  
        magic_buffer /src/file/src/magic.c:542:6
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	UBSAN_OPTIONS=print_stacktrace=1  
	./magic_fuzzer failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 34 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no   |
    |   AFL++   |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no   |

