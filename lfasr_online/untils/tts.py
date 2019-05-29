# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import time
import os
import requests

URL = "https://api.xfyun.cn/v1/service/v1/tts"
AUE = "raw"


def getHeader(appid='5ba065de', apikey='737878202665c4064685cd01c2a4c639', voice_name="xiaoyan",
              auf="audio/L16;rate=16000"):
    curTime = str(int(time.time()))
    param = {}
    param["aue"] = "raw"
    param["auf"] = auf
    param["voice_name"] = voice_name
    param = json.dumps(param)
    print("param:{}".format(param))

    paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
    print("x_param:{}".format(paramBase64))

    m2 = hashlib.md5()
    m2.update((apikey + curTime + paramBase64).encode('utf-8'))

    checkSum = m2.hexdigest()
    print('checkSum:{}'.format(checkSum))

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': appid,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


def getBody(text):
    data = {'text': text}
    return data


def writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    f.close()


def tts_request(appid='5ba065de', apikey='737878202665c4064685cd01c2a4c639', voice_name="xiaoyan",
                auf="audio/L16;rate=16000", text=None):
    r = requests.post(url=URL, headers=getHeader(appid=appid, apikey=apikey, voice_name=voice_name,
                                                 auf=auf), data=getBody(text=text))
    contentType = r.headers['Content-Type']
    if contentType == "audio/mpeg":
        file = './files/' + voice_name + '.wav'
        if os.path.isfile(file):
            os.remove(file)
        with open(file,'wb') as f:
            f.write(r.content)
        print(r.headers)
        return True
    else:
        print("合成错误", voice_name)
        print(r.content)
        return r.content

