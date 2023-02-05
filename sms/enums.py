from django.conf import settings

SMS_USAGE_TYPE_LOGIN = 'LOGIN'
SMS_USAGE_TYPE_SIGNUP = 'SIGNUP'

SMS_USAGE_TYPES = (
    (SMS_USAGE_TYPE_LOGIN, 'ورود'),
    (SMS_USAGE_TYPE_SIGNUP, 'ثبت نام')
)

GYMTIME_SMS_CANCELLED = 'CANCELLED'
GYMTIME_SMS_CREATED = 'CREATED'
GYMTIME_SMS_AWAITING_SENDING = 'AWAITING_SENDING'
GYMTIME_SMS_SENT = 'SENT'

GYMTIME_SMS_STATE = (
    (GYMTIME_SMS_CANCELLED, 'ارسالش کنسل شده'),
    (GYMTIME_SMS_CREATED, 'ساخته شده'),
    (GYMTIME_SMS_AWAITING_SENDING, 'در انتظار ارسال'),
    (GYMTIME_SMS_SENT, 'ارسال شده')
)

KAVENEGAR_MESSAGE_LENGTH_LIMIT = 'MESSAGE_LENGTH_LIMITS'
KAVENEGAR_RECEPTORS_LIMIT = 'RECEPTORS_LIMIT'
KAVENEGAR_LIMITS = {
    KAVENEGAR_MESSAGE_LENGTH_LIMIT: 900,
    KAVENEGAR_RECEPTORS_LIMIT: 200,
}

GYMTIME_SEND_SMS_MINIMUM_DELAY_MINUTES = 5
