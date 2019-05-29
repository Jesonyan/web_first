#!/usr/bin/python
# -*- coding: UTF-8 -*-
import base64
import hashlib
import json
import time

import requests


def ise_request(text, audio, language=None, category=None, extra_ability=None):
    x_appid = '5ba065de'
    api_key = '085cfd0d636340369dc75c00c803ad1e'
    curTime = str(int(time.time()))
    url = 'https://api.xfyun.cn/v1/service/v1/ise'

    text = text
    # text = "Twenty children laugh and say,Look! A lamb in shcool"
    body = {'audio': base64.b64encode(audio), 'text': text}
    param = json.dumps({"aue": "raw", "reslt_level": "entirety", "language": language, "category": category, "extra_ability": extra_ability})
    print(param)
    paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
    m2 = hashlib.md5()
    m2.update((api_key + curTime + paramBase64).encode('utf-8'))
    checkSum = m2.hexdigest()
    x_header = {
        'X-Appid': x_appid,
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    req = requests.post(url, data=body, headers=x_header)
    result = req.content.decode('utf-8')
    print(result)
    return result
