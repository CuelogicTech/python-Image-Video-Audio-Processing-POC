# from PIL import Image 
# image_file = Image.open("burger.jpg")  # open colour image
# image_file = image_file.convert('1')  # convert image to black and white
# image_file.save('burger_copy.jpg')


import numpy as np
from PIL import Image
import time
import calculate_time

x = Image.open('img/world.topo.bathy.200407.3x21600x21600.A2.png', 'r')
x = x.convert('L')  #makes it greyscale
y = np.asarray(x.getdata(), dtype=np.float64).reshape((x.size[1], x.size[0]))

# <manipulate matrix y...>

y = np.asarray(y, dtype=np.uint8)  #if values still in range 0-255!
w = Image.fromarray(y, mode='L')
w.save('img/world.topo.bathy.200407.3x21600x21600.A2.gray.png')
