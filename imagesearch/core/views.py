#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import traceback
import json
import uuid
import re
import tempfile
import wand.image
import wand.display
import wand.exceptions
import os

from os import listdir
from os.path import isfile, join

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse




#local stuff
from img import persisted_img
im = persisted_img()

BANK_PATH = 'static/img/bank'
BANK_THUMB_PATH = join(BANK_PATH,'thumb')

def get_images(path):
    #Need to change this
    return filter(
        lambda x : re.search('\.(jpg|jpeg|png)', x.lower()) != None,
        [join(path, f) for f in listdir(path) if isfile(join(path,f))]
    )

def get_bank_images():
    return get_images(BANK_PATH)

def get_thumb_images():
    return get_images(BANK_THUMB_PATH)


def home(request):
    return render(request, 'base.html', {})


def search(request):
    if request.method == 'GET':
        img_name = request.GET.get('f')
        file_path = join(settings.MEDIA_ROOT, img_name)
        file = open(file_path, 'r+')
        if file:
            # try:
            with wand.image.Image(filename=file_path) as img:
                img.resize(256, 256)
                img.save(filename=file_path)
            matches = im.match(file_path, limit=10)
            return render(request, 'base.html',
                          {'media_url': settings.MEDIA_URL,
                          'image_name': img_name,
                          'image_matches': matches}
                        )

            # except:
            #     traceback.print_exc()
            #     return render(request, 'base.html',
            #                   {'media_url': settings.MEDIA_URL,
            #                   'image_name': img_name,
            #                   'image_matches': []}
            #                 )


@csrf_exempt
def upload_file(request):
    # Save the image object in the media folder and proceed to search
    if request.method == 'POST':
        is_file = request.FILES.get('file')
        if is_file:
            if not os.path.exists(settings.MEDIA_ROOT + '/' + str(is_file.name)):
                default_storage.save(settings.MEDIA_ROOT + '/'
                    + str(is_file.name), ContentFile(is_file.read()))
            response = {'filename': is_file.name,
                        'media_url': settings.MEDIA_URL}
            return HttpResponse(json.dumps(response))
        else:
            msg = 'Something has went wrong, please try again.'
            return HttpResponse(msg)
    else:
        return render(request, 'base.html', {})

def upload_file_bank(request):
    # Save images in the bank
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            # Create the temporary file for search operation
            file_path = default_storage.save(settings.MEDIA_ROOT + '/'
                    + str(file.name), ContentFile(file.read()))
            guid = str(uuid.uuid4().get_hex().upper()[0:12]) + '.jpg'
            dstfile = join(
                BANK_PATH,
                guid
            )
            dstfile_thumb = join(
                BANK_THUMB_PATH,
                guid
            )
            try:
                with wand.image.Image(filename=file_path) as img:
                    img.save(filename=dstfile)
                    img.resize(256, 256)
                    img.save(filename=dstfile_thumb)
                    im.add_image(dstfile_thumb)
            except wand.exceptions.MissingDelegateError:
                return HttpResponse(json.dumps({'success':False ,'error': 'input is not a valid image'}))
            return HttpResponse(json.dumps({'success':True ,'error': ''}))
        return HttpResponse( json.dumps({'success':False ,'error': 'Not a valid image file'}))

