import cv2
import sys
from pydub import AudioSegment
import moviepy.editor as mp
import speech_recognition as sr
import time
import urlparse
import os.path
import re
import subprocess
import shlex
import json


class processAudioVideo(object):

    def __init__(self, filePath):
        self.frameDirectory = 'avprocessing/frames/'
        self.audioDirectory = 'avprocessing/audio/'

        if not os.path.exists(self.frameDirectory):
            os.makedirs(self.frameDirectory, 0777)

        if not os.path.exists(self.audioDirectory):
            os.makedirs(self.audioDirectory, 0777)

        self.filePath = filePath
        file_split_path = os.path.splitext(os.path.basename(urlparse.urlsplit(self.filePath).path))
        self.fileName = file_split_path[0]

    def processVideo(self, mediaType):

        video = cv2.VideoCapture(self.filePath)
        self.fileType = mediaType

        # Find OpenCV version
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

        if int(major_ver) < 3:
            fps = video.get(cv2.cv.CV_CAP_PROP_FPS)

            if str(fps) == 'nan':
                # print 'The video file is seems to be corrupted, please upload another file.'
                return response_dict = {
                    'error' : 'The video file is seems to be corrupted, please upload another file.'
                }

            total_frame_count = video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
            fps, length, seconds = self.calculateVideoLengthAndFps(video, total_frame_count, fps)

        else:
            fps = video.get(cv2.CAP_PROP_FPS)
            
            if str(fps) == 'nan':
                # print 'The video file is seems to be corrupted, please upload another file.'
                return response_dict = {
                    'error' : 'The video file is seems to be corrupted, please upload another file.'
                }
            
            total_frame_count = video.get(cv2.cv.CAP_PROP_FRAME_COUNT)
            fps, length, seconds = self.calculateVideoLengthAndFps(video, total_frame_count, fps)

        response = self.processMedia(seconds, self.fileType)
        height, width = self.findVideoResolution()

        # print "=>Frames per second using: {0}".format(fps)
        # print "=>Length of video: {0} minutes".format(length)
        # print "=>Video resolution: height-> {0}, width-> {1}".format(height, width)
        # if not response.strip():
        #     print "=>Exception: Cannot detect the words"
        # else:
        #     print "=>Transcription: ", str(response)

        response_dict = {
            'fps' : fps,
            'medialength': length,
            'message' : str(response),
            'height'  : height,
            'width'   : width
        }
        return response_dict

        video.release()
        sys.exit()

    def calculateVideoLengthAndFps(self, video, total_frame_count, fps):

        count = 1
        seconds = (total_frame_count / fps)
        minutes = time.strftime("%H:%M:%S", time.gmtime(seconds))

        if video.isOpened():
            is_exist, frame = video.read()
        else:
            is_exist = False

        while is_exist:
            is_exist, frame = video.read()
            if count % 30 == 0:
                cv2.imwrite(self.frameDirectory + 'frame_' + self.fileName + '_' + str(count) + '.jpg', frame)
            count = count + 1
            cv2.waitKey(1)

        return fps, minutes, seconds

    def processAudio(self, mediaType):

        self.fileType = mediaType
        sound = AudioSegment.from_file(self.filePath)
        sound.export(self.audioDirectory + self.fileName + '.wav', format="wav")
        self.filePath = self.audioDirectory + self.fileName + '.wav'

        seconds = (len(sound) / 1000)
        actual_length = time.strftime("%H:%M:%S", time.gmtime(seconds))
        response = self.processMedia(seconds, self.fileType)

        # print "=>Length of audio: {0} minutes".format(actual_length)
        # if not response.strip():
        #     print "=>Exception: Cannot detect the words"
        # else:
        #     print "=>Transcription: ", str(response)

        response_dict = {
            'fps' : 0,
            'medialength': actual_length,
            'message' : str(response)
        }
        return response_dict

        sys.exit()

    def processMedia(self, actual_length, mediaType):
        start = 0
        end = 10
        text = ''
        length = int(actual_length)
        func = self.processVideoChunks if mediaType == 'video' else self.processAudioChunks
        
        # if the length of the video is less than 10 secs.
        if(length > 10):
            quotient = divmod(length, 10)
            quo1 = quotient[0]
            quo2 = quotient[1]
            length = quo1 + 1
        else:
            int1 = re.split('[ .]', str(actual_length))

            quo1 = 0
            quo2 = int(int1[0])
            length = 1

        for i in range(0, length):

            if quo1 == i and quo2 > 0:
                end = (start + quo2) - 1
                text += func(start, end, i)

            else:
                text += func(start, end, i)
                start = end + 1
                end = end + 10

        return text

    def processAudioChunks(self, start, end, i):
        clip = mp.AudioFileClip(self.filePath).subclip(start, end)
        clip.write_audiofile(str(self.audioDirectory) + str(self.fileName) + '_' + str(i) + ".wav")
        text = str(self.convertAudioToText(str(self.audioDirectory) + str(self.fileName) + '_' + str(i) + ".wav"))
        return text

    def processVideoChunks(self, start, end, i):
        clip = mp.VideoFileClip(self.filePath).subclip(start, end)
        clip.audio.write_audiofile(str(self.audioDirectory) + str(self.fileName) + '_' + str(i) + ".wav")
        text = str(self.convertAudioToText(str(self.audioDirectory) + str(self.fileName) + '_' + str(i) + ".wav"))
        return text

    def convertAudioToText(self, audioPath):
        r = sr.Recognizer()
        with sr.WavFile(audioPath) as source:  # for now I used hardcoded path, will change later
            audio = r.record(source)  # extract audio data from the file

        try:
            # recognize speech using Google Speech Recognition
            return r.recognize_google(audio) + ' '
        except:
            # print("Could not understand audio") # speech is unintelligible
            return ''


    # function to find the resolution of the input video file
    def findVideoResolution(self):
        cmd = "ffprobe -v quiet -print_format json -show_streams"
        args = shlex.split(cmd)
        args.append(self.filePath)
        # run the ffprobe process, decode stdout into utf-8 & convert to JSON
        ffprobeOutput = subprocess.check_output(args).decode('utf-8')
        ffprobeOutput = json.loads(ffprobeOutput)

        # find height and width
        height = ffprobeOutput['streams'][0]['height']
        width = ffprobeOutput['streams'][0]['width']

        return height, width

    def validateExt(self):

        file_path, filename = os.path.split(self.filePath)
        shortname, extension = os.path.splitext(filename)
        is_path_exists = os.path.isfile(self.filePath)
        
        if not is_path_exists:
            return response_dict = {
                'error' : 'File doesn\'t exists.'
            }

        video_extension_list = ['.mp4']
        audio_extension_list = ['.wav', '.mp3', '.ogg', '.mpeg', '.wma', '.m4a']

        if extension.lower() in video_extension_list:
            return 'video'
        elif extension.lower() in audio_extension_list:
            return 'audio'
        else:
            return "Invalid File Format"

filePath = sys.argv[1]
fileObject = processAudioVideo(filePath)
responseObj = fileObject.validateExt()

if str(responseObj) == 'video':
    fileObject.processVideo('video')
elif str(responseObj) == 'audio':
    fileObject.processAudio('audio')
else:
    print '\n', '~~' * 40
    print "Invalid format.. Please provide ('.mp4', '.wav', '.mp3', '.ogg', '.mpeg', '.wma', '.m4a') format file"
    print '~~' * 40, '\n'
