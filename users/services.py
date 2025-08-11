from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def send_verification_email(user, code):
    subject = 'Подтверждение регистрации в Workout Tracker'

    # Текстовый вариант (для почтовых клиентов без поддержки HTML)
    text_content = f'''
    Здравствуйте, {user.username}!

    Ваш код подтверждения: {code}

    Введите его на сайте для завершения регистрации.

    С уважением,
    Команда Workout Tracker
    '''

    # HTML вариант
    html_content = render_to_string('users/verification_email.html', {
        'user': user,
        'code': code,
    })

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
