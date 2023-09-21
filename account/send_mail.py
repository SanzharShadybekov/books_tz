from django.core.mail import send_mail

HOST = '54.145.126.104'


def send_confirmation_email(user, code):
    print(user, code)
    link = f'http://{HOST}/api/v1/accounts/activate/{code}/'
    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Что активировать ваш аккаунт нужно перейти по ссылке ниже:'
        f'\n{link}'
        f'\nСсылка работает один раз!',
        'johnsnowtest73@gmail.com',
        [user],
        fail_silently=False,
    )
