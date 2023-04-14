### Failure information on libxml2-17737
- OSS-Fuzz issue: [17737](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=17737) (26 Sep 2019) 
- fuzz target: [libxml2_xml_reader_for_file_fuzzer.cc](https://github.com/google/oss-fuzz/blob/16125ac2bce61d29aa5e418444dd328a555c3d90/projects/libxml2/libxml2_xml_reader_for_file_fuzzer.cc) which is the latest version before the oss-fuzz issue 17737 report time successfully reproduces a reported failure with a bug-revealing input (25 Sep 2019)
    - failure-observed commit: [99a864a1f7a9cb59865f803770d7d62fb47cad69](https://gitlab.gnome.org/GNOME/libxml2/-/commit/99a864a1f7a9cb59865f803770d7d62fb47cad69) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=5654854260752384
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: heap-use-after-free
    - stack trace:  
		```
		xmlTextReaderFreeNodeList  
		xmlTextReaderFreeDoc  
		xmlFreeTextReader 
		```

### Bug-inducing commit information
- bug-inducing commit: [1fbcf4098ba2aefe241de8d7ceb229b995d8daec](https://gitlab.gnome.org/GNOME/libxml2/-/commit/1fbcf4098ba2aefe241de8d7ceb229b995d8daec) (24 Sep 2019)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
	- changed functions: `xmlTextReaderFreeNodeList(xmlTextReaderPtr, xmlNodePtr)`
- [seed_corpus.tar](https://drive.google.com/file/d/1NadtWdMNOIzo0uUIFrxOTu5ZhTtMbXfD/view?usp=share_link): initial seed corpus at bug-inducing commit (1274 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 1275 
	- \# seed corpus at fix-inducing commit: 1308
- the number of commits between failure-observed commit and BIC: 1

### Fix-inducing commit information
- fix-inducing commit: [664f881008f40356c0502c8cc154e17e3c80e353](https://gitlab.gnome.org/GNOME/libxml2/-/commit/664f881008f40356c0502c8cc154e17e3c80e353) (26 Sep 2019)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
	- developers explicitly mentioned the bug fixes [here](https://gitlab.gnome.org/GNOME/libxml2/-/commit/664f881008f40356c0502c8cc154e17e3c80e353)
	- changed functions: `xmlTextReaderFreeNodeList(xmlTextReaderPtr, xmlNodePtr)`
- the number of commits between BIC and FIC: 2 

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and FIC date, which appears from BIC until FIC
- failures by other bugs: 94 failures in `other_failures/`
    - failures detected by AFL++ for 48 hours on a clean version (i.e., commit right before BIC)
		- 94 failures are collected

- target failure  
    - type: heap-use-after-free 
    - failure stack trace patterns for the expected failure:  
		```
		xmlTextReaderFreeNodeList /src/libxml2/xmlreader.c:371:32  
		xmlTextReaderFreeDoc /src/libxml2/xmlreader.c:565:32  
		xmlFreeTextReader /src/libxml2/xmlreader.c:2294:3
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./libxml2_xml_reader_for_file_fuzzer failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 1274 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   462 |  2655 |   no  |  9504 |   no  |   13  |  1321 |   no  |  2261  |
    |   AFL++   |   59  |   183 |   263 |   235 |   225 |   310 |   112 |  1208 |   310 |    49  |
