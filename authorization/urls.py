from django.urls import re_path as url
from django.urls import path, include
from oauth2_provider.views import AuthorizationView


from authorization.views import RegisterView
from referral.views import TokenRevokeView, TokenViewCustom

app_name = 'authorization'


oauth_urlpatterns = [
    path('revoke-token/', TokenRevokeView.as_view(), name='revoke-token'),
    path('token/', TokenViewCustom.as_view(), name='token'),
    url(r'^authorize/?$', AuthorizationView.as_view(), name="authorize"),
]

urlpatterns = [
    path('reg/', RegisterView.as_view()),
    path('login/', include((oauth_urlpatterns, 'rest_framework_social_oauth2'), namespace='rest_framework_social_oauth2'))
]
