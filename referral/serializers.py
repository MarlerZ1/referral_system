import pytz
from adrf.serializers import Serializer
from django.db import transaction
from rest_framework import serializers
from django.utils import timezone


from authorization.models import User
from authorization.serializers import ClientData
from referral.models import ReferralCode


class ReferralCodeSerializer(Serializer):
    class Meta:
        model = ReferralCode
        fields = ['uuid', 'created_at', 'expires_at']


class UserReferralSerializer(Serializer):
    referral_code = ReferralCodeSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'referral_code']


class ReferralCodeCreateSerializer(Serializer):
    expires_at = serializers.DateTimeField()

    class Meta:
        model = ReferralCode
        fields = ['expires_at']

    def validate_expires_at(self, value):
        if value.tzinfo:
            value = value.astimezone(pytz.utc)

        if value < timezone.now():
            raise serializers.ValidationError("The expiration date cannot be in the past")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        with transaction.atomic():
            referral_code =  ReferralCode.objects.filter(owner=user).first()
            if referral_code:
                raise serializers.ValidationError("You already have an active referral code")

            referral_code = ReferralCode.objects.create(**validated_data, owner=user)

            user.own_referral_code = referral_code
            user.save()

        return referral_code


class ReferralCodeDeleteSerializer(serializers.Serializer):
    async def delete(self):
        user = self.context['request'].user

        referral_code = await ReferralCode.objects.filter(owner=user).afirst()

        if referral_code:
            await referral_code.adelete()
        else:
            raise serializers.ValidationError("You don't have an active referral code")



class TokenCreateSerializer(ClientData):
    grant_type = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ExpiresAtSerializer(serializers.Serializer):
    expires_at = serializers.DateTimeField()
