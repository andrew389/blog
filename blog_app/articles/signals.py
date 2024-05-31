from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article
from tg_bot.notifications import notify_new_article


@receiver(post_save, sender=Article)
async def send_article_notification(sender, instance, created, **kwargs):
    if created:
        await notify_new_article({'title': instance.title, 'body': instance.body})
