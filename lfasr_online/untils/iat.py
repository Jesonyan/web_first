import base64
import hashlib
import json
import time

import requests

URL = "https://api.xfyun.cn/v1/service/v1/iat"
APPID = "5bc445a5"
API_KEY = "b1feec08bd8eae5d4a0df07e06d18b71"


def getHeader(aue, engineType):
    curTime = str(int(time.time()))
    # curTime = '1526542623'
    # param = "{\"aue\":\"" + aue + "\"" + ",\"engine_type\":\"" + engineType + "\"+ ",\"engine_type\":\"" + engineType + "\"}"
    param = {}
    param["engine_type"] = engineType
    param["aue"] = aue
    # param["speex_size"] = "38"
    # param["speex_size"] = str(60)
    # param["vinfo"] = "1"
    param = json.dumps(param)
    # print("param:{}".format(param))
    paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
    # print("x_param:{}".format(paramBase64))

    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + paramBase64).encode('utf-8'))
    checkSum = m2.hexdigest()
    # print('checkSum:{}'.format(checkSum))
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    # print(header)
    return header


def getBody(filepath):
    # binfile = open(filepath, 'rb')
    # data = {'audio': base64.b64encode(binfile.read())}
    data = {'audio': base64.b64encode(filepath)}
    # print(data)
    # print('data:{}'.format(type(data['audio'])))
    # print("type(data['audio']):{}".format(type(data['audio'])))
    return data


aue = "raw"


# audioFilePath = r"C:\Users\Administrator\Desktop\16k.8bit.pcm"

def iat_request(audioFilePath, engineType="sms16k"):
    response = requests.post(url=URL, data=getBody(audioFilePath), headers=getHeader(aue, engineType))
    result = response.content.decode('utf-8')
    print(result)
    return result

# iat_request(r"D:\weachat\WeChat Files\yan1281225057\FileStorage\File\2019-03\test.wav")
# for dirname, root, filenames in os.walk(r'C:\Users\Administrator\Desktop\录音'):
#     for filename in filenames:
#         audioFilePath = r'C:\Users\Administrator\Desktop\录音/' + filename
#         r = requests.post(URL, headers=getHeader(aue, engineType), data=getBody(audioFilePath))
#         result = r.content.decode('utf-8')
#         text = json.loads(result)
#         print(text['data'])
#
#         print(type(text))
#         result = text['data'] + '\n'
#         with open(r'C:\Users\Administrator\Desktop\result.txt', 'a+') as f:
#             f.write(result)
