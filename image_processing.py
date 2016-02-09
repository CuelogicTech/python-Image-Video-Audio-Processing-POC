# brew install imagemagick
# brew install tesseract

# suo pip install Pillow
# sudo pip install pytesseract
# intsall OpenCv (http://www.samontab.com/web/2014/06/installing-opencv-2-4-9-in-ubuntu-14-04-lts/)
# sudo pip install pyssim (if used)
# sudo pip install -U scikit-image (need to install sudo apt-get install python-scipy)

import numpy as np
import cv2
import sys
import os
from PIL import Image
from pytesseract import *
from matplotlib import pyplot as plt
from skimage.measure import structural_similarity as ssim
#from skimage.measure import structural_similarity as ssim


class ImageProcessing(object):

	def __init__(self, image):
		self.imagePath = image
		self.imgOpen = Image.open(self.imagePath)

	def faceDetection(self):

		face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
		eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')

		img = cv2.imread(self.imagePath)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.2, 3, minSize=(30, 30))

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

		#cv2.w('img',img)
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

		#print str(sorted(colors.keys()))

		#img = cv2.imread(self.imagePath)
		#color = ('b','g','r')
		#for i,col in enumerate(color):
			#histr = cv2.calcHist([img],[i],None,[256],[0,256])
			#plt.plot(histr,color = col)
			#plt.xlim([0,256])
		#plt.show()
		#B G R

		return self.getColorPercentage(colors)
		
	def checkDuplicateImage(self, compare_path):
		
		# load the images
		originalImgRead = cv2.imread(self.imagePath)

		# convert the images to grayscale
		originalGreyScale = cv2.cvtColor(originalImgRead, cv2.COLOR_BGR2GRAY)

		originImageSize = self.imgOpen

		duplicateImages = []
		for fname in os.listdir(compare_path):
    
			path = os.path.join(compare_path, fname)
			shortname, extension = os.path.splitext(fname)
    
			if os.path.isfile(os.path.join(path)) and fname != "test3-orig.jpg" :
    	
				# load the images
				imagesRead = cv2.imread(compare_path+"/"+fname)
				imageSize = Image.open(compare_path+"/"+fname)

				# convert the images to grayscale
				imagesGreyScale = cv2.cvtColor(imagesRead, cv2.COLOR_BGR2GRAY)

				if cmp(originImageSize.size, imageSize.size) == 0:
					ssimResult = self.compare_images(originalGreyScale, imagesGreyScale)
					if ssimResult >= 0.99:
						duplicateImages.append(compare_path+"/"+fname)

		return duplicateImages

	def compare_images(self,imageA, imageB):

		# compute the mean squared error and structural similarity
		# index for the images
		ssimResult = ssim(imageA, imageB)
		return ssimResult 

	def getColorPercentage(self, colors):

		red_color = yellow_color = orange_color = green_color = blue_color = white_color = pink_color = black_color = grey_color = purple_color = brown_color = 0

		for bgr_code in colors.keys():
			
			if bgr_code[2] > 150 and  bgr_code[1] < 50 and bgr_code[0] < 50:
				red_color += 1
			elif bgr_code[2] > 200 and bgr_code[1] > 200 and bgr_code[0] < 100:
				yellow_color += 1
			elif bgr_code[2] > 200 and bgr_code[1] > 100 and bgr_code[1] < 200 and bgr_code[0] <50:
				orange_color += 1
			elif bgr_code[2] < 50 and bgr_code[1] > 150 and bgr_code[0] < 50:
				green_color += 1
			elif bgr_code[2]< 50 and bgr_code[1] < 50 and bgr_code[0] > 150:
				blue_color += 1
			elif bgr_code[2] > 240 and bgr_code[1] > 240 and bgr_code[0] > 240:
				white_color += 1
			elif bgr_code[2] < 40 and bgr_code[1] < 40 and bgr_code[0] < 40:
				black_color += 1
			elif bgr_code[2] > 150 and bgr_code[1] < 50 and bgr_code[0] > 150:
				pink_color += 1
			elif bgr_code[2] > 40 and bgr_code[2] < 240 and bgr_code[1] > 40 and bgr_code[1] < 240 and bgr_code[0] > 40 and bgr_code[0] < 240:
				grey_color += 1
			elif bgr_code[2] >80 and bgr_code[2] < 120 and bgr_code[1] > 0 and bgr_code[1] < 110 and bgr_code[0] > 180:
				purple_color += 1
			elif bgr_code[2] > 70 and bgr_code[2] < 120 and bgr_code[1] < 50 and bgr_code[0] < 50:
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


imagePath = sys.argv[1]
imageProcess = ImageProcessing(imagePath)
print "Face Detection: ", imageProcess.faceDetection()
print "\n==================================================================================================\n"

print "Text: ", imageProcess.extract_text()

print "\n==================================================================================================\n"

print "Color Percentage: ", imageProcess.getImageColor()

print "\n==================================================================================================\n"

print "Duplicate Image Path: ", imageProcess.checkDuplicateImage("images/test-images")