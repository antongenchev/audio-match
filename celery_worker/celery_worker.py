from celery import Celery

app = Celery('celery_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

import celery_worker.tasks