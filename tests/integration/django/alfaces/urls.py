from django.conf.urls import url

from alfaces.donothing.views import index

urlpatterns = [
    url(r'', index)
]
