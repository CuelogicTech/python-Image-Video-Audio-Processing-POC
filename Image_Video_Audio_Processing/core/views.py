import os
import json

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView

from .models import Picture,Audio,Video
from .response import JSONResponse, response_mimetype
from .serialize import serialize

# Importing Core files for processing
from image_processing import ImageProcessing
from process_video import processAudioVideo


def index(request):
    return render(request, 'core/home.html')


class PictureCreateView(CreateView):
    model = Picture
    fields = "__all__"

    def form_valid(self, form):
        temp = []
        sortedcolors={}
        resultant_face_detected =""
        self.object = form.save()
        files = [serialize(self.object)]
        file_path = settings.MEDIA_ROOT+files[0]['name']

        imageprocessor = ImageProcessing(file_path)
        face_detected = imageprocessor.faceDetection()
        face_count = face_detected['face_count']
        if 'result_image' in face_detected:
            resultant_face_detected = face_detected['result_image']
        extract_text = imageprocessor.extract_text()
        if len(extract_text['text']) == 0:
            extract_text = "Cannot detect the words"
        else:
            extract_text = extract_text['text']

        getImageColor = imageprocessor.getImageColor()

        checkDuplicateImage = imageprocessor.checkDuplicateImage(settings.MEDIA_ROOT+'pictures/')
        for each in checkDuplicateImage:
            temp.append("media"+(each.split('/media')[1]))

        data = {'files': files, 'face_count' : face_count,'getImageColor' : getImageColor,
                'checkDuplicateImage' : temp,'extract_text' :extract_text ,'face_detected' : resultant_face_detected}

        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        return HttpResponse(content=json.dumps(form.errors), status=400, content_type='application/json')


class BasicPictureCreateView(PictureCreateView):
    template_name_suffix = '_base'


class AudioCreateView(CreateView):
    model = Audio
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        file_path = settings.MEDIA_ROOT+files[0]['name']

        audioprocessor = processAudioVideo(file_path)
        get_type = audioprocessor.validateExt()

        if get_type == "audio":
            output_audio = audioprocessor.processAudio(get_type)

            if len(output_audio['message']) == 0:
                message = "Cannot detect the words"
            else:
                message = output_audio['message']

            data = {'files': files,
                   'message' : message
                }
        else:
            data = {'files': files,
                    'error':"Invalid File Format"
                }

        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        print data
        return HttpResponse(content=data, status=400, content_type='application/json')


class BasicAudioCreateView(AudioCreateView):
    template_name_suffix = '_base'


class VideoCreateView(CreateView):
    model = Video
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        file_path = settings.MEDIA_ROOT+files[0]['name']

        videoprocessor = processAudioVideo(file_path)
        get_type = videoprocessor.validateExt()
        if get_type == "video":
            output_video = videoprocessor.processVideo(get_type)
            if 'fps' in output_video:

                if len(output_video['message']) == 0:
                    message = "Cannot detect the words"
                else:
                    message = output_video['message']

                data = {'files': files,
                        'fps' : output_video['fps'],
                        'medialength': output_video['medialength'],
                        'message' : message,
                        'height_video' :output_video['height'],
                        'width_video':output_video['width'],
                        'quality':output_video['quality']
                        }
            else:
                data = {'files': files,
                        'error':output_video['error']
                        }
        else:
            data = {'files': files,
                    'error':"Invalid File Format"
                    }
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')

class BasicVideoCreateView(VideoCreateView):
    template_name_suffix = '_base'
