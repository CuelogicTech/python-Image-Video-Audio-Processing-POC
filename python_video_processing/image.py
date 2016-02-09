import numpy as np
import cv2

# Load an color image in grayscale
img = cv2.imread('messi.jpg', 0)
ball = img[280:340, 330:390]
img[273:333, 100:160] = ball

cv2.imshow("Faces found", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
