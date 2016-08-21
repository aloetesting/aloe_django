from django.conf.urls import url

from donothing.views import index

urlpatterns = [
    url(r'', index)
]
