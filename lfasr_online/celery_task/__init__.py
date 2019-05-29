from celery import Celery
import config

celery = Celery('celery_app',
                broker=config.CELERY_BROKER_URL,
                backend=config.CELERY_RESULT_BACKEND,
                include=['app',  'tasks']
                )


def make_celery(app):
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


