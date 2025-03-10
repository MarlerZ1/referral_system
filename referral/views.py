from adrf.views import APIView
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.response import Response

from authorization.models import User
from referral.models import ReferralCode
from referral.serializers import UserReferralSerializer, ReferralCodeCreateSerializer, ReferralCodeDeleteSerializer, \
    ExpiresAtSerializer, ReferralCodeSerializer
from utils.Cache import get_cached_code


class EmailReferralCodeView(APIView):
    serializer_class = None

    async def get(self, request, email, *args, **kwargs):
        if not email:
            return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            code = await  get_cached_code(email=email)
            if code:
                return Response({"User referral code:": str(ReferralCodeSerializer(code).data)}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not have a referral code."}, status=status.HTTP_404_NOT_FOUND)

        except ObjectDoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

@sync_to_async
def get_users_by_referral_code(referral_code):
        return User.objects.filter(referral_code=referral_code)


class ReferralListView(APIView):
    serializer_class = None

    async def get(self, request, user_id, *args, **kwargs):
        try:
            user = await User.objects.aget(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        code = await get_cached_code(owner=user)

        referrals = []
        async for user in await sync_to_async(User.objects.filter)(referral_code=code):
            referrals.append(user)


        return Response(UserReferralSerializer(referrals, many=True).data, status=status.HTTP_200_OK)


class ReferralCodeCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=ExpiresAtSerializer)
    async def post(self, request):
        serializer = ReferralCodeCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            await sync_to_async(serializer.save)()
            return Response({"message": "The referral code has been created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReferralCodeDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    async def delete(self, request):
        serializer = ReferralCodeDeleteSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            await serializer.delete()
            return Response({"message": "The referral code has been deleted", }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
