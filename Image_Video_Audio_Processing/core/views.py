import json

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from django.views.generic import CreateView, DeleteView, ListView
from .models import Picture,Audio,Video
from .response import JSONResponse, response_mimetype
from .serialize import serialize

def index(request):
    return render(request, 'core/home.html')

class PictureCreateView(CreateView):
    model = Picture
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
