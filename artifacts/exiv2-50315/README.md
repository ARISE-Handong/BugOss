### Failure information on exiv2-50315 
- OSS-Fuzz issue: [50315](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=50315) (17 Aug 2022) 
- fuzz target: [fuzz-read-print-write.cpp](https://github.com/Exiv2/exiv2/blob/88fcd234bbb5e3fca03171b81c8d0e84b2619b26/fuzz/fuzz-read-print-write.cpp) which is the latest version before the oss-fuzz issue 50315 report time successfully reproduces a reported failure with a bug-revealing input (17 Aug 2022)
    - failure-observed commit: [88fcd234bbb5e3fca03171b81c8d0e84b2619b26](https://github.com/Exiv2/exiv2/commit/88fcd234bbb5e3fca03171b81c8d0e84b2619b26)
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=5011915578933248 
- sanitizer: undefined
    - `$CFLAGS -fsanitize=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unsigned-integer-overflow,unreachable,vla-bound,vptr -fno-sanitize-recover=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unreachable,vla-bound,vptr`
    - `$CXXFLAGS -fsanitize=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unsigned-integer-overflow,unreachable,vla-bound,vptr -fno-sanitize-recover=array-bounds,bool,builtin,enum,float-divide-by-zero,function,integer-divide-by-zero,null,object-size,return,returns-nonnull-attribute,shift,signed-integer-overflow,unreachable,vla-bound,vptr`
- reported failure symptom 
    - type: integer-overflow 
    - stack trace:  
		```
        Exiv2::floatToRationalCast   
        Exiv2::Internal::printDegrees   
        Exiv2::Exifdatum::write
		```

### Bug-inducing commit information
- bug-inducing commit: [10a62b23500954abf7eb2cc3e577bebb21bb0b72](https://github.com/Exiv2/exiv2/commit/10a62b23500954abf7eb2cc3e577bebb21bb0b72) (16 Aug 2022)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
	- changed functions: `gcd(IntType, IntType)`, `print0x9204(std::ostream, const Value, const ExifData *)`, `floatToRationalCast(float)`
- [seed_corpus.tar](https://drive.google.com/file/d/171Y1RVFmlhelQwRDNwI8Spdi0axqZ4Aa/view?usp=share_link): initial seed corpus at bug-inducing commit (454 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 454
	- \# seed corpus at fix-inducing commit: 460
- the number of commits between failure-observed commit and BIC: 1

### Bug-fixinging commit information
- bug-fixing commit: [7a92e1bd0f8a1435eed7743e3aeadcb73f63182d](https://github.com/Exiv2/exiv2/commit/7a92e1bd0f8a1435eed7743e3aeadcb73f63182d) (29 Aug 2022)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://github.com/Exiv2/exiv2/commit/7a92e1bd0f8a1435eed7743e3aeadcb73f63182d)
    - changed functions: `floatToRationalCast(float)`
- the number of commits between BIC and BFC: 18

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
- failures by other bugs: 13 failures in `other_failures/`
    - failures detected by AFL++ for 48 hours on a clean version (i.e., commit right before BIC)
		- [failure1](./other_failures/failure1), [failure2](./other_failures/failure2), [failure3](./other_failures/failure3), [failure4](./other_failures/failure4), [failure5](./other_failures/failure5), [failure6](./other_failures/failure6), [failure7](./other_failures/failure7), [failure8](./other_failures/failure8), [failure9](./other_failures/failure9), [failure10](./other_failures/failure10), [failure11](./other_failures/failure11), [failure12](./other_failures/failure12), [failure13](./other_failures/failure13)

- target failure  
    - type: integer-overflow
    - crash message: /usr/local/bin/../include/c++/v1/numeric:517:59: runtime error: negation of -2147483648 cannot be represented in type 'int'; cast to an unsigned type to negate this value to itself 
    - failure stack trace patterns for the expected failure:  
		```
        gcd<int, int> /usr/local/bin/../include/c++/v1/numeric:549:26  
        Exiv2::floatToRationalCast(float) /src/exiv2/src/types.cpp:633:21  
        Exiv2::Internal::printDegrees(std::__1::basic_ostream<char, std::__1::char_traits<char> >&, Exiv2::Value const&, Exiv2::ExifData const*) /src/exiv2/src/tags_int.cpp:2515:26
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	UBSAN_OPTIONS=print_stacktrace=1 
	./fuzz-read-print-write failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 454 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no   |
    |   AFL++   |   no  | 21275 |   no  |   no  |   no  |  1615 |   no  |   no  |   no  |   no   |

