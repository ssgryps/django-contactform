from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'^(?P<form_model_id>[0-9]+)/$', 'contactform.views.index')
)
