import cv2
import sys
import moviepy.editor as mp
import speech_recognition as sr
import time
import urlparse
import os.path


class videoProcess(object):

    def __init__(self, videoPath):
        self.videoPath = videoPath
        video_split_path = os.path.splitext(os.path.basename(urlparse.urlsplit(self.videoPath).path))
        self.videoName = video_split_path[0]

    def getVideoLengthAndFps(self):

        video = cv2.VideoCapture(self.videoPath)

        # Find OpenCV version
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

        if int(major_ver) < 3:
            fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
            total_frame_count = video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
            fps, length, seconds = self.calculateLengthAndFps(video, total_frame_count, fps)

        else:
            fps = video.get(cv2.CAP_PROP_FPS)
            total_frame_count = video.get(cv2.cv.CAP_PROP_FRAME_COUNT)
            fps, length, seconds = self.calculateLengthAndFps(video, total_frame_count, fps)

        print "=>Frames per second using: {0}".format(fps)
        print "=>Length of video: {0} minutes".format(length)
        audio_result = self.convertVideoToAudio(seconds)
        print "=>Transcription: ", str(audio_result)
        video.release()

    def calculateLengthAndFps(self, video, total_frame_count, fps):

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
                cv2.imwrite('frames/frame_' + self.videoName + '_' + str(count) + '.jpg', frame)
            count = count + 1
            cv2.waitKey(1)

        return fps, minutes, seconds

    def convertVideoToAudio(self, length):
        start = 0
        end = 10
        text = ''
        remaining_length = 0

        length = int(round(length))
        for i in range(0, length):

            if remaining_length < 10 and remaining_length > 0:
                if i % remaining_length == 0:
                    clip = mp.VideoFileClip(self.videoPath).subclip(start, end)
                    clip.audio.write_audiofile("audio/" + self.videoName + '_' + str(i) + ".wav")
                    text += str(self.convertAudioToText("audio/" + self.videoName + '_' + str(i) + ".wav"))

            elif i % 10 == 0:
                clip = mp.VideoFileClip(self.videoPath).subclip(start, end)
                clip.audio.write_audiofile("audio/" + self.videoName + '_' + str(i) + ".wav")
                text += str(self.convertAudioToText("audio/" + self.videoName + '_' + str(i) + ".wav"))

                start = i + 1
                end = i + 10
                remaining_length = length - i

        return text

    def convertAudioToText(self, audioPath):
        r = sr.Recognizer()
        with sr.WavFile('audio/audio.wav') as source:  # for now I used hardcoded path, will change later
            audio = r.record(source)  # extract audio data from the file

        try:
            print("Transcription: " + r.recognize_google(audio, show_all=False))  # recognize speech using Google Speech Recognition
            return r.recognize_google(audio)
        except LookupError:  # speech is unintelligible
            print("Could not understand audio")
            return 'Could not understand audio'

videoPath = sys.argv[1]
videoObject = videoProcess(videoPath)
videoObject.getVideoLengthAndFps()
