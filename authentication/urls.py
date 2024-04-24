from django.urls import path
from django.conf.urls import include

from authentication.views import *

from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

app_name = 'authentication'

urlpatterns = [
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register', RegisterView.as_view(), name='auth_register'),
    path('logout', TokenBlacklistView.as_view(), name='auth_logout'),
    path('refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
    # path(r'^auth/rest-auth/', include('rest_auth.urls')),
]
