from django.conf.urls import url

from kale.donothing.views import index

urlpatterns = [
    url(r'', index)
]
