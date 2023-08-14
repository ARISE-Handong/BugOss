### Failure information on harfbuzz-55779
- OSS-Fuzz issue: [55779](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=55779) (8 Feb 2023) 
- fuzz target: [hb-shape-fuzzer.cc](https://github.com/harfbuzz/harfbuzz/blob/8708b9e081192786c027bb7f5f23d76dbe5c19e8/test/fuzzing/hb-shape-fuzzer.cc) which is the latest version before the oss-fuzz issue 55779 report time successfully reproduces a reported failure with a bug-revealing input 
    - failure-observed commit: [3fd9311649e2e0e5e2bfbe27c082e3f2dbc797f5](https://github.com/harfbuzz/harfbuzz/commit/3fd9311649e2e0e5e2bfbe27c082e3f2dbc797f5) (8 Feb 2023)
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=6377756666757120  
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom
    - type: assert-violation
    - stack trace:  
	```
	j < i
	OT::Layout::propagate_attachment_offsets
	OT::Layout::GPOS::position_finish_offsets
	```

### Bug-inducing commit information
- bug-inducing commit: [8708b9e081192786c027bb7f5f23d76dbe5c19e8](https://github.com/harfbuzz/harfbuzz/commit/8708b9e081192786c027bb7f5f23d76dbe5c19e8) (7 Feb 2023)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `OT::Layout::GPOS_impl::MarkLigPosFormat1_2::apply`, `OT::Layout::GPOS_impl::MarkBasePosFormat1_2::apply`, `set_lookup_mask`
    - bug locations:  
        - [src/OT/Layout/GPOS/MarkBasePosFormat1.hh:129](https://github.com/harfbuzz/harfbuzz/commit/8708b9e081192786c027bb7f5f23d76dbe5c19e8#diff-606f88c7b3fb0f49f015411db16a62f80c757c2fac9c606219ca27ef3ab835c1R129), [131-132](https://github.com/harfbuzz/harfbuzz/commit/8708b9e081192786c027bb7f5f23d76dbe5c19e8#diff-606f88c7b3fb0f49f015411db16a62f80c757c2fac9c606219ca27ef3ab835c1R131-R132), [134-137](https://github.com/harfbuzz/harfbuzz/commit/8708b9e081192786c027bb7f5f23d76dbe5c19e8#diff-606f88c7b3fb0f49f015411db16a62f80c757c2fac9c606219ca27ef3ab835c1R134-R137) 
        - [src/OT/Layout/GPOS/MarkLigPosFormat1.hh:111-114](https://github.com/harfbuzz/harfbuzz/commit/8708b9e081192786c027bb7f5f23d76dbe5c19e8#diff-9aec5b7fd9f8ab5736a77e346514a79a2e4463f15ecaa5e31ebf101d96f1b85dR111-R114), [118](https://github.com/harfbuzz/harfbuzz/commit/8708b9e081192786c027bb7f5f23d76dbe5c19e8#diff-9aec5b7fd9f8ab5736a77e346514a79a2e4463f15ecaa5e31ebf101d96f1b85dR118) 
- [seed_corpus.tar](https://drive.google.com/file/d/15LtQxf0nTr-zddufXYYEyqnUsjLlLFzF/view?usp=sharing): initial seed corpus at bug-inducing commit (1003 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 1003 
	- \# seed corpus at fix-inducing commit: 1004
- the number of commits between failure-observed commit and BIC: 6  

### Bug-ficing commit information
- bug-fixing commit: [64fa5cd482d0be2e215998aa1c2a05b978133e7c](https://github.com/harfbuzz/harfbuzz/commit/64fa5cd482d0be2e215998aa1c2a05b978133e7c) (8 Feb 2023)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://github.com/harfbuzz/harfbuzz/commit/64fa5cd482d0be2e215998aa1c2a05b978133e7c)
    - changed functions: `OT::Layout::GPOS_impl::MarkLigPosFormat1_2::apply`, `OT::Layout::GPOS_impl::MarkBasePosFormat1_2::apply`
    - fix locations: 
        - [src/OT/Layout/GPOS/MarkBasePosFormat1.hh:125-129](https://github.com/harfbuzz/harfbuzz/commit/64fa5cd482d0be2e215998aa1c2a05b978133e7c#diff-606f88c7b3fb0f49f015411db16a62f80c757c2fac9c606219ca27ef3ab835c1R125-R129)  
        - [src/OT/Layout/GPOS/MarkLigPosFormat1.hh:107-111](https://github.com/harfbuzz/harfbuzz/commit/64fa5cd482d0be2e215998aa1c2a05b978133e7c#diff-9aec5b7fd9f8ab5736a77e346514a79a2e4463f15ecaa5e31ebf101d96f1b85dR107-R111) 
- the number of commits between BIC and BFC: 13  

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
- failures by other bugs: 0 failure 

- target failure
    - type: assert-violation  
    - crash message: ../../src/harfbuzz/src/OT/Layout/GPOS/GPOS.hh:113: void OT::Layout::propagate_attachment_offsets(hb_glyph_position_t *, unsigned int, unsigned int, hb_direction_t, unsigned int): Assertion `j < i' failed. 
    - failure stack trace patterns for the expected failure:  
		```
		raise /build/glibc-sMfBJT/glibc-2.31/signal/../sysdeps/unix/sysv/linux/raise.c:51:1
		abort /build/glibc-sMfBJT/glibc-2.31/stdlib/abort.c:79:7
		__assert_fail_base /build/glibc-sMfBJT/glibc-2.31/assert/assert.c:92:3
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./hb-shape-fuzzer failing-input 2> exec_result
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

