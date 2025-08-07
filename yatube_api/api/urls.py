from rest_framework import routers
from rest_framework.authtoken import views

from django.urls import include, path


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
