#####################################################################################
Phase 1
Basic Image/Audio/Video Processing
#####################################################################################

Media Type:
1. Image
2. Video
3. Audio


1. Image
   - R&D to find out library to processing on image
   - Extract text from an image
   - Text analysis
   - Find out language from text
   - Color percentage 
   - Face detection
   - Duplicate image

2. Video
   - R&D to find out library to processing on video
   - Extact audio from vidoe
   - Covert audio to text
   - Text analysis
   - Find out language from text
   - Video lenght
   - Extract color percentage in video frames

3. Audio
   - R&D to find out library to processing on audio
   - Covert audio to text
   - Text analysis
   - Find out language from text

#####################################################################################
Phase 2
Image/Video Search Engine
#####################################################################################


Media Type:
1. Image
2. Video

Objective

To effectively perform comparison of images and video and extract relevant information

Steps

1. Retrieve Original image metadata before conversion.
2. Using a hash function for immediate comparison.
3. GrayScale conversion of original.
4. DownScale converted image retaining maximum detail of same.
5. Formulate efficient algorithm for retrieving image matches.
6. Formulate efficient algorithm to retrieve textual content embedded in image.
7. Train application to identify certain graphic content [eg: faces, logos and objects]
8. Identify suitable and efficient storage for saving and retrieving metadata of matches.
9. Explore possibilities and device phase 2 for above steps in video processing.

Application Initial Workflow

https://drive.google.com/a/cuelogic.co.in/file/d/0B5oreTB1NzafalR0MnBFd3p1OEU/view?usp=sharing

Hashing images
1. http://research.microsoft.com/pubs/77279/venkie00robust.pdf
2. http://www.phash.org/docs/pubs/thesis_zauner.pdf
3. http://blog.iconfinder.com/detecting-duplicate-images-using-python/
4. https://github.com/JohannesBuchner/imagehash

Gray Scaling
1. http://www.tannerhelland.com/3643/grayscale-image-algorithm-vb6/
2. http://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/
3. https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-649.pdf
4. https://extr3metech.wordpress.com/2012/09/23/convert-photo-to-grayscale-with-python-opencv/

Down Scaling
1. https://pixinsight.com/forum/index.php?topic=556.0
2. https://web.archive.org/web/20140824074425/http://www.cg.tuwien.ac.at/~theussl/DA/node11.html
3. http://mentallandscape.com/Papers_siggraph88.pdf
4. http://johanneskopf.de/publications/downscaling/paper/downscaling.pdf

Gray Scale Image Comparison
1. http://www.pyimagesearch.com/2014/09/15/python-compare-two-images/

Image storage & Metadata Extraction 
1. http://www.ijeijournal.com/papers/v2i4/D02042628.pdf
2. http://www.cise.ufl.edu/~sahni/papers/encycloimage.pdf
3. http://stackoverflow.com/questions/18948382/run-length-encoding-in-python


