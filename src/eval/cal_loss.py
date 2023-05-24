# import argparse
# import json

# # 使用命令行参数-i指定输入文件名

# parser = argparse.ArgumentParser()
# parser.add_argument('-i', '--input', default='webrtc_receiver_loss.log')
# args = parser.parse_args()

# with open(args.input, mode="r", encoding="utf-8-sig") as f:
#     #out_file = open("throughput.out", "w+")

#     total_count = 0
#     total_loss = 0

#     while(True):
#         text_line = f.readline()
#         if(text_line):
#             if(text_line.startswith("(receive_statistics_impl.cc:210):")):
#                 total_count += 1
#             if(text_line.startswith("(receive_statistics_impl.cc:267):")):
#                 total_loss += (int)(text_line.strip()[-1])
            
#             #print(arrivalTimeMs, payloadSize, file=out_file)
#         else:
#             break
#     #print(total_payload_size, total_time)
#     print(total_loss / total_count)
#     f.close()
#     #out_file.close()

import argparse
import json

# 使用命令行参数-i指定输入文件名

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', default='BetaRTC/webrtc_receiver_mut.log')
args = parser.parse_args()

with open(args.input, mode="r", encoding="utf-8-sig") as f:
    # out_file = open(args.input[:-4] + "_loss.out", "w+")

    flag = False
    last_arrival_time = 0
    total_time_ms = 0
    total_loss = 0
    total_count = 0

    count_dealed = False
    loss_dealed = False

    while(True):
        text_line = f.readline()
        if(text_line):
            if(text_line.startswith("(remote_estimator_proxy.cc:151):")):
                # json_data = json.loads(text_line[33:])
                # arrivalTimeMs = json_data["packetInfo"]["arrivalTimeMs"]
                # payloadSize = json_data["packetInfo"]["payloadSize"]

                if(flag == False):
                    flag = True
                #    last_arrival_time = arrivalTimeMs

                # 过了1s时间，输出吞吐量
                # if(total_time_ms + arrivalTimeMs - last_arrival_time > 200):
                #     print(total_loss / total_count, file=out_file)
                #     total_time_ms = 0
                #     # total_payload_size = 0
                #     total_loss = 0
                #     total_count = 0

                # total_payload_size += int(payloadSize)
                # total_time_ms += arrivalTimeMs - last_arrival_time
                # last_arrival_time = arrivalTimeMs
                count_dealed = False
                loss_dealed = False
            
            if(text_line.startswith("(receive_statistics_impl.cc:210):") and not count_dealed):
                total_count += 1
                count_dealed = True
            
            if(text_line.startswith("(receive_statistics_impl.cc:267):") and not loss_dealed):
                total_loss += (int)(text_line.strip()[-1])
                loss_dealed = True
            
            #print(arrivalTimeMs, payloadSize, file=out_file)
        else:
            break
    #print(total_payload_size, total_time)
    print(total_loss / total_count)
    f.close()
    #out_file.close()


'''
{
    "mediaInfo":
    {
        "audioInfo":
        {
            "audioJitterBufferDelay":1.7976931348623157e+308,
            "audioJitterBufferEmittedCount":18446744073709551615,
            "concealedSamples":18446744073709551615,
            "concealmentEvents":18446744073709551615,
            "echoReturnLoss":1.7976931348623157e+308,
            "echoReturnLossEnhancement":1.7976931348623157e+308,
            "estimatedPlayoutTimestamp":9223372036854775807,
            "totalSamplesReceived":18446744073709551615,
            "totalSamplesSent":18446744073709551615
        },
        "videoInfo":
        {
            "framesCaptured":18446744073709551615,
            "framesDecoded":18446744073709551615,
            "framesDroped":18446744073709551615,
            "framesReceived":18446744073709551615,
            "framesSent":18446744073709551615,
            "fullFramesLost":18446744073709551615,
            "hugeFreameSent":18446744073709551615,
            "keyFramesReceived":18446744073709551615,
            "keyFramesSent":18446744073709551615,
            "partialFramesLost":18446744073709551615,
            "videoJitterBufferDelay":1.7976931348623157e+308,
            "videoJitterBufferEmittedCount":18446744073709551615
        }
    },
    "pacerPacingRate":1.7976931348623157e+308,
    "pacerPaddingRate":1.7976931348623157e+308,
    "packetInfo":
    {
        "arrivalTimeMs":1648712865749,
        "header":
        {
            "headerLength":24,
            "paddingLength":0,
            "payloadType":125,
            "sendTimestamp":48291,
            "sequenceNumber":15621,
            "ssrc":1789444856
        },
        "lossRates":0.0,
        "payloadSize":757
    }
}
'''
