import fastapi_mail

email_config = fastapi_mail.ConnectionConfig(
    MAIL_USERNAME ="username",
    MAIL_PASSWORD = "**********",
    MAIL_FROM="tetris.tech@gmail.com",
    MAIL_PORT=8025,
    MAIL_SERVER="mailpit",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = False,
    VALIDATE_CERTS = True
)
