import re

from jalali_date import datetime2jalali, date2jalali

TOMAN = 'تومان'
RIAL = 'ریال'


def ir_currency(amount, suffix=TOMAN):
    if amount is None:
        return '---'
    return '{:,} {}'.format(amount, suffix)


def jalali_strfdatetime(input_datetime, output_format='%H:%M %Y/%m/%d'):
    if not input_datetime:
        return '-'
    return datetime2jalali(input_datetime).strftime(output_format)


def jalali_strfdate(input_date, output_format='%Y/%m/%d'):
    if not input_date:
        return '-'
    return date2jalali(input_date).strftime(output_format)


def make_bold_html(text):
    return '<b>{}</b>'.format(text)


camel_to_snake_pat1 = re.compile('(.)([A-Z][a-z]+)')
camel_to_snake_pat2 = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(name):
    name = camel_to_snake_pat1.sub(r'\1_\2', name)
    return camel_to_snake_pat2.sub(r'\1_\2', name).lower()
