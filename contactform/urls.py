from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<form_model_id>[0-9]+)/$', 'contactform.views.index')
]
