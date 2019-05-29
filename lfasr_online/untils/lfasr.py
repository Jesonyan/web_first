# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import http.client
import json
import os
import time
import urllib.parse
import shutil
import requests
import threading
# reload(sys)
# sys.setdefaultencoding('ISO-8859-1')

lfasr_host = 'raasr.xfyun.cn'
# 讯飞开放平台的appid和secret_key
app_id = '5ac73e6d'
secret_key = '096064e9c39a823bbc78e62dccc8ab66'
# 请求的接口名
api_prepare = '/prepare'
api_upload = '/upload'
api_merge = '/merge'
api_get_progress = '/getProgress'
api_get_result = '/getResult'
# 文件分片大下52k
file_piece_sice = 10485760
# 要是转写的文件路径
# uplaod_file_path = r'C:\Users\Administrator\Desktop\test\20180605_18456596025_8079032.mp3'

base_header = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json;charset=utf-8'}

# ——————————————————转写可配置参数————————————————
# 转写类型
lfasr_type = 0
# 是否开启分词
has_participle = 'false'
has_seperate = 'true'
# 多候选词个数
max_alternatives = 0
# 子用户标识
suid = ''


def prepare():
    response = requests.post(url="http://raasr.xfyun.cn/api" + api_prepare, data=generate_request_param(api_prepare))
    # data = json.loads(response.text)["data"]
    print("prepare:" + response.text)
    return response.text
    # return lfasr_post(api_prepare, urllib.parse.urlencode(generate_request_param(api_prepare)), base_header)


def upload(taskid, upload_file_path):
    file_object = open(upload_file_path, 'rb')
    try:
        index = 1
        sig = SliceIdGenerator()
        while True:
            content = file_object.read(file_piece_sice)
            if not content or len(content) == 0:
                break
            response = post_multipart_formdata(generate_request_param(api_upload, taskid, sig.getNextSliceId()),
                                               content)
            if json.loads(response).get('ok') != 0:
                # 上传分片失败
                print('upload slice fail, response: ' + response)
                return False
            print('upload slice ' + str(index) + ' success')
            index += 1
    finally:
        'file index:' + str(file_object.tell())
        file_object.close()

    return True


def merge(taskid):
    return lfasr_post(api_merge, urllib.parse.urlencode(generate_request_param(api_merge, taskid)), base_header)


def get_progress(taskid):
    return lfasr_post(api_get_progress, urllib.parse.urlencode(generate_request_param(api_get_progress, taskid)),
                      base_header)


def get_result(taskid):
    print(urllib.parse.urlencode(generate_request_param(api_get_result, taskid)))
    return lfasr_post(api_get_result, urllib.parse.urlencode(generate_request_param(api_get_result, taskid)),
                      base_header)


# 根据请求的api来生成请求参数
def generate_request_param(apiname, taskid=None, slice_id=None):
    # 生成签名与时间戳
    ts = str(int(time.time()))
    tt = (app_id + ts).encode('utf-8')
    m2 = hashlib.md5()
    m2.update(tt)
    md5 = m2.hexdigest()
    md5 = bytes(md5, encoding='utf-8')
    # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
    signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
    signa = base64.b64encode(signa)
    signa = str(signa, 'utf-8')
    file_len = os.path.getsize(upload_file_path)
    file_name = os.path.basename(upload_file_path)
    param_dict = {}

    # 根据请求的api_name生成请求具体的请求参数
    if apiname == api_prepare:

        slice_num = int(file_len / file_piece_sice) + (0 if (file_len % file_piece_sice == 0) else 1)

        # print(slice_num)
        param_dict['app_id'] = app_id
        param_dict['signa'] = signa
        param_dict['ts'] = ts
        param_dict['file_len'] = str(file_len)
        param_dict['file_name'] = file_name
        param_dict['slice_num'] = str(slice_num)
        param_dict['has_seperate'] = 'true'

        # param_dict['max_alternatives'] = str(max_alternatives)
        # param_dict['suid'] = suid
    elif apiname == api_upload:
        param_dict['app_id'] = app_id
        param_dict['signa'] = signa
        param_dict['ts'] = ts
        param_dict['task_id'] = taskid
        param_dict['slice_id'] = slice_id
    elif apiname == api_merge:
        param_dict['app_id'] = app_id
        param_dict['signa'] = signa
        param_dict['ts'] = ts
        param_dict['task_id'] = taskid
        # parentpath, shotname, extension = get_file_msg(upload_file_path)
        # file_name = shotname + extension
        param_dict['file_name'] = file_name
    elif apiname == api_get_progress or apiname == api_get_result:
        param_dict['app_id'] = app_id
        param_dict['signa'] = signa
        param_dict['ts'] = ts
        param_dict['task_id'] = taskid
    return param_dict


def get_file_msg(filepath):
    (parentpath, tempfilename) = os.path.split(filepath)
    (shotname, extension) = os.path.splitext(tempfilename)
    return parentpath, shotname, extension


def lfasr_post(apiname, requestbody, header):
    conn = http.client.HTTPConnection(lfasr_host)
    conn.request('POST', '/api' + apiname, requestbody, header)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    conn.close()
    return data


def post_multipart_formdata(strparams, content):
    files = {
        "filename": strparams.get("slice_id"),
        "content": content
    }
    response = requests.post("http://raasr.xfyun.cn/api" + api_upload, files=files, data=strparams)
    print(response.text)
    return response.text


class SliceIdGenerator:
    """slice id生成器"""

    def __init__(self):
        self.__ch = 'aaaaaaaaa`'

    def getNextSliceId(self):
        ch = self.__ch
        j = len(ch) - 1
        while j >= 0:
            cj = ch[j]
            if cj != 'z':
                ch = ch[:j] + chr(ord(cj) + 1) + ch[j + 1:]
                break
            else:
                ch = ch[:j] + 'a' + ch[j + 1:]
                j = j - 1
        self.__ch = ch
        return self.__ch


def request_lfasr_result(filename, upload_file_path, appid):
    # 1.预处理
    pr = prepare()
    prepare_result = json.loads(pr)
    if prepare_result['ok'] != 0:
        print('prepare error, ' + str(pr))
        return

    taskid = prepare_result['data']
    print('prepare success, taskid: ' + taskid)

    # 2.分片上传文件
    if upload(taskid, upload_file_path=upload_file_path):
        print('upload success')
    else:
        print('upload fail')

    # 3.文件合并
    mr = merge(taskid)
    merge_result = json.loads(mr)
    if merge_result['ok'] != 0:
        print('merge fail, ' + mr)
        return

    # 4.获取任务进度
    while True:
        # 每隔20秒获取一次任务进度
        progress = get_progress(taskid)
        progress_dic = json.loads(progress)
        if progress_dic['err_no'] != 0 and progress_dic['err_no'] != 26605:
            print('task error: ' + progress_dic['failed'])
            return
        else:
            data = progress_dic['data']
            task_status = json.loads(data)
            if task_status['status'] == 9:
                print('task ' + taskid + ' finished')
                break
            print('The task ' + taskid + ' is in processing, task status: ' + data)

        # 每次获取进度间隔20S
        time.sleep(20)
    # save_result = 'result/' + os.path.basename(upload_file_path)
    # shutil.rmtree(save_result)
    # 5.获取结果
    lfasr_result = json.loads(get_result(taskid))
    print("result: " + lfasr_result['data'])
    a = json.loads(lfasr_result['data'])
    for i in range(len(a)):
        global save_result
        save_result = os.path.dirname(os.getcwd()) + "/result/" + os.path.basename(
            os.path.dirname(upload_file_path)) + "/"
        # print(save_result)
        text = a[i]
        content = "speaker: " + str(text['speaker']) + ":   " + text['onebest'] + '\n'
        if os.path.exists(save_result) is False:
            os.makedirs(save_result)
        with open(r"{0}\{1}".format(save_result, filename + ".txt"), 'ab+') as f:
            f.write(content.encode('utf-8'))


# def lfasr_batch(filename, upload_file_path, appid=None):
    # for dirpath, root, filenames in os.walk(upload_file):
    #     files = filenames
    #     for filename in files:
    #         files.remove(filename)
    #         global upload_file_path
    #
    #         upload_file_path = upload_file + "\{0}".format(filename)
    # request_lfasr_result(filename, upload_file_path, appid)
    # print(save_result)
    # return save_result


class MyThread(threading.Thread):
    def __init__(self, threadID, filename, upload_file_path,appid):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.upload_file_path = upload_file_path
        self.filename = filename
        self.appid = appid

    def run(self):
        print("start:" + self.upload_file_path)
        # lfasr_batch(self.filename, self.upload_file_path)
        request_lfasr_result(self.filename, self.upload_file_path, self.appid)
        print("end:" + self.upload_file_path)


def lfasr_thread(upload_file):
    threadList = []
    # upload_file = r'D:\Users\Administrator\PycharmProjects\lfasr_online\files\转写_wav_mismeadure'
    for root, dirs, files in os.walk(upload_file):
        sum = len(files)
        for i in range(0, sum):
            global upload_file_path
            upload_file_path = root + '/' + files[0]
            thread = MyThread(i, filename=files[0], upload_file_path=upload_file_path,appid=app_id)
            thread.start()
            threadList.append(thread)
            files.remove(files[0])
        for t in threadList:
            t.join()
    return save_result


# if __name__ == '__main__':
#     threadList = []
#     upload_file = r'D:\Users\Administrator\PycharmProjects\lfasr_online\files\转写_wav_mismeadure'
#     for root, dirs, files in os.walk(upload_file):
#         sum = len(files)
#         for i in range(0, sum):
#             upload_file_path = root + '/' + files[0]
#             thread = MyThread(i, filename=files[0], upload_file_path=upload_file_path)
#             thread.start()
#             threadList.append(thread)
#             files.remove(files[0])
#         for t in threadList:
#             t.join()
# lfasr_batch(r"C:\Users\Administrator\Desktop\lejuwav")
