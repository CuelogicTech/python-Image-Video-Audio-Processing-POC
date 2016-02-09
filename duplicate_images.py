from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from PIL import Image


def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	s = ssim(imageA, imageB)
 
	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
 
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

# load the images
original = cv2.imread("images/test-images/test3-orig.jpg")

# convert the images to grayscale
original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

originImageSize = Image.open("images/test-images/test3-orig.jpg")


basepath = 'images/test-images'
for fname in os.listdir(basepath):
    
    path = os.path.join(basepath, fname)
    shortname, extension = os.path.splitext(fname)
    
    if os.path.isfile(os.path.join(path)) and fname != "test3-orig.jpg" :
    	
		#print basepath+"/"+fname
    	# load the images
		images = cv2.imread(basepath+"/"+fname)
		imageSize = Image.open(basepath+"/"+fname)

		# convert the images to grayscale
		images = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)

		if cmp(originImageSize.size, imageSize.size) == 0:
			compare_images(original, images, "Original vs. Contrast")
