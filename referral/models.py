import uuid

from django.core.cache import cache
from django.db import models


class ReferralCode(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    owner = models.ForeignKey('authorization.User', on_delete=models.CASCADE, related_name="owner")

    def __str__(self):
        return str(self.uuid)

    def delete(self, using=None, keep_parents=False):
        cache.delete(self.owner.email)
        super().delete(using, keep_parents)
