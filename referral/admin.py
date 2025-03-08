from django.contrib import admin

from referral.models import ReferralCode


# Register your models here.
@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'created_at', "expires_at"]