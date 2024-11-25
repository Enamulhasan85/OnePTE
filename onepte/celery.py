# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery

# # Set the default Django settings module for Celery
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onepte.settings')

# app = Celery('onepte')

# # Load configuration from Django settings, using the CELERY namespace
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Autodiscover tasks in all registered Django apps
# app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')


# app.conf.update(
#     task_serializer='json',
#     accept_content=['json'],
#     result_serializer='json',
#     timezone='UTC',
#     enable_utc=True,
#     worker_hijack_root_logger=False,  # Prevent issues with root logger
#     worker_redirect_stdouts_level='INFO',
#     worker_log_color=False,  # Disable colors in the worker logs
# )

