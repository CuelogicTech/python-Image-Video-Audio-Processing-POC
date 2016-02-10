# brew install imagemagick
# brew install tesseract

# suo pip install Pillow
# sudo pip install pytesseract
# intsall OpenCv (http://www.samontab.com/web/2014/06/installing-opencv-2-4-9-in-ubuntu-14-04-lts/)
# sudo pip install pyssim (if used)
# sudo pip install -U scikit-image (need to install sudo apt-get install python-scipy)

#import numpy as np
import cv2
import sys
import os
from PIL import Image
from pytesseract import *
#from matplotlib import pyplot as plt
from subprocess import check_output

class ImageProcessing(object):

	def __init__(self, image):


		self.imagePath = image

		if self.imageValidation():
			self.imgOpen = Image.open(self.imagePath)

	def faceDetection(self):

		face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
		eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')

		img = cv2.imread(self.imagePath)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.2, 3, minSize=(20, 20), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

		#cv2.imshow('img',img)
		imageFilename = os.path.basename(self.imagePath)
		
		cv2.imwrite('images/face_detect/'+imageFilename, img)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		face_detect = {}
		face_detect["face_count"] = len(faces)
		face_detect["result_image"] = 'images/face_detect/'+imageFilename
		return face_detect

	def extract_text(self):

		text = image_to_string(self.imgOpen)
		return text

	def getImageColor(self):

		img_rgb = self.imgOpen.convert('RGB')

		colors = {}
		for color in img_rgb.getdata():
			colors[color] = colors.get(color, 0) + 1

		return self.getColorPercentage(colors)
		
	def checkDuplicateImage(self, compare_path):
		
		images_compare = check_output(["python", "ssim", self.imagePath, compare_path+"/*"])

		duplicateImages = []
		split_result = images_compare.split(' - ')
		for image_path in split_result:
			splitImagePath = image_path.split('\n')
			if len(splitImagePath) == 2 :
				duplicateImg = splitImagePath[0].split(':')
				
				duplicateImgRatio = float(duplicateImg[1]) * 100
				if duplicateImgRatio > 45:
					duplicateImages.append(duplicateImg[0])

		return duplicateImages

	def getColorPercentage(self, colors):

		red_color = yellow_color = orange_color = green_color = blue_color = white_color = pink_color = black_color = grey_color = purple_color = brown_color = 0

		for bgr_code in colors.keys():
			# BGR RGB
			if bgr_code[0] > 150 and  bgr_code[1] < 50 and bgr_code[2] < 50:
				red_color += 1
			elif bgr_code[0] > 200 and bgr_code[1] > 200 and bgr_code[2] < 100:
				yellow_color += 1
			elif bgr_code[0] > 200 and bgr_code[1] > 100 and (bgr_code[2] < 200 and bgr_code[2] <50):
				orange_color += 1
			elif bgr_code[0] < 50 and bgr_code[1] > 150 and bgr_code[2] < 50:
				green_color += 1
			elif bgr_code[0]< 50 and bgr_code[1] < 50 and bgr_code[2] > 150:
				blue_color += 1
			elif bgr_code[0] > 240 and bgr_code[1] > 240 and bgr_code[2] > 240:
				white_color += 1
			elif bgr_code[0] < 40 and bgr_code[1] < 40 and bgr_code[2] < 40:
				black_color += 1
			elif bgr_code[0] > 150 and bgr_code[1] < 50 and bgr_code[2] > 150:
				pink_color += 1
			elif (bgr_code[0] > 40 and bgr_code[0] < 240) and (bgr_code[1] > 40 and bgr_code[1] < 240) and (bgr_code[2] > 40 and bgr_code[2] < 240):
				grey_color += 1
			elif (bgr_code[0] > 80 and bgr_code[0] < 120) and (bgr_code[1] > 0 and bgr_code[1] < 110) and bgr_code[2] > 180:
				purple_color += 1
			elif (bgr_code[0] > 70 and bgr_code[0] < 120) and bgr_code[1] < 50 and bgr_code[2] < 50:
				brown_color += 1


		total_color = red_color + yellow_color + orange_color + green_color + blue_color + white_color + pink_color + black_color + grey_color + purple_color + brown_color

		clorsPercentage = {}
		clorsPercentage["red"] = round((red_color / float(total_color)) * 100, 4)
		clorsPercentage["yellow"] = round((yellow_color / float(total_color)) * 100, 4)
		clorsPercentage["orange"] = round((orange_color / float(total_color)) * 100, 4)
		clorsPercentage["green"] = round((green_color / float(total_color)) * 100, 4)
		clorsPercentage["blue"] = round((blue_color / float(total_color)) * 100, 4)
		clorsPercentage["white"] = round((white_color / float(total_color)) * 100, 4)
		clorsPercentage["pink"] = round((pink_color / float(total_color)) * 100, 4)
		clorsPercentage["black"] = round((black_color / float(total_color)) * 100, 4)
		clorsPercentage["grey"] = round((grey_color / float(total_color)) * 100, 4)
		clorsPercentage["purple"] = round((purple_color / float(total_color)) * 100, 4)
		clorsPercentage["brown"] = round((brown_color / float(total_color)) * 100, 4)

		return clorsPercentage

	def imageValidation(self):
		
		filepath, filename = os.path.split(self.imagePath)
		shortname, extension = os.path.splitext(filename)
		extensionlist = ['.jpg', '.png', '.gif', '.jpeg']
		
		if extension.lower() in extensionlist:
			return True
		else:
			return False


imagePath = sys.argv[1]
imageProcess = ImageProcessing(imagePath)

if imageProcess.imageValidation():

	print "Face Detection: ", imageProcess.faceDetection()
	print "\n==================================================================================================\n"

	print "Text: ", imageProcess.extract_text()
	print "\n==================================================================================================\n"

	print "Color Percentage: ", imageProcess.getImageColor()
	print "\n==================================================================================================\n"

	print "Duplicate Images Path: ", imageProcess.checkDuplicateImage("images/test-images")
else:
	print "Invalid Image"