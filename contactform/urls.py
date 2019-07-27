from django.conf.urls import url

from contactform.views import index

urlpatterns = [
    url(r'^(?P<form_model_id>[0-9]+)/$', index)
]
