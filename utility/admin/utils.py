from urllib.parse import urljoin

from django.utils.html import format_html


def colored_field(value, color, condition=True):
    if not condition:
        return value
    return format_html(
        '<span style="color: {}; font-weight: bold;">{}</span>'.format(
            color,
            value,
        )
    )


def get_coverage_field(percentage, show_percentage=True):
    if show_percentage:
        return format_html(
            '''
            <progress value="{0}" max="100"></progress>
            <span style="font-weight:bold">{0}%</span>
            ''',
            percentage
        )
    return format_html(
        '''
        <progress value="{0}" max="100"></progress>
        ''',
        percentage
    )


def create_image_response(file, width=100, height=100):
    return format_html('<img src="{url}" width="{width}" height={height} />'.format(
        url=file.url,
        width=width,
        height=height,
    ))
