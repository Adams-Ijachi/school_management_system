from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)

        if instance.user_type == 2:
            Staff.objects.create(admin=instance, phone_number="", profile_Image="", address="", current_position="")

        if instance.user_type == 3:
            Student.objects.create(admin=instance, grade=Class.objects.get(id=1), address="", profile_Image="",
                                   gender="",
                                   parent=Parent.objects.get(id=1))

        if instance.user_type == 4:
            Parent.objects.create(admin=instance, phone_number="", gender="", address="", profile_Image="")


@receiver(post_save,sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):

    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
    if instance.user_type == 4:
        instance.parent.save()