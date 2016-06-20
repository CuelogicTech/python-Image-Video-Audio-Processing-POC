import array
import sys
import os
import math
import re
 
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage: %s filename1.yuv filename2.yuv [width height]" % sys.argv[0]
 
 
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
 
    if filename1 == filename2:
        print "warning! do you really mean to compare the file with itself?"
 
    data1 = array.array('B')
    data2 = array.array('B')
 
    file1_size = os.path.getsize(filename1)
    file2_size = os.path.getsize(filename2)
 
    minsize = min(file1_size, file2_size)
 
    if file1_size != file2_size:
        print "warning, file sizes do not match! comparing min size %d bytes" % minsize
 
    if len(sys.argv) >= 5:
        w = int(sys.argv[3])
        h = int(sys.argv[4])
    else:
        m = re.search(".*[_-](\d+)x(\d+).*", filename1)
        # assert m
        w = int(m.group(1))
        h = int(m.group(2))
        # assert w*h*3/2 <= minsize
        print "(%dx%d)" %(w,h)
 
 
    data1.fromfile(open(filename1,"rb"),minsize)
    data2.fromfile(open(filename2,"rb"),minsize)
 
    print "data size: %d, w*h=%d, w*h*3/2=%d" % (len(data1), w*h, w*h*3/2)
    print "evaluating mse.."
 
    def psnr(mse):
        log10 = math.log10
        return 10.0*log10(float(256*256)/float(mse))
 
    def mean(seq):
        if len(seq) == 0: return 0.0
        else: return sum(seq)/float(len(seq))
 
    def sum_square_err(data1, data2, beg, end):
        return sum( (a-b)*(a-b) for a,b in zip(data1[beg:end],data2[beg:end]))
 
    y = 0
    u = y + (w * h)
    v = u + (w/2 * h/2)
    data_end = w*h*3/2
 
    begin = [y,u,v,y]
    end = [u,v,data_end,data_end]
    size = [w*h, w*h/4, w*h/4, w*h*3/2]
 
    colorspace_mse = [sum_square_err(data1,data2,
        begin[i], end[i])/float(size[i]) for i in range(4)]
 
    colorspace_psnr = [psnr(m) for m in colorspace_mse]
 
    print "planes: Y, U, V, Whole frame"
    print 'colorplane mse: ', colorspace_mse
    print 'colorplane psnr: ', colorspace_psnr