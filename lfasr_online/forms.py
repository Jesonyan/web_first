from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


class BaseForm(FlaskForm):
    def get_error(self):
        print(self.errors)
        message = self.errors.popitem()[1][0]
        print(message)
        return message


class TtsForm(BaseForm):
    appid = StringField(validators=[InputRequired(message="请输入appid")])
    apikey = StringField(validators=[InputRequired(message="请输入apikey")])
    text = StringField(validators=[InputRequired(message="请输入文本信息")])
    voice_name = StringField()
    checkbox = StringField()
