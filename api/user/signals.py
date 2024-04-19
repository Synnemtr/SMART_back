from django.db.models.signals import post_save
from django.dispatch import receiver
from api.user.models import User
from api.user.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create_profile(user=instance)
