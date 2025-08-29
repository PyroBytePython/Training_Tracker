import threading
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def send_verification_email(user, code):
    def _send_email():
        try:
            subject = 'Подтверждение регистрации в Workout Tracker'

            text_content = (
                f"Здравствуйте, {user.username}!\n\n"
                f"Ваш код подтверждения: {code}\n\n"
                f"Введите его на сайте для завершения регистрации.\n\n"
                f"С уважением,\nКоманда Workout Tracker"
            )

            html_content = render_to_string('users/verification_email.html', {
                'user': user,
                'code': code,
            })

            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,   # 👈 всегда совпадает с авторизованным SMTP-пользователем
                [user.email]                 # 👈 сюда письмо реально уходит
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            print(f"[EMAIL] Код отправлен на {user.email} ({code})")

        except Exception as e:
            print(f"[EMAIL][ERROR] Ошибка при отправке на {user.email}: {e}")

    threading.Thread(target=_send_email, daemon=True).start()
