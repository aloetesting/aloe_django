from django.conf.urls import url

from leaves.views import index

urlpatterns = [
    url(r'', index),
]
