from flask import Flask
import config

from exts import mail
from celery_task import make_celery
from view import views_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    mail.init_app(app)
    app.register_blueprint(views_bp)
    return app


app = create_app()
celery = make_celery(app)

if __name__ == '__main__':
    app.run()
