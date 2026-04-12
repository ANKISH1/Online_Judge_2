from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Submissions
from apps.users.models import Profile
from django.db.models import F

@receiver(post_save, sender=Submissions)
def problems_attempted(sender, instance,**kwargs):
    if instance.verdict == "ACCEPTED":
        profile = Profile.objects.get(user= instance.user)
        profile.problems_solved = F('problems_solved')+1
        profile.save()