import sensor, image, time
import cmath
from machine import UART
from pyb import UART
uart = UART(3,115200)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

def find_maxblob(blobs):
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob

def find_max(rects): #寻找面积最大的矩形块
    max_size = 0
    for b in rects:
        area = (b.rect())
        if b.magnitude() > max_size :
            max_blob = b
            max_size = b.magnitude()
    return max_blob

def find_maxcir(circles): #寻找面积最大的圆形
    max_size1 = 0
    for b in circles:
        if 3.1415926*b[2]*b[2] > max_size1:
            max_cir = b
            max_size1 = 3.1415926*b[2]*b[2]
    return max_cir

def data_convert(data):
    if data < 255:
        data1 = 0
        data2 = data
    if data > 255:
        data1 = 1
        data2 = data-255
    return data1,data2


while(True):
    clock.tick()
    xmid = 0
    ymid = 0
    xmidd = 0
    ymidd = 0
    img = sensor.snapshot() #去畸变
    rects = img.find_rects(threshold = 5000)
    circles = img.find_circles(threshold = 5000, x_margin = 10, y_margin = 10, r_margin = 10,r_min = 20, r_max = 80, r_step = 2)
    green_threshold   = (0, 100, -40, -18, 0, 37)
    blue_threshold = (16, 63, -14, 16, -35, -10)
    red_threshold = (0, 100, 10, 127, 0, 57)
    blobs = img.find_blobs([blue_threshold])
    blobsgreen = img.find_blobs([green_threshold])
    blobsred = img.find_blobs([red_threshold])
    if blobs:
        max_blob=find_maxblob(blobs)
        print('sum :', len(blobs))
#        img.draw_rectangle(max_blob.rect())
#        img.draw_cross(max_blob.cx(), max_blob.cy())
        color = 'B'
        print('蓝色色块像素',max_blob.pixels())
        print('蓝色色块框面积',max_blob.area())
        scolor = max_blob.pixels()
        ssarea = max_blob.area()
    if blobsgreen:
        max_blobgreen=find_maxblob(blobsgreen)
        print('sum :', len(blobsgreen))
#        img.draw_rectangle(max_blobgreen.rect())
#        img.draw_cross(max_blobgreen.cx(), max_blobgreen.cy())
        color = 'G'
        print('绿色色块像素',max_blobgreen.pixels())
        print('绿色色块框面积',max_blobgreen.area())
        scolor = max_blobgreen.pixels()
        ssarea = max_blobgreen.pixels()
    if blobsred:
        max_blobred=find_maxblob(blobsred)
        print('sum :', len(blobsred))
        color = 'R'
        print('红色色块像素',max_blobred.pixels())
        print('红色色块框面积',max_blobred.area())
        scolor = max_blobred.pixels()
        ssarea = max_blobred.area()

    if circles:
        shape = 2
        d = find_maxcir(circles)
        area = (d.x()-d.r(), d.y()-d.r(), 2*d.r(), 2*d.r())
        radius = d.r()
        xmid = d.x()
        ymid = d.y()
        sshape = 3.1415926*d.r()*d.r()
        print('circles',sshape)

    if rects:
        shape = 1
        c = find_max(rects)
        area = c.rect()
        sshape1 = area[2]*area[3]
        xmidd = area[0]+int(area[2]/2)
        ymidd = area[1]+int(area[3]/2)
        radius = area[2]
        print('sshape1',sshape1)


    if shape == 2:

        if abs(sshape-scolor)<30:
            if (color == 'R'):
                img.draw_circle(d.x(), d.y(), d.r(), color = (255, 0, 0))#识别到的红色圆形用红色的圆框出来
                img.draw_cross(d.x(),d.y())
            elif color == 'G':
                img.draw_circle(d.x(), d.y(), d.r(), color = (0, 255, 0))#识别到的红色圆形用红色的圆框出来
                img.draw_cross(d.x(),d.y())
            elif color == 'B':
                img.draw_circle(d.x(), d.y(), d.r(), color = (0, 0, 255))#识别到的红色圆形用红色的圆框出来
                img.draw_cross(d.x(),d.y())

    elif shape == 1:
        if abs(sshape1-scolor)<100:
            if color == 'R':
                img.draw_rectangle(max_blobred.rect(), color = (255, 0, 0))
                img.draw_cross(max_blobred.cx(), max_blobred.cy())
            if color == 'G':
                img.draw_rectangle(max_blobgreen.rect(), color = (0, 255, 0))
                img.draw_cross(max_blobgreen.cx(), max_blobgreen.cy(), color = (0, 0, 255))
            if color == 'B':
                img.draw_rectangle(max_blob.rect())
                img.draw_cross(max_blob.cx(), max_blob.cy())

    if 0.43< scolor/ssarea<0.57:
        print('这是三角形')
        shape = 3
        if color == 'B':
            img.draw_rectangle(max_blob.rect())
            img.draw_cross(max_blob.cx(), max_blob.cy())
            xmiddd = max_blob.cx()
            ymiddd = max_blob.cy()
        if color == 'R':
            img.draw_rectangle(max_blobred.rect())
            img.draw_cross(max_blobred.cx(), max_blobred.cy())
            xmiddd = max_blobred.cx()
            ymiddd = max_blobred.cy()
        if color == 'G':
            img.draw_rectangle(max_blobgreen.rect())
            img.draw_cross(max_blobgreen.cx(), max_blobgreen.cy())
            xmiddd = max_blobgreen.cx()
            ymiddd = max_blobgreen.cy()


#        radius = int(cmath.sqrt(4/cmath.sqrt(3)*max_blob.pixels()))

    start = 0xb3
    end = 0xb4
    if shape == 1:

        [data1,data2] = data_convert(xmidd)
#        output_str1="[%c,%c]" % (data1,data2) #方式1
        [data3,data4] = data_convert(ymidd)
#        output_str2="[%c,%c]" % (data3,data4) #方式1
        uart.write('%c' %(start))
        uart.write('%c' %(shape))
        uart.write('%c' %(color))
        uart.write('%c' %(data1))
        uart.write('%c' %(data2))
        uart.write('%c' %(data3))
        uart.write('%c' %(data4))
        uart.write('%c' %(radius))
        print('边长为',radius)

    if shape == 2:
        [data1,data2] = data_convert(xmid)
    #        output_str1="[%c,%c]" % (data1,data2) #方式1
        [data3,data4] = data_convert(ymid)
    #        output_str2="[%c,%c]" % (data3,data4) #方式1
        uart.write('%c' %(start))
        uart.write('%c' %(shape))
        uart.write('%c' %(color))
        uart.write('%c' %(data1))
        uart.write('%c' %(data2))
        uart.write('%c' %(data3))
        uart.write('%c' %(data4))
        uart.write('%c' %(radius))
        print('边长为',radius)

    if shape == 3:
        [data1,data2] = data_convert(xmiddd)
        #        output_str1="[%c,%c]" % (data1,data2) #方式1
        [data3,data4] = data_convert(ymiddd)
        #        output_str2="[%c,%c]" % (data3,data4) #方式1
        uart.write('%c' %(start))
        uart.write('%c' %(shape))
        uart.write('%c' %(color))
        uart.write('%c' %(data1))
        uart.write('%c' %(data2))
        uart.write('%c' %(data3))
        uart.write('%c' %(data4))
#        uart.write('%c' %(radius))
#        print('边长为',radius)

    uart.write('%c' %(end))

print("FPS %f" % clock.fps())

