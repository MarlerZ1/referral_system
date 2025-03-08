import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authorization.models import User
from referral.models import ReferralCode


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

                    code.clean()
                    code.owner = user
                    code.save()
                except ValueError:
                    print("Invalid UUID format")
                except ValidationError:
                    print("Code isn't active")
                except ObjectDoesNotExist:
                    print("Incorrect code")
        return user