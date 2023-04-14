"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

failure_type = "AddressSanitizer: heap-buffer-overflow"
failure_stack_trace = [\
	"pcpp::SSLCertificateRequestMessage::SSLCertificateRequestMessage(unsigned char*, unsigned long, pcpp::SSLHandshakeLayer*) /src/PcapPlusPlus/Packet++/src/SSLHandshake.cpp:1614:22",
	"pcpp::SSLHandshakeMessage::createHandhakeMessage(unsigned char*, unsigned long, pcpp::SSLHandshakeLayer*) /src/PcapPlusPlus/Packet++/src/SSLHandshake.cpp:1118:14",
	"pcpp::SSLHandshakeLayer::SSLHandshakeLayer(unsigned char*, unsigned long, pcpp::Layer*, pcpp::Packet*) /src/PcapPlusPlus/Packet++/src/SSLLayer.cpp:153:34"]
failure_logging = "[BugOSS] Packet++/src/Packet.cpp:712"

f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())

if failure_type not in exec_result:
	print("This is different failure type")
	exit()

if failure_logging not in exec_result:
	print("The additional branch is not executed")
	exit()

n_correct = 0
for st in failure_stack_trace:
	if st in exec_result:
		n_correct += 1

if n_correct == 3:
	print("Find a failure by a target bug")
else:
	print("This is different failure what we want to find")
