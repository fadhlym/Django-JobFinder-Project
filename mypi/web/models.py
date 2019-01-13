from django.db import models
from django.contrib.auth.models import Permission, User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    perusahaan = models.CharField(max_length=30)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class kerja(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nama_kerja = models.CharField(max_length=100)
    exp = models.PositiveIntegerField()
    gender = models.CharField(max_length=30)
    sal = models.CharField(max_length=30, default='Classified')
    job_type = models.CharField(max_length=30)
    umur = models.CharField(max_length=30)
    kota = models.CharField(max_length=100)
    job_req = models.TextField(default='')
    jobs_desc = models.TextField(default='')
    comp_name = models.CharField(max_length=50)
    comp_address = models.TextField(default='')
    comp_desc = models.TextField(default='')
    comp_phone = models.CharField(max_length=12)
    comp_sites = models.CharField(max_length=40)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_kerja

