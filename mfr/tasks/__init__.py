from celery import Celery

app = Celery('task')
#app.config_from_object('settings')
