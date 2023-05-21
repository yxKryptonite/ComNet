import argparse
import json

# 使用命令行参数-i指定输入文件名

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', default='webrtc_receiver_22_3_31.log')
args = parser.parse_args()

with open(args.input, mode="r", encoding="utf-8-sig") as f:
    #out_file = open("throughput.out", "w+")

    flag = False
    last_arrival_time = 0
    total_time_ms = 0
    total_payload_size = 0

    while(True):
        text_line = f.readline()
        if(text_line):
            if(text_line.startswith("(remote_estimator_proxy.cc:147):") == False):
                continue
            json_data = json.loads(text_line[33:])
            arrivalTimeMs = json_data["packetInfo"]["arrivalTimeMs"]
            payloadSize = json_data["packetInfo"]["payloadSize"]

            total_payload_size += int(payloadSize)
            if(flag == False):
                flag = True
                last_arrival_time = arrivalTimeMs
            total_time_ms += arrivalTimeMs - last_arrival_time
            last_arrival_time = arrivalTimeMs
            
            #print(arrivalTimeMs, payloadSize, file=out_file)
        else:
            break
    #print(total_payload_size, total_time)
    print(total_payload_size * 1000 / total_time_ms)
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
