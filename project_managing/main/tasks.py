
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_project_created_notification(project_id: int, project_title: str, user_email: str):
    subject = 'Уведомление о создании проекта'
    message = f'Вы успешно создали проект с названием {project_title}, его ID {project_id}.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])


@shared_task
def send_project_deleted_notification(project_id: int, project_title: str, user_email: str):
    subject = 'Уведомление об удалении проекта'
    message = f'Вы успешно удалили проект с названием {project_title}, его ID {project_id}.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
