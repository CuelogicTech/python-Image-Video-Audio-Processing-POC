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

		print "Found {0} faces!".format(len(faces))

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

		cv2.imshow('img',img)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()


	def extract_text(self):

		text = image_to_string(self.imgOpen)
		print text

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
		for bgr_code in colors.keys():
			#print bgr_code
			#print "--===>>>", bgr_code[0]
			#print "--===>>>", bgr_code[1]
			#print "--===>>>", bgr_code[2]
			if bgr_code[2] > 150 and  bgr_code[1] < 50 and bgr_code[0] < 50:
				print "red"
			elif bgr_code[2] > 200 and bgr_code[1] > 200 and bgr_code[0] < 100:
				print "yellow"
			elif bgr_code[2] > 200 and bgr_code[1] > 100 and bgr_code[1] < 200 and bgr_code[0] <50:
				print "orange"
			elif bgr_code[2] < 50 and bgr_code[1] > 150 and bgr_code[0] < 50:
				print "green"
			elif bgr_code[2]< 50 and bgr_code[1] < 50 and bgr_code[0] > 150:
				print "blue"
			elif bgr_code[2] > 240 and bgr_code[2] > 240 and bgr_code[2] > 240:
				print "blue"

			#exit()
			#if bgr_code[0]

	def checkDuplicateImage(self, compare_path):
		
		# load the images
		originalImgRead = cv2.imread(self.imagePath)

		# convert the images to grayscale
		originalGreyScale = cv2.cvtColor(originalImgRead, cv2.COLOR_BGR2GRAY)

		originImageSize = self.imgOpen

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
					self.compare_images(originalGreyScale, imagesGreyScale, "Original vs. Contrast")

	def compare_images(self,imageA, imageB, title):
		# compute the mean squared error and structural similarity
		# index for the images
		ssimResult = ssim(imageA, imageB)
 
		# setup the figure
		fig = plt.figure(title)

		if ssimResult >= 0.99:
			plt.suptitle("SSIM: %.2f" % (ssimResult))
 
			# show first image
			ax = fig.add_subplot(1, 2, 1)
			plt.imshow(imageA, cmap = plt.cm.gray)
			plt.axis("off")
 
			# show the second image
			ax = fig.add_subplot(1, 2, 2)
			plt.imshow(imageB, cmap = plt.cm.gray)
			plt.axis("off")
 
			# show the images
			plt.show()


imagePath = sys.argv[1]
imageProcess = ImageProcessing(imagePath)
imageProcess.faceDetection()
imageProcess.extract_text()
imageProcess.getImageColor()
imageProcess.checkDuplicateImage("images/test-images")