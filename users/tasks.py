# import uuid
# from datetime import timedelta
#
# from celery import shared_task
#
# from django.utils.timezone import now
#
# from users.models import EmailVerification, User
#
#
# @shared_task
# def send_email_verification(user_id):
#     user = User.objects.get(id=user_id)
#     expiration_date = now() + timedelta(hours=48)
#     record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration_time=expiration_date)
#     record.create_email_for_verification()
#
