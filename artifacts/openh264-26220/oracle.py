"""
	It receives an execution result of fuzzer with a failing test case
"""

import sys

def check(exec_result, failure_type, failure_stack_trace):
	if failure_type not in exec_result:
		return False

	n_correct = 0
	for st in failure_stack_trace:
		if st in exec_result:
			n_correct += 1

	if n_correct == 3:
		return True
	return False



f = open(sys.argv[1], 'r')
exec_result = ''.join(f.readlines())

failure25921_type = "AddressSanitizer: heap-buffer-overflow"
failure25921_stack_trace = [\
	"WelsDec::NeedErrorCon(WelsDec::TagWelsDecoderContext*) /src/openh264/codec/decoder/core/src/error_concealment.cpp:450:10",
	"WelsDec::CheckAndFinishLastPic(WelsDec::TagWelsDecoderContext*, unsigned char**, TagBufferInfo*) /src/openh264/codec/decoder/core/src/decoder_core.cpp:2940:57",
	"WelsDecodeBs /src/openh264/codec/decoder/core/src/decoder.cpp:877:9"]

failure25922_type = "UndefinedBehaviorSanitizer: undefined-behavior"
failure25922_error_message = "codec/decoder/core/src/error_concealment.cpp:130:12: runtime error: load of value 81, which is not a valid value for type 'bool'"
failure25922_stack_trace = [\
	"WelsDec::DoErrorConSliceCopy(WelsDec::TagWelsDecoderContext*) /src/openh264/codec/decoder/core/src/error_concealment.cpp:130:12",
	"WelsDec::ImplementErrorCon(WelsDec::TagWelsDecoderContext*) /src/openh264/codec/decoder/core/src/error_concealment.cpp:470:5",
	"WelsDec::CheckAndFinishLastPic(WelsDec::TagWelsDecoderContext*, unsigned char**, TagBufferInfo*) /src/openh264/codec/decoder/core/src/decoder_core.cpp:2942:7"]

failure25923_type = "Abrt"

failure25932_type = "AddressSanitizer: heap-buffer-overflow"
failure25932_stack_trace = [\
	"WelsDec::DoErrorConSliceCopy(WelsDec::TagWelsDecoderContext*) /src/openh264/codec/decoder/core/src/error_concealment.cpp:130:12",
	"WelsDec::ImplementErrorCon(WelsDec::TagWelsDecoderContext*) /src/openh264/codec/decoder/core/src/error_concealment.cpp:470:5",
	"WelsDec::CheckAndFinishLastPic(WelsDec::TagWelsDecoderContext*, unsigned char**, TagBufferInfo*) /src/openh264/codec/decoder/core/src/decoder_core.cpp:2942:7"]

failure25939_type = "AddressSanitizer: attempting double-free"
failure25939_stack_trace = [\
	"WelsCommon::WelsFree(void*, char const*) /src/openh264/codec/common/src/memory_align.cpp:113:5",
	"WelsCommon::CMemoryAlign::WelsFree(void*, char const*) /src/openh264/codec/common/src/memory_align.cpp:154:3",
	"WelsDec::FreePicture(WelsDec::SPicture*, WelsCommon::CMemoryAlign*) /src/openh264/codec/decoder/core/src/pic_queue.cpp:141:12"]

failure25961_type = "AddressSanitizer: heap-buffer-overflow"
failure25961_stack_trace = [\
	"WelsDec::UpdateP16x16MotionInfo(WelsDec::TagDqLayer*, int, signed char, short*) /src/openh264/codec/decoder/core/src/mv_pred.cpp:813:7",
	"WelsDec::ParseInterPMotionInfoCabac(WelsDec::TagWelsDecoderContext*, WelsDec::TagNeighborAvail*, unsigned char*, short (*) [30][2], short (*) [30][2], signed char (*) [30]) /src/openh264/codec/decoder/core/src/parse_mb_syn_cabac.cpp:562:5",
	"WelsDec::WelsDecodeMbCabacPSliceBaseMode0(WelsDec::TagWelsDecoderContext*, WelsDec::TagNeighborAvail*, unsigned int&) /src/openh264/codec/decoder/core/src/decode_slice.cpp:883:5"]

failure25970_type = "AddressSanitizer: heap-buffer-overflow"
failure25970_stack_trace = [\
	"UpdateDecStatNoFreezingInfo /src/openh264/codec/decoder/core/src/decoder.cpp:1215:34",
	"UpdateDecStat /src/openh264/codec/decoder/core/src/decoder.cpp:1243:5",
	"WelsDec::DecodeFrameConstruction(WelsDec::TagWelsDecoderContext*, unsigned char**, TagBufferInfo*) /src/openh264/codec/decoder/core/src/decoder_core.cpp:280:5"]

failure25973_type = "AddressSanitizer: heap-buffer-overflow"
failure25973_stack_trace = [\
	"WelsDec::WelsDecodeMbCabacPSlice(WelsDec::TagWelsDecoderContext*, WelsDec::TagNalUnit*, unsigned int&) /src/openh264/codec/decoder/core/src/decode_slice.cpp:1367:5",
	"WelsDec::WelsDecodeSlice(WelsDec::TagWelsDecoderContext*, bool, WelsDec::TagNalUnit*) /src/openh264/codec/decoder/core/src/decode_slice.cpp:1595:12",
	"WelsDec::DecodeCurrentAccessUnit(WelsDec::TagWelsDecoderContext*, unsigned char**, TagBufferInfo*) /src/openh264/codec/decoder/core/src/decoder_core.cpp:2755:18"]

failure26068_type = "AddressSanitizer: heap-buffer-overflow"
failure26068_stack_trace = [\
	"DeblockChromaLt42_c(unsigned char*, int, int, int, int, signed char*) /src/openh264/codec/common/src/deblocking_common.cpp:192:12",
	"DeblockChromaLt4H2_c(unsigned char*, int, int, int, signed char*) /src/openh264/codec/common/src/deblocking_common.cpp:239:3",
	"WelsDec::FilteringEdgeChromaHV(WelsDec::TagDqLayer*, WelsDec::tagDeblockingFilter*, int) /src/openh264/codec/decoder/core/src/deblocking.cpp:1085:9"]

failure26220_type = "AddressSanitizer: heap-buffer-overflow"
failure26220_stack_trace = [\
	"WelsDec::WelsCheckAndRecoverForFutureDecoding(WelsDec::TagWelsDecoderContext*) /src/openh264/codec/decoder/core/src/manage_dec_ref.cpp:182:11",
	"WelsDec::WelsInitBSliceRefList(WelsDec::TagWelsDecoderContext*, int) /src/openh264/codec/decoder/core/src/manage_dec_ref.cpp:232:17",
	"InitRefPicList /src/openh264/codec/decoder/core/src/decoder_core.cpp:2425:12"]



if check(exec_result, failure25921_type, failure25921_stack_trace) == True:
	print("Find a failure by a target bug")
	exit()

if check(exec_result, failure25932_type, failure25932_stack_trace) == True:
	print("Find a failure by a target bug")
	exit()

if check(exec_result, failure25939_type, failure25939_stack_trace) == True:
	print("Find a failure by a target bug")
	exit()

if check(exec_result, failure25961_type, failure25961_stack_trace) == True:
	print("Find a failure by a target bug")
	exit()

if check(exec_result, failure25970_type, failure25970_stack_trace) == True:
	print("Find a failure by a target bug")
	exit()

if check(exec_result, failure25973_type, failure25973_stack_trace) == True:
	print("Find a failure by a target bug")
	exit()

if check(exec_result, failure25068_type, failure25068_stack_trace) == True:
	print("Find a failure by a target bug")
	exit()

if check(exec_result, failure26220_type, failure26220_stack_trace) == True:
	print("Find a failure by a target bug")
	exit()

if check(exec_result, failure25922_type, failure25922_stack_trace) == True:
	if failure25922_error_message in exec_result:
		print("Find a failure by a target bug")
		exit()

if failure25923_type in exec_result:
	print("Find a failure by a target bug")
	exit()
