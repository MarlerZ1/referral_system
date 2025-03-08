from django.utils import timezone
from rest_framework import serializers

from authorization.models import User
from referral.models import ReferralCode


class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ['uuid', 'created_at', 'expires_at']

class UserReferralSerializer(serializers.ModelSerializer):
    referral_code = ReferralCodeSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'referral_code']


class ReferralCodeCreateSerializer(serializers.ModelSerializer):
    expires_at = serializers.DateTimeField()
    class Meta:
        model = ReferralCode
        fields = ['expires_at']

    def validate_expires_at(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("The expiration date cannot be in the past")
        return value

    def create(self, validated_data):
        user = self.context['request'].user

        referral_code = ReferralCode.objects.filter(owner=user).first()
        if referral_code:
            raise serializers.ValidationError("You already have an active referral code")

        referral_code = ReferralCode.objects.create(**validated_data, owner=user)

        user.own_referral_code = referral_code
        user.save()

        return referral_code

class ReferralCodeDeleteSerializer(serializers.Serializer):
    def validate(self, data):
        user = self.context['request'].user

        referral_code = ReferralCode.objects.filter(owner=user).first()
        if not referral_code:
            raise serializers.ValidationError("You don't have an active referral code")
        return data

    def delete(self):
        user = self.context['request'].user

        referral_code = ReferralCode.objects.filter(owner=user).first()
        if referral_code:
            referral_code.delete()