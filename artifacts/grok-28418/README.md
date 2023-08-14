### Failure information on grok-28418 
- OSS-Fuzz issue: [28418](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=28418) (8 Dec 2020) 
- fuzz target: [grk_decompress_fuzzer.cpp](https://github.com/GrokImageCompression/grok/blob/2b2f0e892c47c7b65b5c55ebf92ad77ff1dc14f3/tests/fuzzers/grk_decompress_fuzzer.cpp) which is the latest version before the oss-fuzz issue 28418 report time successfully reproduces a reported failure with a bug-revealing input (8 Dec 2020)
    - failure-observed commit: [2b2f0e892c47c7b65b5c55ebf92ad77ff1dc14f3](https://github.com/GrokImageCompression/grok/commit/2b2f0e892c47c7b65b5c55ebf92ad77ff1dc14f3) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=6170881403518976
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: direct-leak 
    - stack trace:  
		```
	        grk::PacketIter::get_include   
		grk::pi_next   
		grk::T2Decompress::decompress_packets
		```

### Bug-inducing commit information
- bug-inducing commit: [93e6af95ec46bbba5e112a1fbdbdb6a1294d61d8](https://github.com/GrokImageCompression/grok/commit/93e6af95ec46bbba5e112a1fbdbdb6a1294d61d8) (7 Dec 2020)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `pi_next_lrcp(PacketIter *)`, `pi_next_rlcp(PacketIter *)`, `pi_next_rpcl(PacketIter *)`, `pi_next_pcrl(PacketIter *)`, `pi_next_pcrl(PacketIter *)`, `pi_next_cprl(PacketIter *)`, `pi_create_decompress(grk_image *, CodingParams *, uint16_t)`, `pi_create_compress(const grk_image *, CodingParams *, uint16_t, J2K_T2_MODE)`, `pi_destroy(PacketIter *)`, `T2Decompress::decompress_packets(uint16_t, ChunkBuffer *, uint64_t *)`
    - bug locations: [src/lib/jp2/codestream/PacketIter.cpp:924-927](https://github.com/GrokImageCompression/grok/commit/93e6af95ec46bbba5e112a1fbdbdb6a1294d61d8#diff-d3dc197db944ac5e717f0d776f5aaff7157ab7b1b22540ecdfadf0facc245d26L924-L928), [1052-1055](https://github.com/GrokImageCompression/grok/commit/93e6af95ec46bbba5e112a1fbdbdb6a1294d61d8#diff-d3dc197db944ac5e717f0d776f5aaff7157ab7b1b22540ecdfadf0facc245d26L1052-L1056) 
- [seed_corpus.tar](https://drive.google.com/file/d/12hsa8mJkrYwSQovBUVWzS1U7KoHZYFE2/view?usp=share_link): initial seed corpus at bug-inducing commit (178 initial seeds in `seed_corpus/`)
    - seed corpus at the latest [commit](https://github.com/GrokImageCompression/grok-test-data/commit/5118df38d89d26949c82d9143c74d80656781089) before BIC  (1 Dec 2020)
		- `input/conformance/*.jp2`, `input/conformance/*.j2k`, `input/nonregression/*.jp2`, `input/nonregression/*.j2k`
	- \# seed corpus at failure-observed commit: 178 
	- \# seed corpus at fix-inducing commit: 178
- the number of commits between failure-observed commit and BIC: 1

### Bug-fixing commit information
- bug-fixing commit: [1cb27625e7237a1a03a1c9ad67bc1f006473aa35](https://github.com/GrokImageCompression/grok/commit/1cb27625e7237a1a03a1c9ad67bc1f006473aa35) (8 Dec 2020)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://github.com/GrokImageCompression/grok/commit/1cb27625e7237a1a03a1c9ad67bc1f006473aa35)
    - changed functions: `pi_create(const grk_image *, const CodingParams *, uint16_t, std::vector<uint8_t*> *)`, `pi_create_decompress(grk_image *, CodingParams *, uint16_t, std::vector<uint8_t*> *)`, `pi_create_compress(const grk_image *, CodingParams *, uint16_t, J2K_T2_MODE, std::vector<uint8_t*> *)`, `get_include(uint16_t)`, `update_include(void)`, `destroy_include(void)`, `T2Compress:compress_packets(uint16_t, uint16_t, BufferedStream *, uint32_t *, bool, uint32_t,	uint32_t)`, `T2Compress::compress_packets_simulate(uint16_t, uint16_t, uint32_t *, uint32_t, uint32_t, PacketLengthMarkers *)`, `T2Decompress:decompress_packets((uint16_t, ChunkBuffer *, uint64_t *)`
    - fix locations: [src/lib/jp2/t2/T2Decompress.cpp:40-41](https://github.com/GrokImageCompression/grok/commit/93e6af95ec46bbba5e112a1fbdbdb6a1294d61d8#diff-d3dc197db944ac5e717f0d776f5aaff7157ab7b1b22540ecdfadf0facc245d26L1052-L1056) 
- the number of commits between BIC and BFC: 3 

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
- failures by other bugs: 36 failures in `other_failures/`
    - failures detected by AFL++ for 48 hours on a clean version (i.e., commit right before BIC)
		- 36 failures are collected

- target failure 
    - type: heap-buffer-overflow  
    - failure stack trace patterns for the expected failure:  
		```
		grk::PacketIter::get_include(unsigned short) /src/grok/src/lib/jp2/codestream/PacketIter.cpp:1447:14  
		grk::PacketIter::update_include() /src/grok/src/lib/jp2/codestream/PacketIter.cpp:1459:17  
		grk::pi_next(grk::PacketIter*) /src/grok/src/lib/jp2/codestream/PacketIter.cpp:1414:11  
		grk::T2Decompress::decompress_packets(unsigned short, grk::ChunkBuffer*, unsigned long*) /src/grok/src/lib/jp2/t2/T2Decompress.cpp:71:10
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./grk_decompress_fuzzer failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 178 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  | 12698 |   no  |   no  |   no  |   no  |   no  | 17039 |   no  |    no  |
    |   AFL++   |   no  |   no  |   no  | 13671 | 18918 |   no  |   no  |   no  |   no  |   764  |

