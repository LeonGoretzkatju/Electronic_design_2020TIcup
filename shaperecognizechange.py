import sensor, image, time
import cmath
#from fpioa_manager import fm
from machine import UART
from pyb import UART
#from board import board_info
#import lcd
uart = UART(3,115200)
#uart_A = UART(3, 115200,force=True)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
#sensor.set_auto_gain(False) # must be turned off for color tracking
#sensor.set_auto_whitebal(False) # must be turned off for color tracking
#lcd.init()
clock = time.clock()
xmid = 0
ymid = 0
xmidd = 0
ymidd = 0
scolor = 1000
sshape = 1000
shape = 0
sred =0
sgreen = 0
sblue = 0
c = [0,0,0,0]
roiarea = [80-int(160/2),60-int(130/2),160,120]

def find_maxblob(blobs):#寻找面积最大的色块
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob

def find_maxrect(rects): #寻找面积最大的矩形块
    max_size = 0
    for b in rects:
        b_area = b.rect()
        bshape = b_area[2]*b_area[3]
        if bshape > max_size :
            max_rect = b
            max_size = bshape
    return max_rect

def find_maxcir(circles): #寻找面积最大的圆形
    max_size1 = 0
    for b in circles:
        if 3.1415926*b[2]*b[2] > max_size1:
            max_cir = b
            max_size1 = 3.1415926*b[2]*b[2]
    return max_cir

def data_convert(data): #数据解算 防止一次的数据量大于255 将数据拆分成两个数据
    if data < 255:
        data1 = 0
        data2 = data
    if data > 255:
        data1 = 1
        data2 = data-255
    return data1,data2





while(True):
    clock.tick()

    flag = 0
    flagred = 0
    flaggreen = 0
    flagblue = 0
    img = sensor.snapshot() #去畸变
    img.draw_cross(int(img.width()/2),int(img.height()/2))
    print('image width',img.width())
    print('image height',img.height())
#    img = img.morph(kernel_size, kerne+..l)
#    img = img.mean(2)
    rects = img.find_rects(roi = roiarea,threshold = 5000)
    circles = img.find_circles(roi = roiarea,threshold = 5000, x_margin = 10, y_margin = 10, r_margin = 10,r_min = 2, r_max = 80, r_step = 2)
#检测矩形边缘与圆形的边缘
    green_threshold   = (10, 65, -80, -10, -5, 31)
    blue_threshold = (0, 65, -30, 30, -128, -10)
    red_threshold = (0, 65, 15, 127, -10, 50)

    '''
    green_threshold   = (0, 100, -80, -20, -5, 30)
    blue_threshold = (0, 59, -80, 30, -128, -5)
    red_threshold = (0, 100, 15, 127, -10, 50)
    '''
    #寻找不同颜色的色块 设置ROI区域
    blobsblue = img.find_blobs([blue_threshold],roi = roiarea)
    blobsgreen = img.find_blobs([green_threshold],roi = roiarea)
    blobsred = img.find_blobs([red_threshold],roi = roiarea)

    if blobsblue:
        max_blobblue=find_maxblob(blobsblue)
        sblue = max_blobblue.pixels() #获取色块中的像素值
    if blobsgreen:
        max_blobgreen=find_maxblob(blobsgreen)
        sgreen = max_blobgreen.pixels()
    if blobsred:
        max_blobred=find_maxblob(blobsred)
        sred = max_blobred.pixels()




    if sred>sgreen and sred>sblue:
        scolor = sred
        flagred = 1
        xmid = max_blobred.cx()
        ymid = max_blobred.cy()
        width = max_blobred.w()
        height = max_blobred.h()
        img.draw_rectangle(max_blobred.rect(),color = (255, 255, 0))
#        img.draw_cross(max_blobred.cx(), max_blobred.cy())
        print('sum:', len(blobsred))
        color = 'R'
        print('红色色块像素',max_blobred.pixels())
        print('红色色块框面积',max_blobred.area())
        sarea = max_blobred.area()
    if sgreen>sblue and sgreen>sred:
        scolor = sgreen
        flaggreen = 1
        xmid = max_blobgreen.cx()
        ymid = max_blobgreen.cy()
        width = max_blobgreen.w()
        height = max_blobgreen.h()
        img.draw_rectangle(max_blobgreen.rect(),color = (255, 255, 0))
#        img.draw_cross(max_blobgreen.cx(), max_blobgreen.cy())
        print('sum:', len(blobsgreen))
        color = 'G'
        print('绿色色块像素',max_blobgreen.pixels())
        print('绿色色块框面积',max_blobgreen.area())
        sarea = max_blobgreen.area()
    if sblue>sred and sblue>sgreen:
        scolor = sblue
        flagblue = 1
        xmid = max_blobblue.cx()
        ymid = max_blobblue.cy()
        width = max_blobblue.w()
        height = max_blobblue.h()
        img.draw_rectangle(max_blobblue.rect(),color = (255, 255, 0))
#        img.draw_cross(max_blobblue.cx(), max_blobblue.cy())
        print('sum:', len(blobsblue))
        color = 'B'
        print('蓝色色块像素',max_blobblue.pixels())
        print('蓝色色块框面积',max_blobblue.area())
        sarea = max_blobblue.area()
        print('比例',scolor/sarea)

    for i in blobsblue:
        if 0.43< scolor/sarea<0.59 and flagblue == 1:
            print('这是三角形')
            color = 'B'
            xmiddd = xmid
            ymiddd = ymid
            if (abs(xmiddd - 80) <= 40) and (abs(ymiddd - 60) < 40):
                shape = 3
                radius = width
    for i in blobsred:
        if 0.43< scolor/sarea<0.59 and flagred == 1:
            print('这是三角形')
            color = 'R'
            xmiddd = xmid
            ymiddd = ymid
            if (abs(xmiddd - 80) <= 40) and (abs(ymiddd - 60) < 40):
                shape = 3
                radius = width
    for i in blobsgreen:
        if 0.43< scolor/sarea<0.59 and flaggreen == 1:
            print('这是三角形')
            color = 'G'
            xmiddd = xmid
            ymiddd = ymid
            if (abs(xmiddd - 80) <= 40) and (abs(ymiddd - 60) < 40):
                shape = 3
                radius = width
    if circles:
        d = find_maxcir(circles)
        area = (d.x()-d.r(), d.y()-d.r(), 2*d.r(), 2*d.r())
        img.draw_circle(d.x(),d.y(),d.r())
        radius = d.r()
        xmid = d.x()
        ymid = d.y()
        sshape = 3.1415926*d.r()*d.r()
        print('sum:', len(circles))
        print('圆形面积',sshape)
        if abs(scolor/sshape-1)<=0.15:
            shape = 2
            flag = 1

    if rects and flag == 0:
        for a in rects:
            a_area = a.rect()
            a_sshape = a_area[2]*a_area[3]
            a_xmidd = a_area[0]+int(a_area[2]/2)
            a_ymidd = a_area[1]+int(a_area[3]/2)
            if abs(xmid - a_xmidd)<20 and abs(ymid - a_ymidd)<20:
                c = a
                area = c.rect()
                img.draw_rectangle(a.rect())
                sshape = area[2]*area[3]
                print('sum:', len(rects))
                print('矩形面积',sshape)
                xmidd = area[0]+int(area[2]/2)
                ymidd = area[1]+int(area[3]/2)
                radius = area[2]
                if abs(scolor/sshape-1)<=0.1:
                    shape = 1
                '''
                if 0.28< scolor/sshape<0.65:
                    print('这是三角形')
                    shape = 3
                    xmiddd = area[0]+int(area[2]/2)
                    ymiddd = area[1]+int(area[3]/2)
                    radius = area[2]
                '''

#        statistics = img.get_statistics(roi=area)#像素颜色统计
#        cr = c.find_rects(roi=area,threshold = 3500)
#        for ci in cr:
#            statistics = ci.get_statistics(roi = area)

    if shape == 1:
        if color == 'R':
            img.draw_rectangle(area, color = (255, 0, 0))
#            img.draw_cross(area[0]+int(area[2]/2),area[1]+int(area[3]/2))
        if color == 'G':
            img.draw_rectangle(area, color = (0, 255, 0))
#            img.draw_cross(area[0]+int(area[2]/2),area[1]+int(area[3]/2))
        if color == 'B':
            img.draw_rectangle(area, color = (0, 0, 255))
#            img.draw_cross(area[0]+int(area[2]/2),area[1]+int(area[3]/2))

    if shape == 2:
        if color == 'R':
            img.draw_circle(d.x(), d.y(), d.r(), color = (255, 0, 0))#识别到的红色圆形用红色的圆框出来
            img.draw_cross(d.x(),d.y())
        if color == 'G':
            img.draw_circle(d.x(), d.y(), d.r(), color = (0, 255, 0))#识别到的红色圆形用红色的圆框出来
            img.draw_cross(d.x(),d.y())
        if color == 'B':
            img.draw_circle(d.x(), d.y(), d.r(), color = (0, 0, 255))#识别到的红色圆形用红色的圆框出来
            img.draw_cross(d.x(),d.y())

    if shape == 3 and flagblue == 1:
        area = (xmiddd-int(width/2),ymiddd-int(height/2)-4,width,height)
        if color == 'R':
            img.draw_rectangle(area, color = (0, 0, 0))
    #            img.draw_cross(area[0]+int(area[2]/2),area[1]+int(area[3]/2))
        if color == 'G':
            img.draw_rectangle(area, color = (0, 0, 0))
    #            img.draw_cross(area[0]+int(area[2]/2),area[1]+int(area[3]/2))
        if color == 'B':
            img.draw_rectangle(area, color = (0, 0, 0))
    #            img.draw_cross(area[0]+int(area[2]/2),area[1]+int(area[3]/2))

#        img.draw_rectangle(max_blob.rect())
#        img.draw_cross(max_blob.cx(), max_blob.cy())
#        xmiddd = max_blob.cx()
#        ymiddd = max_blob.cy()

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
        uart.write('%c' %(radius))
        print('边长为',radius)

    uart.write('%c' %(end))

    print("FPS %f" % clock.fps())
