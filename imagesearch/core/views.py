#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse


def home(request):
    return render(request, 'base.html', {})


def search(request):
    if request.method == 'GET':
        img_name = request.GET.get('f')
        return render(request, 'base.html',
                      {'media_url': settings.MEDIA_URL,
                      'image_name': img_name})


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        is_file = request.FILES.get('file')
        if is_file:
            path = default_storage.save(settings.MEDIA_ROOT + '/'
                    + str(is_file.name), ContentFile(is_file.read()))
            msg = 'File has been uploaded'
            response = {'filename': is_file.name,
                        'media_url': settings.MEDIA_URL}
            return HttpResponse(json.dumps(response))
        else:
            msg = 'Something has went wrong, please try again.'
            return HttpResponse(msg)
    else:
        return render(request, 'base.html', {})
