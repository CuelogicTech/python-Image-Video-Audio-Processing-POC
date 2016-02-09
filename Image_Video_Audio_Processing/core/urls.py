
from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('capital_one.views',
  url(r'^get/image/results/', 'image_processing', name='image_processing'),
  url(r'^get/audio/results/', 'audio_processing', name='audio_processing'),
  url(r'^get/video/results/', 'video_processing', name='video_processing')
)
