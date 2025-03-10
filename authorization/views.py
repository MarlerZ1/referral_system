from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_social_oauth2.views import RevokeTokenView, TokenView

from authorization.serializers import RegisterSerializer, TokenRevokeSerializer
from referral.serializers import TokenCreateSerializer


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    async def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        try:
            await serializer.check_email(request.data["email"])

            if await sync_to_async(serializer.is_valid)():
                await sync_to_async(serializer.save)()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenRevokeView(APIView, RevokeTokenView):
    serializer_class = TokenRevokeSerializer

    @extend_schema(request=TokenRevokeSerializer)
    async def post(self, request, *args, **kwargs):
        return await sync_to_async(super().post)(request, *args, **kwargs)


class TokenViewCustom(APIView, TokenView):
    serializer_class = TokenCreateSerializer

    @extend_schema(request=TokenCreateSerializer)
    async def post(self, request, *args, **kwargs):
        return await sync_to_async(super().post)(request, *args, **kwargs)
