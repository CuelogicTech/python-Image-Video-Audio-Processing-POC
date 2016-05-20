import numpy as np
from PIL import Image
import timer

x = Image.open('bug.jpg', 'r')
x = x.convert('L')  #makes it greyscale
y = np.asarray(x.getdata(), dtype=np.float64).reshape((x.size[1], x.size[0]))

# <manipulate matrix y...>

y = np.asarray(y, dtype=np.uint8)  #if values still in range 0-255!
w = Image.fromarray(y, mode='L')
w.save('burger_gray.jpg')