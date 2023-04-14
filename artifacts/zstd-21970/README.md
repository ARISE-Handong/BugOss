### Failure information on zstd-21970
- OSS-Fuzz issue: [21970](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=21970) (1 May 2020) 
- fuzz target: [stream_decompress.c](https://github.com/facebook/zstd/blob/da2748a855821aa7edc9080997119e44c96d657c/tests/fuzz/stream_decompress.c) which is the latest version before the oss-fuzz issue 21970 report time successfully reproduces a reported failure with a bug-revealing input (1 May 2020)
    - failure-observed commit: [da2748a855821aa7edc9080997119e44c96d657c](https://github.com/facebook/zstd/commit/da2748a855821aa7edc9080997119e44c96d657c) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=5675435464851456
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: null-dereference
    - stack trace:  
		```
		ZSTD_copy16  
		ZSTD_decompressSequences_default  
		ZSTD_decompressBlock_internal 
		```

### Bug-inducing commit information
- bug-inducing commit: [0ed07f6dfe942627e7724e5b910e23ec3cd8ece8](https://github.com/facebook/zstd/commit/0ed07f6dfe942627e7724e5b910e23ec3cd8ece8) (29 Apr 2020)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
	- changed functions: `ERR_getErrorString(ERR_enum)`, `ZSTD_initDCtx_internal(ZSTD_DCtx *)`, `ZSTD_dParam_getBounds(ZSTD_dParameter)`, `ZSTD_DCtx_setParameter(ZSTD_DCtx *, ZSTD_dParameter, int)`, `ZSTD_decompressStream(ZSTD_DStream *, ZSTD_outBuffer *, ZSTD_inBuffer *)`
- [seed_corpus.tar](https://drive.google.com/file/d/1nCL1dTU1PPX-Bha9VJNp-Rekb5oNC5y0/view?usp=share_link): initial seed corpus at bug-inducing commit (12462 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 12462
	- \# seed corpus at fix-inducing commit: 12462
- the number of commits between failure-observed commit and BIC: 4

### Fix-inducing commit information
- fix-inducing commit: [5717bd39ee1bd5d2855023652336deeb722a57d5](https://github.com/facebook/zstd/commit/5717bd39ee1bd5d2855023652336deeb722a57d5) (7 May 2020)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
	- developers explicitly mentioned the bug fixes [here](https://github.com/facebook/zstd/commit/5717bd39ee1bd5d2855023652336deeb722a57d5)
	- changed functions: `XXH64_update_endian(XXH64_state_t *, const void *, size_t, XXH_endianess)`, `ZSTD_execSequenceEnd(BYTE *, BYTE *, seq_t, const BYTE **, const BYTE *, const BYTE *, const BYTE *, const BYTE *, const BYTE *)`, `ZSTD_execSequence(BYTE *, BYTE *, seq_t, const BYTE **, const BYTE *, const BYTE *, const BYTE *, const BYTE *)`, `ZSTD_decompressSequences_body(ZSTD_DCtx *, void *, size_t, const void *, size_t, int, const ZSTD_longOffset_e)`, `ZSTD_decompressSequencesLong_body(ZSTD_DCtx *, void *, size_t, const void *, size_t, int, const ZSTD_longOffset_e)`, `ZSTD_decompressBlock_internal(ZSTD_DCtx *, void *, size_t, const void *, size_t, const int)`, `HUF_decompress_usingDTable(void *, size_t, const void *, size_t, const U16 *)`, `ZSTD_copyUncompressedBlock(void *, size_t, const void *, size_t)`, `ZSTDv01_decodeLiteralsBlock(void *, void *, size_t, const BYTE **, size_t *, const void *, size_t)`, `ZSTD_decompressSequences(void *, void *, size_t, const void *, size_t, const BYTE *, size_t)`, `ZSTD_copyUncompressedBlock(void *, size_t, const void *, size_t)`, `ZSTD_decompressSequences(void *, void *, size_t, const void *, size_t)`, `ZSTD_copyUncompressedBlock(void *, size_t, const void *, size_t)`, `ZSTD_decompressSequences(void *, void *, size_t, const void *, size_t)`, `ZSTD_copyRawBlock(void *, size_t, const void *, size_t)`, `ZSTD_decompressSequences(ZSTD_DCtx *, void *, size_t, const void *, size_t)`, `ZSTDv05_decompressSequences(ZSTDv05_DCtx *, void *, size_t, const void *, size_t)`, `ZSTDv06_decompressSequences(ZSTDv06_DCtx *, void *, size_t, const void *, size_t)`, `ZSTDv07_copyRawBlock(void *, size_t, const void *, size_t)`, `ZSTDv07_decompressSequences(ZSTDv07_DCtx *, void *, size_t, const void *, size_t)`, `ZSTDv07_generateNxBytes(void *, size_t, BYTE, size_t)`
- the number of commits between BIC and FIC: 53 

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and FIC date, which appears from BIC until FIC
- failures by other bugs: 0 failures 

- target failure 
    - type: null-dereference 
    - failure stack trace patterns for the expected failure:  
		```
		ZSTD_copy16 /src/zstd/tests/fuzz/../../lib/common/zstd_internal.h:199:55
		ZSTD_execSequence /src/zstd/tests/fuzz/../../lib/decompress/zstd_decompress_block.c:731:5
		ZSTD_decompressSequences_body /src/zstd/tests/fuzz/../../lib/decompress/zstd_decompress_block.c:1020:39
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./stream_decompress failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 12462 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |  2140 |   248 |  1404 |  2034 |  2135 |  2359 |  1206 |   293 |   595 |    140 |
    |   AFL++   |   548 |   349 |   913 |   462 |   339 |   445 |   775 |   443 |   517 |    549 |

