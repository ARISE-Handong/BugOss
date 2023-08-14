### Failure information on arrow-40653
- OSS-Fuzz issue: [40653](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=40653) (3 Nov 2021) 
- fuzz target: [arrow-ipc-file-fuzz](https://github.com/apache/arrow/blob/3c5b62c116733e434508a8673c2d466776b27eed/cpp/src/arrow/ipc/file_fuzz.cc) which is the latest version before the oss-fuzz issue 40653 report time successfully reproduces a reported failure with a bug-revealing input 
    - failure-observed commit: [bf67ec74635db2183619601f025e4724bd5a6b75](https://github.com/apache/arrow/commit/bf67ec74635db2183619601f025e4724bd5a6b75) (3 Nov 2021)
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=6318558565498880
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom
    - type: abort
    - stack trace:  
		```
	arrow::util::CerrLog::~CerrLog
	arrow::util::ArrowLog::~ArrowLog
	arrow::MapArray::SetData
		```

### Bug-inducing commit information
- bug-inducing commit: [3c5b62c116733e434508a8673c2d466776b27eed](https://github.com/apache/arrow/commit/3c5b62c116733e434508a8673c2d466776b27eed) (7 Oct 2021)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `arrow::ipc::internal::FuzzIpcStream(const uint8_t* data, int64_t size)`, `arrow::ipc::internal::FuzzIpcFile(const uint8_t* data, int64_t size)`
    - bug locations: [cpp/src/arrow/ipc/reader.cc:2029](https://github.com/apache/arrow/commit/3c5b62c116733e434508a8673c2d466776b27eed#diff-e992169684aea9845ac776ada4cbb2b5dc711b49e5a3fbc6046c92299e1aefceR2029), [2053](https://github.com/apache/arrow/commit/3c5b62c116733e434508a8673c2d466776b27eed#diff-e992169684aea9845ac776ada4cbb2b5dc711b49e5a3fbc6046c92299e1aefceR2053), [2070](https://github.com/apache/arrow/commit/3c5b62c116733e434508a8673c2d466776b27eed#diff-e992169684aea9845ac776ada4cbb2b5dc711b49e5a3fbc6046c92299e1aefceR2070) 
- [seed_corpus.tar](https://drive.google.com/file/d/1DLAkdxn2gdPfiyznsrpgkOGSLeKn4jZT/view?usp=sharing): initial seed corpus at bug-inducing commit (10 initial seeds in `seed_corpus/`)
    - seed corpus at the latest [commit](https://github.com/apache/arrow/commit/3c5b62c116733e434508a8673c2d466776b27eed) at BIC (7 Oct 2021)
	- \# seed corpus at failure-observed commit: XX 
	- \# seed corpus at fix-inducing commit: 10
- the number of commits between failure-observed commit and BIC: 206 

### Bug-fixing commit information
- bug-fixing commit: [fdc6a79b1028c8dae086ccba1cd6ce9f66f90fcb](https://github.com/apache/arrow/commit/fdc6a79b1028c8dae086ccba1cd6ce9f66f90fcb) (5 Nov 2021)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://github.com/apache/arrow/commit/fdc6a79b1028c8dae086ccba1cd6ce9f66f90fcb)
    - changed functions: `value_offset(int64_t i)`, `Visit(const MapType& type)`, `FixedSizeListValueLength(KernelContext* ctx, const ExecBatch& batch, Datum* out)`, `Visit(const FixedSizeListType& type)`, `ListParentIndicesType(const DataType& input_type)`
    - fix locations: [cpp/src/arrow/array/validate.cc:79-80](https://github.com/apache/arrow/commit/fdc6a79b1028c8dae086ccba1cd6ce9f66f90fcb#diff-609d8dec95e35837ef36ce0b467e1d9fa15c19cf5a2d820b736d522e8def1db1R79-R80)  
- the number of commits between BIC and BFC: 230

### Failure samples
- failure by a target bug: 2 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
- failures by other bugs: 4 failures in `other_failures/`
	- oss-fuzz issue [39677](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=39677), [39703](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=39703), [39763](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=39763), [39773](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=39773) 

- target failure
    - type: abort 
    - failure stack trace patterns for the expected failure:  
		```
	__sanitizer_print_stack_trace  
	fuzzer::PrintStackTrace()  
	fuzzer::Fuzzer::CrashCallback()  
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./arrow-ipc-file-fuzz failing-input 2> exec_result
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

