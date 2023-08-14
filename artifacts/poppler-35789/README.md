### Failure information on poppler-35789
- OSS-Fuzz issue: [35789](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=35789) (4 Jul 2021) 
- fuzz target: [label_fuzzer.cc](https://gitlab.freedesktop.org/poppler/poppler/-/blob/77e545351b7ac359e19422e8158ff00f6dd597d3/glib/tests/fuzzing/label_fuzzer.cc) which is the latest version before the oss-fuzz issue 35789 report time successfully reproduces a reported failure with a bug-revealing input (3 Jul 2021)
    - failure-observed commit: [77e545351b7ac359e19422e8158ff00f6dd597d3](https://gitlab.freedesktop.org/poppler/poppler/-/commit/77e545351b7ac359e19422e8158ff00f6dd597d3) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=6191316215136256
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: null-dereference 
    - stack trace:  
		```
		JBIG2SymbolDict::setBitmap  
		JBIG2Stream::readSymbolDictSeg  
		JBIG2Stream::readSegments
		```

### Bug-inducing commit information
- bug-inducing commit: [2b2808719d2c91283ae358381391bb0b37d9061d](https://gitlab.freedesktop.org/poppler/poppler/-/commit/2b2808719d2c91283ae358381391bb0b37d9061d) (2 Jul 2021)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `isOk(void)`, `JBIG2Stream::readSegments(void)`
    - bug locations: [poppler/JBIC2Stream.cc:970](https://gitlab.freedesktop.org/poppler/poppler/-/commit/2b2808719d2c91283ae358381391bb0b37d9061d#f620460273a22459b3b2454ed648695f6c0cfe49_971_970) 
- [seed_corpus.tar](https://drive.google.com/file/d/1N-oMQ-a3UyxZ-BReLxsw5foGnpiZ5woM/view?usp=share_link): initial seed corpus at bug-inducing commit (476 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 476
	- \# seed corpus at fix-inducing commit: 476
- the number of commits between failure-observed commit and BIC: 1

### Bug-fixing commit information
- bug-fixing commit: [f2a6c6fe06ba2279f8509c56a11d649f02d1500c ](https://gitlab.freedesktop.org/poppler/poppler/-/commit/f2a6c6fe06ba2279f8509c56a11d649f02d1500c) (5 Jul 2021)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://gitlab.freedesktop.org/poppler/poppler/-/commit/f2a6c6fe06ba2279f8509c56a11d649f02d1500c)
    - changed functions: `isOk(void)`, `JBIG2SymbolDict::JBIG2SymbolDict(unsigned int, unsigned int)`
    - fix locations: [poppler/JBIG2Stream.cc:970](https://gitlab.freedesktop.org/poppler/poppler/-/commit/f2a6c6fe06ba2279f8509c56a11d649f02d1500c#f620460273a22459b3b2454ed648695f6c0cfe49_971_970), [977](https://gitlab.freedesktop.org/poppler/poppler/-/commit/f2a6c6fe06ba2279f8509c56a11d649f02d1500c#f620460273a22459b3b2454ed648695f6c0cfe49_977_977), [988-995](https://gitlab.freedesktop.org/poppler/poppler/-/commit/f2a6c6fe06ba2279f8509c56a11d649f02d1500c#f620460273a22459b3b2454ed648695f6c0cfe49_992_988) 
- the number of commits between BIC and BFC: 4

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
- failures by other bugs: 0 failures 

- target failure 
    - type: null-dereference 
    - failure stack trace patterns for the expected failure:  
		```
		JBIG2SymbolDict::setBitmap(unsigned int, JBIG2Bitmap*) /src/poppler/poppler/JBIG2Stream.cc:968:74  
		JBIG2Stream::readSymbolDictSeg(unsigned int, unsigned int, unsigned int*, unsigned int) /src/poppler/poppler/JBIG2Stream.cc:1840:25  
		JBIG2Stream::readSegments() /src/poppler/poppler/JBIG2Stream.cc:1331:18
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./label_fuzzer failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 476 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |    no  |
    |   AFL++   | 18510 | 21062 | 10804 |  8768 |  7870 |  6439 |  8176 |  4270 | 11148 |    no  |

