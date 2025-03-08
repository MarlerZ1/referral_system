from django.contrib.auth.models import AbstractUser
from django.db import models

from referral.models import ReferralCode


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    referral_code = models.ForeignKey(to=ReferralCode, on_delete=models.SET_NULL, null=True, blank=True, related_name="referrals")
    own_referral_code = models.OneToOneField(to=ReferralCode, on_delete=models.CASCADE, null=True, blank=True, related_name="owner")
