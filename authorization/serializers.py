import uuid

import httpx
import pytz
from adrf.serializers import Serializer
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authorization.models import User
from referral.models import ReferralCode
from referral_system.settings import HUNTER_API_KEY, HUNTER_API_URL


class RegisterSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "referral_code", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}


    def create(self, validated_data):
        referral_code = validated_data.pop("referral_code", None)

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)

            if referral_code:
                try:
                    referral_code = uuid.UUID(referral_code, version=4)
                    code = ReferralCode.objects.get(uuid=referral_code)
                except ValueError:
                    raise ValidationError("Invalid UUID format")
                except ObjectDoesNotExist:
                    raise ValidationError("Incorrect code")

                if code.expires_at < timezone.now():
                    raise ValidationError("Code isn't active")

                user.referral_code = code
                user.save()
        return user

    async def check_email(self, email):
        url = f"{HUNTER_API_URL}?email={email}&api_key={HUNTER_API_KEY}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        status = response.json()['data']['status']
        if status == 'invalid':
            raise serializers.ValidationError("Email is incorrect")

class ClientData(Serializer):
    client_id = serializers.CharField(required=True)
    client_secret = serializers.CharField(required=True)

class TokenRevokeSerializer(ClientData):
    token = serializers.CharField(required=True)