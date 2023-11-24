### Failure information on libarchive-44843
- OSS-Fuzz issue: [44843](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=44843) (19 Feb 2022) 
- fuzz target: [libarchive_fuzzer.cc](https://github.com/google/oss-fuzz/blob/a996649c2c9d327062e8a85ff0ce729084064552/projects/libarchive/libarchive_fuzzer.cc) which is the latest version before the oss-fuzz issue 44843 report time successfully reproduces a reported failure with a bug-revealing input 
    - failure-observed commit: [72ce1ff7c6857a7334baa05884e69b9264a2199c](https://github.com/libarchive/libarchive/commit/72ce1ff7c6857a7334baa05884e69b9264a2199c) (19 Feb 2022)
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=4960581478645760
- sanitizer: undefined
    - `$CFLAGS -fsanitize=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unsigned-integer-overflow,unreachable,vla-bound,vptr -fno-sanitize-recover=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unreachable,vla-bound,vptr`
    - `$CXXFLAGS -fsanitize=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unsigned-integer-overflow,unreachable,vla-bound,vptr -fno-sanitize-recover=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unreachable,vla-bound,vptr`
- reported failure symptom
    - type: null-dereference 
    - stack trace:  
		```
        read_data_compressed
        archive_read_format_rar_read_data
        _archive_read_data_block
		```

### Bug-inducing commit information
- bug-inducing commit: [52efa50c69653029687bfc545703b7340b7a51e2](https://github.com/libarchive/libarchive/commit/52efa50c69653029687bfc545703b7340b7a51e2) (17 Feb 2022)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `read_data_compressed(struct archive_read *a, const void **buff, size_t *size, int64_t *offset, size_t looper)`, `expand(struct archive_read *a, int64_t *end)`, `run_filters(struct archive_read *a)`
    - bug locations: [libarchive/archive_read_support_format_rar.c:2182](https://github.com/libarchive/libarchive/commit/52efa50c69653029687bfc545703b7340b7a51e2#diff-bd382f112c3916f64bb3f057aabe01924a79eba84cf1b391887526a7a91b84e3R2182), [2887](https://github.com/libarchive/libarchive/commit/52efa50c69653029687bfc545703b7340b7a51e2#diff-bd382f112c3916f64bb3f057aabe01924a79eba84cf1b391887526a7a91b84e3R2887), [2913](https://github.com/libarchive/libarchive/commit/52efa50c69653029687bfc545703b7340b7a51e2#diff-bd382f112c3916f64bb3f057aabe01924a79eba84cf1b391887526a7a91b84e3R2913) 
- [seed_corpus.tar](https://drive.google.com/file/d/1JBTngmx-WSt6akqQxMDfML_xVxrpjVXs/view?usp=sharing): initial seed corpus at bug-inducing commit (13 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 13
	- \# seed corpus at fix-inducing commit: 13
- the number of commits between failure-observed commit and BIC: 6

### Bug-ficing commit information
- bug-fixing commit: [1271f775dc917798ad7d03c3b3bd66bacad03603](https://github.com/libarchive/libarchive/commit/1271f775dc917798ad7d03c3b3bd66bacad03603) (20 Feb 2022)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://github.com/libarchive/libarchive/commit/1271f775dc917798ad7d03c3b3bd66bacad03603)
    - changed functions: `run_filters(struct archive_read *a)`
    - fix locations: [libarchive/archive_read_support_format_rar.c:3337-3338](https://github.com/libarchive/libarchive/commit/1271f775dc917798ad7d03c3b3bd66bacad03603#diff-bd382f112c3916f64bb3f057aabe01924a79eba84cf1b391887526a7a91b84e3R3337-R3338) 
- the number of commits between BIC and BFC: 7

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
- failures by other bugs: 6 failures in `other_failures/`
	- [failure1](./other_failures/failure1), [failure2](./other_failures/failure2), [failure3](./other_failures/failure3), [failure4](./other_failures/failrue4), [failure5](./other_failures/failure4), [failure6](./other_failures/failure6)

- target failure
    - type: null-dereference 
    - failure stack trace patterns for the expected failure:  
		```
	run_filters /src/libarchive/libarchive/archive_read_support_format_rar.c:3332:32
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./libarchive_fuzzer failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 13  seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |    no  |
    |   AFL++   |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |    no  |

