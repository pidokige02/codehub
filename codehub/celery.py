# config/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codehub.settings')  # 프로젝트 이름에 맞게 변경

app = Celery('codehub')
app.config_from_object('django.conf:settings', namespace='CELERY')

# celery가 task로 데코레이팅된 일들을 다 알아서 찾는다.
# 실질적으로 celery 인스턴스가 만들어지는 code 이다!
app.autodiscover_tasks()
