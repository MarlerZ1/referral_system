from django.urls import path

from referral.views import EmailReferralCodeView, ReferralListView, ReferralCodeCreateView, ReferralCodeDeleteView

app_name = 'referral'

urlpatterns = [
    path('get_code/', EmailReferralCodeView.as_view()),
    path('referrals/<int:user_id>/', ReferralListView.as_view()),
    path('create/', ReferralCodeCreateView.as_view()),
    path('delete/', ReferralCodeDeleteView.as_view()),

]
