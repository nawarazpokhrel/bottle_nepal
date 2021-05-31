

from celery import shared_task

from apps.users.email import ConfirmationEmail


@shared_task
def send_email(receipt, **kwargs):
    print('hhhhhhhhh')
    return ConfirmationEmail(context=kwargs).send(to=[receipt])

