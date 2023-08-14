### Failure information on libhtp-17198
- OSS-Fuzz issue: [17198](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=17198) (15 Sep 2019) 
- fuzz target: [fuzz_htp.c](https://github.com/OISF/libhtp/blob/75cbbbd405695e97567931655fd5a441f86e5836/test/fuzz/fuzz_htp.c) which is the latest version before the oss-fuzz issue 17198 report time successfully reproduces a reported failure with a bug-revealing input (14 Sep 2019)
    - failure-observed commit: [75cbbbd405695e97567931655fd5a441f86e5836](https://github.com/OISF/libhtp/commit/75cbbbd405695e97567931655fd5a441f86e5836) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=5659352148475904
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: heap-buffer-overflow  
    - stack trace:  
		```
		LzmaDec_DecodeToDic   
		LzmaDec_DecodeToBuf  
		htp_gzip_decompressor_decompress
		```

### Bug-inducing commit information
- bug-inducing commit: [3c6555078ec30e0baa4855ec69d55a22fc8d3589](https://github.com/OISF/libhtp/commit/3c6555078ec30e0baa4855ec69d55a22fc8d3589) (13 Sep 2019)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `LzmaDec_DecodeToBuf(CLzmaDec *, Byte *, SizeT *, const Byte *, SizeT *, ELzmaFinishMode, ELzmaStatus *)`, `LzmaDec_Allocate(CLzmaDec *, const Byte *, unsigned, ISzAllocPtr)`
    - bug locations: [htp/lzma/LzmaDec.c:1034-1051](https://github.com/OISF/libhtp/commit/3c6555078ec30e0baa4855ec69d55a22fc8d3589#diff-f7316cfca3a599b2f152594caabbef1f2f80c8d4ede71b11e6222ace3f20e629R1034-R1051) 
- [seed_corpus.tar](https://drive.google.com/file/d/1Mc36cDr5PvIUfSf9oN6SqwlqZYTPicbM/view?usp=share_link): initial seed corpus at bug-inducing commit (97 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 97
	- \# seed corpus at fix-inducing commit: 97
- the number of commits between failure-observed commit and BIC: 2

### Bug-fixing commit information
- bug-fixing commit: [fe16fa764f7cea57be5a288ee85b27dffc460f6f](https://github.com/OISF/libhtp/commit/fe16fa764f7cea57be5a288ee85b27dffc460f6f) (17 Sep 2019)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - reference \[[AFLChurn, CCS'21](https://dl.acm.org/doi/abs/10.1145/3460120.3484596)\]
    - changed functions: `LzmaDec_DecodeReal2(CLzmaDec *, SizeT, const Byte *, SizeT)`, `LzmaDec_DecodeToDic(CLzmaDec *, SizeT, const Byte *, SizeT *, ELzmaFinishMode, ELzmaStatus *, SizeT)`, `LzmaDec_DecodeToBuf`, `LzmaDec_Allocate(CLzmaDec *, const Byte *, unsigned, ISzAllocPtr)`, `LzmaDecode(Byte *, SizeT *, const Byte *, SizeT *, const Byte *, unsigned, ELzmaFinishMode, ELzmaStatus *, ISzAllocPtr)`
    - fix locations: [htp/lzma/LzmaDec.c:980](https://github.com/OISF/libhtp/commit/fe16fa764f7cea57be5a288ee85b27dffc460f6f#diff-f7316cfca3a599b2f152594caabbef1f2f80c8d4ede71b11e6222ace3f20e629R980), [1009](https://github.com/OISF/libhtp/commit/fe16fa764f7cea57be5a288ee85b27dffc460f6f#diff-f7316cfca3a599b2f152594caabbef1f2f80c8d4ede71b11e6222ace3f20e629R1009), [1078](https://github.com/OISF/libhtp/commit/fe16fa764f7cea57be5a288ee85b27dffc460f6f#diff-f7316cfca3a599b2f152594caabbef1f2f80c8d4ede71b11e6222ace3f20e629R1078), [1215](https://github.com/OISF/libhtp/commit/fe16fa764f7cea57be5a288ee85b27dffc460f6f#diff-f7316cfca3a599b2f152594caabbef1f2f80c8d4ede71b11e6222ace3f20e629R1215) 
- the number of commits between BIC and BFC: 3 

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
- failures by other bugs: 0 failures 

- target failure 
    - type: heap-buffer-overflow  
    - failure stack trace patterns for the expected failure:  
		```
		LzmaDec_WriteRem /src/libhtp/htp/lzma/LzmaDec.c:610:21  
		LzmaDec_DecodeToDic /src/libhtp/htp/lzma/LzmaDec.c:917:3  
		LzmaDec_DecodeToBuf /src/libhtp/htp/lzma/LzmaDec.c:1066:11
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./fuzz_htp failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 97 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |  198  |  8213 |   no  |   no  |  7471 | 16465 |  2986 |   no  |  5319 |  1911  |
    |   AFL++   |  385  |   461 |   588 |   660 |   761 |    98 |   242 |   200 |   205 |   483  |

