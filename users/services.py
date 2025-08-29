import threading
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def send_verification_email(email, username, code):
    def _send_email():
        try:
            subject = 'Подтверждение регистрации в Workout Tracker'

            text_content = (
                f"Здравствуйте, {username}!\n\n"
                f"Ваш код подтверждения: {code}\n\n"
                f"Введите его на сайте для завершения регистрации.\n\n"
                f"С уважением,\nКоманда Workout Tracker"
            )

            html_content = render_to_string('users/verification_email.html', {
                'username': username,
                'code': code,
            })

            email_obj = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,  # отправитель (SMTP-аккаунт)
                [email]                   # получатель
            )
            email_obj.attach_alternative(html_content, "text/html")
            email_obj.send()

            print(f"[EMAIL] Код отправлен на {email} ({code})")

        except Exception as e:
            print(f"[EMAIL][ERROR] Ошибка при отправке на {email}: {e}")

    threading.Thread(target=_send_email, daemon=True).start()
