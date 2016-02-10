
from django.conf.urls import patterns, url
from views import *


urlpatterns = patterns('core.views',
  url(r'^image/basic/$', BasicPictureCreateView.as_view(), name='upload-basic'),
  url(r'^audio/basic/$', BasicAudioCreateView.as_view(), name='upload-audio'),
  url(r'^video/basic/$', BasicVideoCreateView.as_view(), name='upload-video'),
)
