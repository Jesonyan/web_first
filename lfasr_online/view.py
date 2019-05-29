# _*_ coding: utf-8 _*_
import os
import shutil
import zipfile
from forms import TtsForm
from flask import render_template, request, views, g, make_response, send_from_directory, Blueprint
# from flask_wtf import CSRFProtect
# from tasks import get_result_send_email
from flask_mail import Message
from exts import mail
import config
from untils import iat, restful, ise, tts

Upload_Path = os.path.join(os.path.dirname(__file__), 'files')
views_bp = Blueprint("view", __name__, url_prefix='/')

from celery_task import celery
from untils import lfasr
# from flask_mail import Message
# from exts import mail
import os
import zipfile


# 压缩文件
def ZipFile(path, zipname):
    z = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(path):
        fpath = dirpath.replace(path, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
            print("压缩成功")
    z.close()
    return os.path.abspath(zipname)


@celery.task
def get_result_send_email(upload_file, to_email):
    save_path = lfasr.lfasr_thread(upload_file)
    result_file = ZipFile(save_path, 'tt.zip')
    print("保存压缩后转写结果的路径：" + result_file)
    try:
        email_send(to_email, file=result_file)
    except Exception as e:
        print(e)
# CSRFProtect(app)

# 发送邮件
def email_send(to_email=None, file=None):
    message = Message("转写结果", recipients=[to_email])
    with views_bp.open_resource(file) as fp:
        message.attach("tt.zip", "file/zip", fp.read())
    mail.send(message)

@views_bp.route('/lfasr/', methods=['GET', "POST"])
def upload_file():
    if request.method == 'GET':
        print('1')
        return render_template('lfasr.html')
    else:
        file = request.files.get("InputFile")
        appid = request.form.get("appid")
        apikey = request.form.get("apikey")

        to_email = request.form.get("email")
        g.to_email = to_email
        if not file:
            return '文件上传出错，请检查或者联系孟岩！'
        if not appid or not apikey or not to_email:
            return '请正确输入appid，apikey，email，并重新上传！'
        zip_file = os.path.join(Upload_Path, file.filename)
        print("上传的压缩文件保存路径：" + zip_file)
        file.save(zip_file)
        f = zipfile.ZipFile(zip_file, "r")
        dir = file.filename.split('.zip')[0]
        unzip_file = 'tmp/' + dir
        if os.path.exists(unzip_file):
            shutil.rmtree(unzip_file)
        os.mkdir(unzip_file)
        for i in f.namelist():
            f.extract(i, unzip_file)
        # requests.get('http://127.0.0.1:5000/get_result/',params={"unzip_file":unzip_file,"to_email":to_email})
        # return redirect(url_for('get_result', unzip_file=unzip_file, to_email=to_email))
        get_result_send_email.delay(upload_file=unzip_file, to_email=to_email)
        return "文件上传成功，请注意查收邮件"


@views_bp.route('/recorder/', methods=["GET", "POST"])
def recorder():
    if request.method == "GET":
        return render_template('iat.html')
    else:
        audio = request.files.get("audioData").read()
        # audio_upload_path = os.path.join(os.path.dirname(__file__), 'audio')
        # audio_file = os.path.join(audio_upload_path, audio.filename + '.wav')
        # if os.path.exists(audio_file):
        #     os.remove(audio_file)
        # audio.save(audio_file)
        result = iat.iat_request(audio)
        print(result)
        return result


# 听写类视图
class IatView(views.MethodView):
    def get(self, result=None):
        return render_template('iat_online.html', result=result)

    def post(self):
        file = request.files.get("InputFile").read()
        print(file, type(file))
        appid = request.form.get("appid")
        apikey = request.form.get("apikey")
        engineType = request.form.get("checkbox")
        if not file:
            return restful.file_upload_error()
        if not appid or not apikey:
            return restful.file_upload_error(message='请正确输入appid，apikey，并重新上传！')
        if engineType == "sms8k":
            result = iat.iat_request(file, engineType="sms8k")
        else:
            result = iat.iat_request(file)
        print(result)
        return self.get(result=result)


# 评测类视图
class IseView(views.MethodView):
    def get(self, result=None):
        return render_template('ise.html', result=result)

    def post(self):
        file = request.files.get("InputFile")
        appid = request.form.get("appid")
        apikey = request.form.get("apikey")
        category = request.form.get("checkbox")
        language = request.form.get("checkbox1")
        multi_dimension = request.form.get("multi_dimension")
        chapter = request.form.get("chapter")
        text = request.form.get('ise-content')
        if not file:
            return restful.file_upload_error()
        if not appid or not apikey:
            return restful.file_upload_error(message='请正确输入appid，apikey，并重新上传！')
        if not text:
            return restful.file_upload_error(message="请输入文本内容！")

        ise_result = ise.ise_request(text=text, language=language, category=category,
                                     extra_ability=multi_dimension, audio=file.read())
        return self.get(result=ise_result)


# 合成类视图
class TtsView(views.MethodView):
    def get(self, message=None):
        message = config.voice
        return render_template('tts.html', message=message)

    def post(self):
        form = TtsForm(request.form)
        if form.validate():
            voice_name = form.voice_name.data
            appid = form.appid.data
            apikey = form.apikey.data
            text = form.text.data
            checkbox = form.checkbox.data
            if not checkbox:
                checkbox = "audio/L16;rate=16000"
            result = tts.tts_request(appid=appid, apikey=apikey, voice_name=voice_name, text=text, auf=checkbox)
            if result is True:
                filename = voice_name + '.wav'
                print(filename)
                response = make_response(
                    send_from_directory(directory='./files/', filename=filename, as_attachment=True))
                response.headers["Content-Disposition"] = "attachment; filename={}".format(
                    filename.encode().decode('latin-1'))
                return response
            else:
                return result
        else:
            return restful.error(form.get_error())


views_bp.add_url_rule('/ise/', view_func=IseView.as_view('iseview'))
views_bp.add_url_rule('/iat/', view_func=IatView.as_view('iatview'))
views_bp.add_url_rule('/tts/', view_func=TtsView.as_view('ttsview'))
