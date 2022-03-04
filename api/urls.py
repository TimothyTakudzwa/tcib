
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TCIBViewset

router = DefaultRouter()
router.register(r'transaction', TCIBViewset)

urlpatterns = [
    path('tcib/', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls'))
]

