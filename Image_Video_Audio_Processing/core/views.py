import json
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from django.views.generic import CreateView, DeleteView, ListView
from .models import Picture,Audio,Video
from .response import JSONResponse, response_mimetype
from .serialize import serialize

from image_processing import ImageProcessing

def index(request):
    return render(request, 'core/home.html')

class PictureCreateView(CreateView):
    model = Picture
    fields = "__all__"

    def form_valid(self, form):
        temp = []
        resultant_face_detected =""
        self.object = form.save()
        files = [serialize(self.object)]
        file_path = settings.MEDIA_ROOT+'pictures/'+files[0]['name']
        imageprocessor = ImageProcessing(file_path)
        face_detected = imageprocessor.faceDetection()
        face_count = face_detected['face_count']
        # if 'result_image' in face_detected:
        #     resultant_face_detected = face_detected['result_image']
        # extract_text = imageprocessor.extract_text()
        getImageColor = imageprocessor.getImageColor()
        checkDuplicateImage = imageprocessor.checkDuplicateImage(settings.MEDIA_ROOT+'pictures/')
        for each in checkDuplicateImage:
            temp.append("media"+(each.split('/media')[1]))
        data = {'files': files, 'face_count':face_count,'getImageColor':getImageColor,
                'checkDuplicateImage':temp,
                'extract_text':'extract_text','face_detected':resultant_face_detected}
        #         'imageValidation':imageValidation}
        print data
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        print form.errors

        data = {'errors': form.errors}
        return HttpResponse(content=json.dumps(data), status=400, content_type='application/json')

class BasicPictureCreateView(PictureCreateView):
    template_name_suffix = '_base'


class AudioCreateView(CreateView):
    model = Audio
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        print files
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')

class BasicAudioCreateView(AudioCreateView):
    template_name_suffix = '_base'


class VideoCreateView(CreateView):
    model = Video
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')

class BasicVideoCreateView(VideoCreateView):
    template_name_suffix = '_base'
