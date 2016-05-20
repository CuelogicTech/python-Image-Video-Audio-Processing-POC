
##Image/Video Search Engine

Media Type: 
1. Image 
2. Video

###Objective

To effectively perform comparison of images and video and extract relevant information

###Steps

Retrieve Original image metadata before conversion.
Using a hash function for immediate comparison.
GrayScale conversion of original.
DownScale converted image retaining maximum detail of same.
Formulate efficient algorithm for retrieving image matches.
Formulate efficient algorithm to retrieve textual content embedded in image.
Train application to identify certain graphic content [eg: faces, logos and objects]
Identify suitable and efficient storage for saving and retrieving metadata of matches.
Explore possibilities and device phase 2 for above steps in video processing.

###Application Initial Workflow

https://drive.google.com/a/cuelogic.co.in/file/d/0B5oreTB1NzafalR0MnBFd3p1OEU/view?usp=sharing

###Hashing images 

1. http://research.microsoft.com/pubs/77279/venkie00robust.pdf 2. http://www.phash.org/docs/pubs/thesis_zauner.pdf 3. http://blog.iconfinder.com/detecting-duplicate-images-using-python/ 4. https://github.com/JohannesBuchner/imagehash

###Gray Scaling 

1. http://www.tannerhelland.com/3643/grayscale-image-algorithm-vb6/ 2. http://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/ 3. https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-649.pdf 4. https://extr3metech.wordpress.com/2012/09/23/convert-photo-to-grayscale-with-python-opencv/

###Down Scaling 

1. https://pixinsight.com/forum/index.php?topic=556.0 2. https://web.archive.org/web/20140824074425/http://www.cg.tuwien.ac.at/~theussl/DA/node11.html 3. http://mentallandscape.com/Papers_siggraph88.pdf 4. http://johanneskopf.de/publications/downscaling/paper/downscaling.pdf

###Gray Scale Image Comparison 

1. http://www.pyimagesearch.com/2014/09/15/python-compare-two-images/

###Image storage & Metadata Extraction 

1. http://www.ijeijournal.com/papers/v2i4/D02042628.pdf 2. http://www.cise.ufl.edu/~sahni/papers/encycloimage.pdf 3. http://stackoverflow.com/questions/18948382/run-length-encoding-in-python

###Image Comparison Methods 

1. http://stackoverflow.com/questions/843972/image-comparison-fast-algorithm 2. http://www.pyimagesearch.com/2014/12/01/complete-guide-building-image-search-engine-python-opencv/ 3. http://www.pyimagesearch.com/2014/01/15/the-3-types-of-image-search-engines-search-by-meta-data-search-by-example-and-hybrid/ 4. http://effbot.org/zone/pil-comparing-images.htm 5. http://www.imagemagick.org/Usage/compare/
