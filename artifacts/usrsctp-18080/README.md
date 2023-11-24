### Failure information on usrsctp-18080
- OSS-Fuzz issue: [18080](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=18080) (9 Oct 2019) 
- fuzz target: [fuzzer_connect.c](https://github.com/sctplab/usrsctp/blob/1ab1d69ce8cbf20a4d0d1e41de6b5c11cd24da71/fuzzer/fuzzer_connect.c) which is the latest version before the oss-fuzz issue 18080 report time successfully reproduces a reported failure with a bug-revealing input (8 Oct 2019)
    - failure-observed commit: [1ab1d69ce8cbf20a4d0d1e41de6b5c11cd24da7](https://github.com/sctplab/usrsctp/commit/1ab1d69ce8cbf20a4d0d1e41de6b5c11cd24da71) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=5736809862004736
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: use-after-free 
    - stack trace:  
		```
		sctp_fill_hmac_digest_m   
		sctp_lowlevel_chunk_output   
		sctp_med_chunk_output
		```

### Bug-inducing commit information
- bug-inducing commit: [05bea46702687f26a81c41c3fb1fd1dd3d9c0aa1](https://github.com/sctplab/usrsctp/commit/05bea46702687f26a81c41c3fb1fd1dd3d9c0aa1) (4 Oct 2019)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `sctp_handle_asconf(struct mbuf *, unsigned int, struct sockaddr *, struct sctp_asconf_chunk *, struct sctp_tcb *, int)`
    - bug locations: [usrsctplib/netinet/sctp_asconf.c:720](https://github.com/sctplab/usrsctp/commit/05bea46702687f26a81c41c3fb1fd1dd3d9c0aa1#diff-0ec0b47c46d30f537fb88f47a502ef53ddebfbf04955128d6f72137bb067e63dR720) 
- [seed_corpus.tar](https://drive.google.com/file/d/1SxgijItVfmXrFmsCbNkoq87xIy9uOh6w/view?usp=share_link): initial seed corpus at bug-inducing commit (156 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 167
	- \# seed corpus at fix-inducing commit: 167
- the number of commits between failure-observed commit and BIC: 7

### Bug-fixing commit information
- bug-fixing commit: [b7e98787c4698521b7adc771ee919a74e83f28ed](https://github.com/weinrank/usrsctp/commit/b7e98787c4698521b7adc771ee919a74e83f28ed) (13 Oct 2019)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://github.com/weinrank/usrsctp/commit/b7e98787c4698521b7adc771ee919a74e83f28ed)
    - changed functions: `sctp_med_chunk_output(struct sctp_inpcb *, struct sctp_tcb *, struct sctp_association *, int *, int *, int, int, struct timeval *, int *, int, int)`
    - fix locations: [usrsctplib/netinet/sctp_output.c:8380-8381](https://github.com/weinrank/usrsctp/commit/b7e98787c4698521b7adc771ee919a74e83f28ed#diff-ea8890ceccfa6038b6f942b495c91b8c2294475c1af7edbe455e2ed49032e5cdR8380-R8381), [8579-8580](https://github.com/weinrank/usrsctp/commit/b7e98787c4698521b7adc771ee919a74e83f28ed#diff-ea8890ceccfa6038b6f942b495c91b8c2294475c1af7edbe455e2ed49032e5cdR8579-R8580) 
- the number of commits between BIC and BFC: 9

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
- failures by other bugs: 2 failures in `other_failures/`
    - failures detected by AFL++ for 48 hours on a clean version (i.e., commit right before BIC)
		- [failure1](./other_failures/failure1), [failure2](./other_failures/failure2)


- target failure 
    - type: use-after-free 
    - failure stack trace patterns for the expected failure:  
		```
		sctp_fill_hmac_digest_m /src/usrsctp/usrsctplib/netinet/sctp_auth.c:1549:2  
		sctp_lowlevel_chunk_output /src/usrsctp/usrsctplib/netinet/sctp_output.c:4174:3  
		sctp_med_chunk_output /src/usrsctp/usrsctplib/netinet/sctp_output.c:9360:17
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./fuzzer_connect failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 156 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |    no  |
    |   AFL++   |   no  |   no  |   no  |   no  |   no  |   no  |  9750 |   no  |   no  |    no  |

