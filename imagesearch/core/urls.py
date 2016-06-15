from django.conf.urls import patterns, url
from views import *


urlpatterns = patterns('core.views',
  url(r'search/$', search, name='search'),
  url(r'fileupload/upload-file/$',upload_file, name='upload_file'),
  url(r'fileupload/upload-file-bank/$',upload_file_bank, name='upload_file_bank')
)
