### Failure information on readstat-13262
- OSS-Fuzz issue: [13262](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=13262) (22 Feb 2019) 
- fuzz target: [fuzz_format_sas7bdat.c](https://github.com/WizardMac/ReadStat/blob/bd7b41057a5670b90ea77bf4ea5b5d9ae5b20129/src/fuzz/fuzz_format_sas7bdat.c) which is the latest version before the oss-fuzz issue 13262 report time successfully reproduces a reported failure with a bug-revealing input (16 Feb 2019)
    - failure-observed commit: [bd7b41057a5670b90ea77bf4ea5b5d9ae5b20129](https://github.com/WizardMac/ReadStat/commit/bd7b41057a5670b90ea77bf4ea5b5d9ae5b20129) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=5137957567070208
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: heap-buffer-overflow  
    - stack trace:  
		```
		sas_read8   
		sas7bdat_parse_subheader_pointer   
		sas7bdat_parse_page_pass2  
		```

### Bug-inducing commit information
- bug-inducing commit: [1de4f389a8ffb07775cb1d99e33cbfa7e96bccf2](https://github.com/WizardMac/ReadStat/commit/1de4f389a8ffb07775cb1d99e33cbfa7e96bccf2) (20 Jan 2019)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `sas7bdat_submit_columns(sas7bdat_ctx_t *, int)`
    - bug locations: [src/sas/readstat_sas7bdat_read.c:602-603](https://github.com/WizardMac/ReadStat/commit/1de4f389a8ffb07775cb1d99e33cbfa7e96bccf2#diff-e76aa66cad6b541963367ca4d9882bbe943f0c59803011df35c2ec80c0842fbeR602-R603) 
- seed_corpus.tar(link): initial seed corpus at bug-inducing commit (94 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 94
	- \# seed corpus at fix-inducing commit: 94
- the number of commits between failure-observed commit and BIC: 41

### Bug-fixing commit information
- bug-fixing commit: [f57262da9966803ee97a5cecfe24512d38c3625e](https://github.com/WizardMac/ReadStat/commit/f57262da9966803ee97a5cecfe24512d38c3625e) (14 Apr 2019)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://github.com/WizardMac/ReadStat/commit/f57262da9966803ee97a5cecfe24512d38c3625e)
    - changed functions: `sas7bdat_parse_page_pass1(const char *, size_t, sas7bdat_ctx_t *)`, `sas7bdat_parse_page_pass2(const char *, size_t, sas7bdat_ctx_t *)`
    - fix locations: [src/sas/readstat_sas7bdat_read.c:788-792](https://github.com/WizardMac/ReadStat/commit/f57262da9966803ee97a5cecfe24512d38c3625e#diff-e76aa66cad6b541963367ca4d9882bbe943f0c59803011df35c2ec80c0842fbeR788-R792)  
- the number of commits between BIC and BFC: 44

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
- failures by other bugs: 5 failures in `other_failures/`
    - failures detected by AFL++ for 48 hours on a clean version (i.e., commit right before BIC)
		- [failure1](./other_failures/failure1), [failure2](./other_failures/failure2), [failure3](./other_failures/failure3)
	- oss-fuzz issue [12978](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=12978), [12598](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=12598)
- target failure 
   	- type: heap-buffer-overflow  
    - failure stack trace patterns for the expected failure
		```
		sas_read8 /src/readstat/src/sas/readstat_sas.c:86:5  
		sas7bdat_parse_page_pass2 /src/readstat/src/sas/readstat_sas7bdat_read.c:744:26  
		sas7bdat_parse_all_pages_pass2 /src/readstat/src/sas/readstat_sas7bdat_read.c:969:23
		```
	- to discriminate the identical failure stack trace by other bugs, insert the logging message to `src/sas/readstat_sas7bdat_read.c`:
		```diff
		static readstat_error_t sas7bdat_submit_columns(sas7bdat_ctx_t *ctx, int compres) {
		...
		 	if (ctx->column_count == 0)
		602 -		goto cleanup;
		602 +		{ fprintf(stderr, "[BugOSS] src/sas/readstat_sas7bdat_read.c:602\n"); goto cleanup; }
		```
- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./fuzz_format_sas7bdat failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 94 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |    no  |
    |   AFL++   | 13004 | 15881 |   no  |   no  | 20091 |  3336 | 14652 | 21057 |   no  |  12692 |

