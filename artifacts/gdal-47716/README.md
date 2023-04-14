### Failure information on gdal-47716
- OSS-Fuzz issue: [47716](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=8000) (30 May 2022) 
- fuzz target: [gdal_fuzzer.cpp](https://github.com/OSGeo/gdal/blob/124d1dfe73b91afd09eb05e22019f7a7286761f8/fuzzers/gdal_fuzzer.cpp) which is the latest version before the oss-fuzz issue 47716 report time successfully reproduces a reported failure with a bug-revealing input (30 May 2022)
    - failure-observed commit: [124d1dfe73b91afd09eb05e22019f7a7286761f8 ](https://github.com/OSGeo/gdal/commit/124d1dfe73b91afd09eb05e22019f7a7286761f8) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=5038492226289664
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: heap-buffer-overflow  
    - stack trace:  
		```
        RMFDataset::WriteHeader   
        RMFDataset::FlushCache   
        RMFDataset::~RMFDataset
		```

### Bug-inducing commit information
- bug-inducing commit: [9e2d1f33c9049e925019a3c0c1e6261968a19758](https://github.com/OSGeo/gdal/commit/9e2d1f33c9049e925019a3c0c1e6261968a19758) (28 May 2022)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
	- changed functions: `RMFDataset::FlushCache(bool)`
- [seed_corpus.tar](https://drive.google.com/file/d/1ZpzLUy8mcbzgiAzOCrSEvzAghFA3cx_2/view?usp=share_link): initial seed corpus at bug-inducing commit (1615 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 1615
	- \# seed corpus at fix-inducing commit: 1615
- the number of commits between failure-observed commit and BIC: 7

### Fix-inducing commit information
- fix-inducing commit: [28d9b1ae40fac1faaf78b1f7ea5de7e55ffae360](https://github.com/OSGeo/gdal/commit/28d9b1ae40fac1faaf78b1f7ea5de7e55ffae360) (30 May 2022)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
	- developers explicitly mentioned the bug fixes [here](https://github.com/OSGeo/gdal/commit/28d9b1ae40fac1faaf78b1f7ea5de7e55ffae360)
	- changed functions: `RMFDataset::WriteHeader()`, `RMFDataset::FlushCache(bool)`
- the number of commits between BIC and FIC: 8

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and FIC date, which appears from BIC until FIC
- failures by other bugs: 0 failures

- target failure 
    - type: heap-buffer-overflow  
    - failure stack trace patterns for the expected failure:  
		```
        RMFDataset::WriteHeader() /src/gdal/frmts/rmf/rmfdataset.cpp:990:9  
        RMFDataset::FlushCache(bool) /src/gdal/frmts/rmf/rmfdataset.cpp:1070:5  
        RMFDataset::~RMFDataset() /src/gdal/frmts/rmf/rmfdataset.cpp:766:17
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./gdal_fuzzer failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 4202 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   no  |   no  |   622 | 13592 |  2631 |   no  |   774 |  5106 |   no   |
    |   AFL++   |   255 |   164 |  1408 |   234 |  1851 |  2731 |   239 |  1665 |  3135 |  2635  |

