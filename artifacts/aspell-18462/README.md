### Failure information on aspell-18462
- OSS-Fuzz issue: [18462](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=18462) (23 Oct 2019) 
- fuzz target: [aspell_fuzzer.cpp](https://github.com/GNUAspell/aspell-fuzz/blob/576059dab2137514bdd236c8189039b557263bd4/aspell_fuzzer.cpp) which is the latest version before the oss-fuzz issue 18462 report time successfully reproduces a reported failure with a bug-revealing input 
    - failure-observed commit: [280d4069f189369ecc49c68b79b6d6cb7f2d6b93](https://github.com/GNUAspell/aspell/commit/280d4069f189369ecc49c68b79b6d6cb7f2d6b93) (10 Oct 2019)
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=5679385310396416
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom
    - type: heap-buffer-overflow
    - stack trace:  
		```
        acommon::ObjStack::dup_top  
        acommon::StringMap::add  
        acommon::Config::lookup_list
		```

### Bug-inducing commit information
- bug-inducing commit: [e0646f9b063b23754951f1254f1ecb7af8ca36f3](https://github.com/GNUAspell/aspell/commit/e0646f9b063b23754951f1254f1ecb7af8ca36f3) (6 Aug 2019)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
        - changed functions: `Config::merge(const Config)`
- [seed_corpus.tar](https://drive.google.com/file/d/1KKD4fYqTXeykiW01_A3B8nDY5rhBHURU/view?usp=share_link): initial seed corpus at bug-inducing commit (2 initial seeds in `seed_corpus/`)
    - seed corpus at the latest [commit](https://github.com/GNUAspell/aspell-fuzz/commit/576059dab2137514bdd236c8189039b557263bd4) before BIC (4 Aug 2019)
        - \# seed corpus at failure-observed commit: 60 
        - \# seed corpus at fix-inducing commit: 60  
- the number of commits between failure-observed commit and BIC: 82

### Bug-fixing commit information
- bug-fixing commit: [0718b375425aad8e54e1150313b862e4c6fd324a](https://github.com/GNUAspell/aspell/commit/0718b375425aad8e54e1150313b862e4c6fd324a) (22 Dec 2019)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://github.com/GNUAspell/aspell/commit/0718b375425aad8e54e1150313b862e4c6fd324a)
    - changed functions: `alloc_bottom(size_t)`, `alloc_top(size_t, size_t)`, `alloc_temp(size_t)`, `resize_temp(size_t)`, `grow_temp(size_t)`
- the number of commits between BIC and BFC: 87

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until FIC
- failures by other bugs: 1 failures in `other_failures/`
    - oss-fuzz issue [16531](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=16531)

- target failure
    - type: heap-buffer-overflow  
    - failure stack trace patterns for the expected failure:  
		```
        acommon::ObjStack::dup_top(acommon::ParmString) /src/aspell/./common/objstack.hpp:95:20  
        acommon::ObjStack::dup(acommon::ParmString) /src/aspell/./common/objstack.hpp:103:38  
        acommon::StringMap::add(acommon::ParmString const&) /src/aspell/./common/string_map.hpp:78:35
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./aspell_fuzzer failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 2 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |    no  |
    |   AFL++   |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |    no  |

