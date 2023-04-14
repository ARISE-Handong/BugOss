### Failure information on curl-8000
- OSS-Fuzz issue: [8000](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=8000) (25 Apr 2018) 
- fuzz target: [curl_fuzzer.cc](https://github.com/curl/curl-fuzzer/blob/c4ce63bf55674cebdad03f8bb6adb354bfc63609/curl_fuzzer.cc) which is the latest version before the oss-fuzz issue 8000 report time successfully reproduces a reported failure with a bug-revealing input (25 Apr 2018)
    - failure-observed commit: [ba67f7d65a42e63eccfe0bcc87f82682d6e4cc9e](https://github.com/curl/curl/commit/ba67f7d65a42e63eccfe0bcc87f82682d6e4cc9e) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=6221983296520192
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: heap-buffer-overflow 
    - stack trace:  
		```
        concat_url   
        Curl_follow  
        multi_runsingle 
		```

### Bug-inducing commit information
- bug-inducing commit: [dd7521bcc1b7a6fcb53c31f9bd1192fcc884bd56](https://github.com/curl/curl/commit/dd7521bcc1b7a6fcb53c31f9bd1192fcc884bd56) (24 Apr 2018)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
	- changed functions: `Curl_httpchunk_read(connectdata *, char *, ssize_t, ssize_t *)`, `strcpy_url(char *, const char *, bool)`
- [seed_corpus.tar](https://drive.google.com/file/d/1onSquIuVxm2GLWHjGRi2EDZehqTRNolI/view?usp=share_link): initial seed corpus at bug-inducing commit (4202 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 4202
	- \# seed corpus at fix-inducing commit: 4202
- the number of commits between failure-observed commit and BIC: 0
	- BIC is a commit right before failure-observed commit

### Fix-inducing commit information
- fix-inducing commit: [3c630f9b0af097663a64e5c875c580aa9808a92b](https://github.com/curl/curl/commit/3c630f9b0af097663a64e5c875c580aa9808a92b) (25 Apr 2018)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
	- developers explicitly mentioned the bug fixes [here](https://github.com/curl/curl/commit/3c630f9b0af097663a64e5c875c580aa9808a92b)
	- changed functions: `strcpy_url(char *, const char *, bool)`
- the number of commits between BIC and FIC: 1

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and FIC date, which appears from BIC until FIC
- failures by other bugs: 0 failures

- target failure symptom
    - type: heap-buffer-overflow  
    - failure stack trace patterns for the expected failure:  
		```
        strcpy_url /src/curl/lib/transfer.c:1540:9  
        concat_url /src/curl/lib/transfer.c:1707:3  
        Curl_follow /src/curl/lib/transfer.c:1771:22
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./curl_fuzzer failing-input 2> exec_result
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
    | libFuzzer |  8731 | 12068 |  2470 | 13098 |   582 |  8593 |  1677 |  5190 |  5191 |  1414  |
    |   AFL++   |  1242 |  1241 |  1247 |  1251 |  1272 |  1184 |  1242 |  1233 |  1249 |  1238  |

