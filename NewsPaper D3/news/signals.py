from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, PostCategory
from django.conf import settings


@receiver(m2m_changed, sender=PostCategory)
def product_created(sender, instance, action, **kwargs):
    if action == 'post_add':
        emails = User.objects.filter(
            subscriptions__category=instance.category_post_many
        ).values_list('email', flat=True)

        subject = f'Новая публикация в категории {instance.category}'

        text_content = (
            f'Публикация: {instance.title}\n'
            f'Ссылка: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Публикация: {instance.name}<br>'
            f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
            f'Ссылка</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    return
