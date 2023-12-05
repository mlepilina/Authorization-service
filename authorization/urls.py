from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from authorization.apps import AuthorizationConfig
from authorization.views import UserServiceView, UserInfoView, UserInviteView

app_name = AuthorizationConfig.name

urlpatterns = [
    path('authorization/', UserServiceView.as_view(), name='authorization'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('info/', UserInfoView.as_view(), name='info'),
    path('info/invite/', UserInviteView.as_view(), name='invited')
]
