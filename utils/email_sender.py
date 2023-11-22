from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def templated_email_send(
    subject: str, send_to: list[str], context: dict, template: str, email_from=None
):
    html_message = render_to_string(template, context=context)
    plain_message = strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=email_from,
        to=send_to,
    )

    message.attach_alternative(html_message, "text/html")
    message.send()
    return True
