
from contactform.views import index
from django.urls import re_path

urlpatterns = [
    re_url(r'^(?P<form_model_id>[0-9]+)/$', index)
]
