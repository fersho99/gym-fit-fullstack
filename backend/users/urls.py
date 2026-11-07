from django.urls import include, path
from rest_framework import routers

from users import views

router = routers.DefaultRouter()
router.register(r'users', views.UserApiViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/me/', views.UserView.as_view(), name='auth_me'),
    path('auth/register/', views.RegisterUserView.as_view(), name='register'),
    path('auth/token/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', views.RefreshView.as_view(), name='token_refresh'),
]
