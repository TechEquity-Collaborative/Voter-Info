from django.conf.urls import url, include

from django.contrib import admin
from rest_framework import routers

from . import views

admin.autodiscover()

# this namespaces URLS in this django app...
app_name = 'districts'

router = routers.DefaultRouter()
# ... so this will be /districts/ -> JSON list of offices
router.register(r'', views.DistrictViewSet)

urlpatterns = [
    # Wire up our API using automatic URL routing from the Django REST Framework (DRF)
    url(r'^', include(router.urls)),
]
