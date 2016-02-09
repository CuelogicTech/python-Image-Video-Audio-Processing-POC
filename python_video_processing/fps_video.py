# The below extract the number of frames/sec (fps). We've used the cv2 library for the same.
# The code reference has been taken from the below link, it also has a code to capture the number of
# frames/sec using the system camera.
#
# Link:
# http://www.learnopencv.com/how-to-find-frame-rate-or-frames-per-second-fps-in-opencv-python-cpp/

import cv2
import datetime
import time

def getfps(path):

    video = cv2.VideoCapture(path)
    c = 1
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver) < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        total_frame_count = video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        length = (total_frame_count / fps)
        minutes = time.strftime("%H:%M:%S", time.gmtime(length))

        if video.isOpened():
            rval, frame = video.read()
        else:
            rval = False

        while rval:
            rval, frame = video.read()
            if c % 30 == 0:
                cv2.imwrite(str(c) + '.jpg', frame)
            c = c + 1
            cv2.waitKey(1)

        print "=>Frames per second using: {0}".format(fps)
        print "=>Length of video: {0} minutes".format(minutes)
    else:
        fps = video.get(cv2.CAP_PROP_FPS)
        length = video.get(cv2.cv.CAP_PROP_FRAME_COUNT)
        minutes = time.strftime("%H:%M:%S", time.gmtime(length))

        print "=>Frames per second using: {0}".format(fps)
        print "=>Length of video: %r minutes" % (minutes)

    video.release()

if __name__ == '__main__':
    import sys

    getfps(sys.argv[1])
