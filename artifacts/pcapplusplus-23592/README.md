### Failure information on pcapplusplus-23592
- OSS-Fuzz issue: [23592](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=23592) (20 Jun 2020) 
- fuzz target: [FuzzTarget.c](https://github.com/seladb/PcapPlusPlus/blob/14a418ed4f9b72a832877dc8330e01259f617bf3/Tests/Fuzzers/FuzzTarget.cpp) which is the latest version before the oss-fuzz issue 23592 report time successfully reproduces a reported failure with a bug-revealing input (17 Jun 2020)
    - failure-observed commit: [14a418ed4f9b72a832877dc8330e01259f617bf3](https://github.com/seladb/PcapPlusPlus/commit/14a418ed4f9b72a832877dc8330e01259f617bf3) 
- bug-revealing input: https://oss-fuzz.com/download?testcase_id=4791311122300928
- sanitizer: address
    - `$CFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
    - `$CXXFLAGS -fsanitize=address -fsanitize-address-use-after-scope`
- reported failure symptom 
    - type: heap-buffer-overflow  
    - stack trace:  
		```
		pcpp::SSLCertificateRequestMessage::SSLCertificateRequestMessage(unsigned char*, unsigned long, pcpp::SSLHandshakeLayer*)   
		pcpp::SSLHandshakeMessage::createHandhakeMessage(unsigned char*, unsigned long, pcpp::SSLHandshakeLayer*)   
		pcpp::SSLHandshakeLayer::SSLHandshakeLayer(unsigned char*, unsigned long, pcpp::Layer*, pcpp::Packet*)
		```

### Bug-inducing commit information
- bug-inducing commit: [50aab202d24331ef35b9eff68d96ef9f97baf6a1](https://github.com/seladb/PcapPlusPlus/commit/50aab202d24331ef35b9eff68d96ef9f97baf6a1) (31 May 2020)
    - search the first commit that failure occurred by reproducing on the commit history with the fuzz target and the bug-revealing input
    - changed functions: `SSLClientHelloMessage::SSLClientHelloMessage(uint8_t *, size_t, SSLHandshakeLayer *)`, `SSLServerHelloMessage::SSLServerHelloMessage(uint8_t *, size_t, SSLHandshakeLayer *)`, `SSLServerHelloMessage::getSessionIDLength(void)`, `SSLCertificateRequestMessage::SSLCertificateRequestMessage(uint8_t *, size_t, SSLHandshakeLayer *)`, `SSLLayer::IsSSLMessage(uint16_t, uint16_t, uint8_t *, size_t, bool)`, `SSLLayer::parseNextLayer(void)`
    - bug locations: [Packet++/src/SSLHandshake.cpp:1608-1609](https://github.com/seladb/PcapPlusPlus/commit/50aab202d24331ef35b9eff68d96ef9f97baf6a1#diff-1d3e491c3afd45f303781820cb09f1ac73284aa377e0ef11fc7571ea35da47e8R1608-R1609) 
- [seed_corpus.tar](https://drive.google.com/file/d/1t0ZJIsrZTGCOqNFLkAEZCj58mvgS_f4U/view?usp=share_link): initial seed corpus at bug-inducing commit (615 initial seeds in `seed_corpus/`)
	- \# seed corpus at failure-observed commit: 619
	- \# seed corpus at fix-inducing commit: 622
- the number of commits between failure-observed commit and BIC: 46

### Bug-fixing commit information
- bug-fixing commit: [31406a092868f87d714910e349ab0b4dc683722b](https://github.com/seladb/PcapPlusPlus/commit/31406a092868f87d714910e349ab0b4dc683722b) (13 Sep 2020)
    - search the commit that the expected failure by the bug-revealing input does not induce after oss-fuzz issue report time
    - developers explicitly mentioned the bug fixes [here](https://github.com/seladb/PcapPlusPlus/commit/31406a092868f87d714910e349ab0b4dc683722b)
    - changed functions: `SSLClientHelloMessage::getSessionIDLength(void)`, `SSLCertificateRequestMessage::SSLCertificateRequestMessage(uint8_t *, size_t, SSLHandshakeLayer *)`
    - fix locations: [Packet++/src/SSLHandshake.cpp:1617-1618](https://github.com/seladb/PcapPlusPlus/commit/50aab202d24331ef35b9eff68d96ef9f97baf6a1#diff-1d3e491c3afd45f303781820cb09f1ac73284aa377e0ef11fc7571ea35da47e8R1608-R1609) 
- the number of commits between BIC and BFC: 130

### Failure samples
- failure by a target bug: 1 failure in `target_failures/`
    - a failure induced by a failure-reproducing input among attached inputs in oss-fuzz issues between BIC and BFC date, which appears from BIC until BFC
- failures by other bugs: 3 failures in `other_failures/`
	- [22963](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=22963), [23022](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=23022), [23026](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=23026)

- target failure 
    - type: heap-buffer-overflow  
    - failure stack trace patterns for the expected failure:  
		```
		pcpp::SSLCertificateRequestMessage::SSLCertificateRequestMessage(unsigned char*, unsigned long, pcpp::SSLHandshakeLayer*) /src/PcapPlusPlus/Packet++/src/SSLHandshake.cpp:1614:22  
		pcpp::SSLHandshakeMessage::createHandhakeMessage(unsigned char*, unsigned long, pcpp::SSLHandshakeLayer*) /src/PcapPlusPlus/Packet++/src/SSLHandshake.cpp:1118:14  
		pcpp::SSLHandshakeLayer::SSLHandshakeLayer(unsigned char*, unsigned long, pcpp::Layer*, pcpp::Packet*) /src/PcapPlusPlus/Packet++/src/SSLLayer.cpp:153:34  
		```
	- to discriminate the identical failure stack trace by other bugs, insert the logging message to `/src/PcapPlusPlus/Packet++/src/Packet.cpp`  
		```diff
		Layer* Packet::createFirstLayer(LinkLayerType linkType) {
			...
				else if (linkType == LINKTYPE_NULL)
				{
		712 -			return new NullLoopbackLayer((uint8_t*)rawData, rawDataLen, this);
		712 +		fprintf(stderr, "[BugOSS] Packet++/src/Packet.cpp:712\n");	return new NullLoopbackLayer((uint8_t*)rawData, rawDataLen, this);
				}
		```		

- `oracle.py` determines the detected failures by fuzzers are induced by the target bug or not. It receives a file which is the execution result of the fuzz target with a failing-input:  
	```
	./FuzzTarget failing-input 2> exec_result
	python3 oracle.py exec_result
	```

### Experiment with 2 baseline fuzzers 
- fuzzers
    - libFuzzer of llvm 14.0.0
    - AFL++ 4.05c
- seed_corpus: 615 seeds (seed_corpus.tar)
- time to first failure detection (limit 21600s)
    |   Fuzzer  | iter1 | iter2 | iter3 | iter4 | iter5 | iter6 | iter7 | iter8 | iter9 | iter10 |
    | --------- |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|
    | libFuzzer |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |   no  |    no  |
    |   AFL++   |   no  |   no  | 14199 |   no  |   no  |   no  |   no  |   no  |   no  |   4865 |

