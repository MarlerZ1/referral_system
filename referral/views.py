from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_social_oauth2.views import TokenView, RevokeTokenView

from authorization.models import User
from referral.models import ReferralCode
from referral.serializers import UserReferralSerializer, ReferralCodeCreateSerializer, ReferralCodeDeleteSerializer, \
    TokenCreateSerializer, TokenRevokeSerializer, ExpiresAtSerializer


class EmailReferralCodeView(APIView):
    serializer_class = None

    def get(self, request, email, *args, **kwargs):
        if not email:
            return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)

            code = ReferralCode.objects.filter(owner=user).first()
            if code:
                return Response({"referral_code": str(code.uuid)}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not have a referral code."}, status=status.HTTP_404_NOT_FOUND)

        except ObjectDoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class ReferralListView(APIView):
    serializer_class = None

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        code = ReferralCode.objects.filter(owner=user).first()

        referrals = User.objects.filter(referral_code=code) if code else []

        serializer = UserReferralSerializer(referrals, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReferralCodeCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=ExpiresAtSerializer)
    def post(self, request):
        serializer = ReferralCodeCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "The referral code has been created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReferralCodeDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        serializer = ReferralCodeDeleteSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.delete()

            return Response({
                "message": "The referral code has been deleted",
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenRevokeView(RevokeTokenView):
    serializer_class = TokenRevokeSerializer

    @extend_schema(request=TokenRevokeSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenViewCustom(TokenView):
    serializer_class = TokenCreateSerializer

    @extend_schema(request=TokenCreateSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
