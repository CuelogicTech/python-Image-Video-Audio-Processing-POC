from PIL import Image
import imagehash
import time
import calculate_time

start_time = time.time()
hash = imagehash.average_hash(Image.open('world.topo.bathy.200407.3x21600x21600.A2.png'))
print
print 'Hash key of an Image:', hash

otherhash = imagehash.average_hash(Image.open('world.topo.bathy.200407.3x21600x21600.A2.gray.png'))