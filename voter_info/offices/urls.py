from django.conf.urls import url, include

from django.contrib import admin
from rest_framework import routers

from . import views

admin.autodiscover()
app_name = 'offices'

router = routers.DefaultRouter()
router.register(r'offices', views.OfficeViewSet)
router.register(r'candidates', views.CandidateViewSet)

urlpatterns = [
    # Wire up our API using automatic URL routing from the Django REST Framework (DRF)
    url(r'^', include(router.urls)),
]
