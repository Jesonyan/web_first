from flask import jsonify


class ResponseCode(object):
    successful = 200
    paramerror = 400


def restful_result(code, message, data):
    return jsonify({
        'code': code,
        'message': message,
        'data': data or {}
    })


def successful(message="", data=None):
    return restful_result(code=ResponseCode.successful, message=message, data=data)


def error(message=""):
    return restful_result(code=ResponseCode.paramerror, message=message, data=None)


def file_upload_error(message=None):
    return message or "文件上传出错，请检查或者联系孟岩！"
