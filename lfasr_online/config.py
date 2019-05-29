import os

TEMPLATES_AUTO_RELOAD = True
JSON_AS_ASCII = False

# secret key
SECRET_KEY = os.urandom(24)


# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
# MAIL_USE_TLS : default False
MAIL_USE_SSL = True
MAIL_USERNAME = '1281225057@qq.com'
MAIL_PASSWORD = 'nvozsrvnwsvlihfh'
MAIL_DEFAULT_SENDER = '1281225057@qq.com'


# Celery配置
CELERY_BROKER_URL = 'redis://:mengyan@47.96.9.78:6379/1'
CELERY_RESULT_BACKEND = 'redis://:mengyan@47.96.9.78:6379/1'

# 在线合成发音人
voice = {}
voice.update({
    "讯飞小燕": "xiaoyan",
    "讯飞许久": "aisjiuxu",
    "讯飞小萍": "aisxping",
    "讯飞许小宝": "aisbabyxu",
    "讯飞小媛": "x_xiaoyuan",
    "讯飞晓燕": "x_xiaoyan",
    "讯飞水哥": "x_xiaoxi",
    "讯飞彬哥": "x_binge",
    "讯飞马叔": "x_laoma",
    "讯飞颖儿": "x_liying_actor",
    "讯飞一峰": "x_yifeng",
    "讯飞小师": "x_xiaoshi_cts",
    "讯飞玉儿": "x_yuer",
    "讯飞小梅": "x_xiaomei",
    "讯飞小侯": "x_xiaohou",
    "讯飞小魏": "x_xiaowei",
    "讯飞刚哥": "x_xiaozhang",
    "讯飞小华": "x_xiaoyang_story",
    "讯飞飞飞": "x_feidie",
    "讯飞萌萌-高兴": "x_mengmenghappy",
    "讯飞萌萌-中立": "x_mengmengneutral",
    "讯飞小瑶": "x_xiaoyao",
    "讯飞小莹": "x_xiaoying",
    "讯飞小乔": "x_xiaoqiao",
    "讯飞小洋": "x_xiaoyang",
    "讯飞晓倩": "x_xiaoqian",
    "讯飞春春": "x_chunchun",
    "讯飞小梦": "x_xiaomeng",
    "讯飞凯瑟琳": "x_catherine",
    "讯飞小俊": "x_xiaojun",
    "讯飞小茹": "x_xiaoaineutral",
    "John": "x_john",
    "讯飞小光": "x_xiaoguan",
    "讯飞小肥": "x_xiaofei",
    "讯飞小薛": "x_xiaoxue_daqi",
    "讯飞程程": "x_chengcheng",
    "讯飞小雪": "x_xiaoxue",
    "讯飞瑶瑶": "x_yaoyao",
    "讯飞小彬": "x_xiaobin",
    "讯飞小桃丸": "x_xiaowanzi",
    "讯飞小强": "x_xiaoqiang",
    "讯飞虫虫": "x_chongchong",
    "讯飞玲姐姐": "x_zhilin",
    "讯飞晓琳": "x_xiaolin",
    "讯飞小包": "x_xiaobao",
    "讯飞小瑞": "x_xiaonuo_novel",
    "讯飞萌小新": "x_xiaoxin",
    "讯飞小南": "x_xiaonan",
    "讯飞小东": "x_xiaodong",
    "讯飞小婧": "x_jinger",
    "讯飞诺诺": "x_xiaoai",
    "讯飞小蓉": "x_xiaorong",
    "讯飞一萍": "x_yiping",
    "Steve": "x_steve",
    "讯飞小春": "x_mengchun",
    "讯飞晓峰": "x_xiaofeng",
    "讯飞芳芳": "x_xiaofang",
    "讯飞小施": "x_xiaoshi",
    "讯飞马三爷": "x_xiaoma",
    "讯飞小王": "x_xiaowang",
    "讯飞小坤": "x_xiaokun",
    "讯飞楠楠": "x_nannan",
    "讯飞萌萌-悲伤": "x_mengmengsad",
    "讯飞宋宝宝": "x_xiaosong",
})