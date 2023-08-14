### Failure information on openh264-26220
- OSS-Fuzz issue: [26220](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=26220) (9 Oct 2020) 
- fuzz target: [decoder_fuzzer.cpp](https://github.com/google/oss-fuzz/blob/456eded09c7f24c5ee3f14fd2e358edc7de9064c/projects/openh264/decoder_fuzzer.cpp) which is the latest version before the oss-fuzz issue 26220 report time successfully reproduces a reported failure with a bug-revealing input (29 Sep 2020)
    - failure-observed commit: [83a0eae9bbbda5bfe802438109a025a3d7caee10](https://github.com/cisco/openh264/commit/83a0eae9bbbda5bfe802438109a025a3d7caee10) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=5153819073445888
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: heap-buffer-overflow  
    - stack trace:  
		```
		WelsDec::WelsCheckAndRecoverForFutureDecoding   
		WelsDec::WelsInitBSliceRefList  
		InitRefPicList 
		```

### Bug-inducing commit information
- bug-inducing commit: [effb3931c7c67f34b167fe6e0a93253bf075f78c](https://github.com/cisco/openh264/commit/effb3931c7c67f34b167fe6e0a93253bf075f78c) (7 Sep 2020)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `CWelsDecoder::DecodeFrame2WithCtx(PWelsDecoderContext, const unsigned char *, const int, unsigned char **, SBufferInfo *)`
    - bug locations: [codec/decoder/plus/src/welsDecoderExt.cpp:814-817](https://github.com/cisco/openh264/commit/effb3931c7c67f34b167fe6e0a93253bf075f78c#diff-089ebaf0325c2c30af67611943308f0621afbceb64450c668961b6bd1561b43fL814-L817) 
- [seed_corpus.tar](https://drive.google.com/file/d/13SyFZwL3cAs7qHD0FQ_W81Li3b1wNg_o/view?usp=share_link): initial seed corpus at bug-inducing commit (174 initial seeds in `seed_corpus/`)  
	- seed corpus consists of the following files:
		- `fuzzdata/samples/h264/*` files in [fuzzdata](https://github.com/mozillasecurity/fuzzdata) at [82c53bdf2a3da3b55974b7f56a636840d578f1c9](https://github.com/MozillaSecurity/fuzzdata/commit/82c53bdf2a3da3b55974b7f56a636840d578f1c9)  
		- `openh264/res/*.264` files in [openh264](https://github.com/cisco/openh264) at [BIC](effb3931c7c67f34b167fe6e0a93253bf075f78c)
	- \# seed corpus at failure-observed commit: 174
	- \# seed corpus at fix-inducing commit: 174
- the number of commits between failure-observed commit and BIC: 18

### Bug-fixing commit information
- bug-fixing commit: [4c76c67e9b790fd40650c4e8a2a059603e8ce195](https://github.com/cisco/openh264/commit/4c76c67e9b790fd40650c4e8a2a059603e8ce195) (11 Oct 2020)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://github.com/cisco/openh264/commit/4c76c67e9b790fd40650c4e8a2a059603e8ce195)
    - changed functions: `CWelsDecoder::DecodeFrame2WithCtx(PWelsDecoderContext, const unsigned char *, const int, unsigned char **, SBufferInfo *)`
    - fix locations: [codec/decoder/plus/src/welsDecoderExt.cpp:814-817](https://github.com/cisco/openh264/commit/4c76c67e9b790fd40650c4e8a2a059603e8ce195#diff-089ebaf0325c2c30af67611943308f0621afbceb64450c668961b6bd1561b43fR814-R817) 
- the number of commits between BIC and BFC: 19 

### Failure samples
- failure by a target bug: 10 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
		- oss-fuzz issue [26220](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=26220), [25921](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=25921), [25922](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=25922), [25923](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=25923), [25932](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=25932), [25939](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=25939), [25961](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=25961), [25970](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=25970), [25973](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=25973), [26068](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=26068) 
- failures by other bugs: 0 failures 

- target failure by issue-26220 (other failures by target bugs are written in `oracle.py`)
    - type: heap-buffer-overflow  
    - failure stack trace patterns for the expected failure:  
		```
		WelsDec::WelsCheckAndRecoverForFutureDecoding(WelsDec::TagWelsDecoderContext*) /src/openh264/codec/decoder/core/src/manage_dec_ref.cpp:182:11  
		WelsDec::WelsInitBSliceRefList(WelsDec::TagWelsDecoderContext*, int) /src/openh264/codec/decoder/core/src/manage_dec_ref.cpp:232:17  
		InitRefPicList /src/openh264/codec/decoder/core/src/decoder_core.cpp:2425:12
		```

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./decoder_fuzzer failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 174 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |    no  |
    |   AFL++   |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |    no  |

