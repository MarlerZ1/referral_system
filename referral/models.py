import uuid
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError


# Create your models here.
class ReferralCode(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def clean(self):
        if self.expires_at < timezone.now():
            raise ValidationError("Срок годности не может быть раньше даты создания.")

    def __str__(self):
        return str(self.uuid)