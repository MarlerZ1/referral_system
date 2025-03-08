from django.urls import path, include
from authorization.views import RegisterView

app_name = 'authorization'

urlpatterns = [
    path('login/', include('rest_framework_social_oauth2.urls', namespace='rest_framework_social_oauth2')),
    path('reg/', RegisterView.as_view()),
]
