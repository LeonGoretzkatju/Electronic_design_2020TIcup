# Untitled - By: T430 - 周二 10月 13 2020

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

a = (0,0,0,0)
clock = time.clock()
def find_maxrect(rects): #寻找面积最大的矩形块
    max_size = 0
    for b in rects:
        b_area = b.rect()
        bshape = b_area[2]*b_area[3]
        if bshape > max_size :
            max_rect = b
            max_size = bshape
    return max_rect
while(True):
    clock.tick()
    img = sensor.snapshot()
    area = img.find_rects(threshold = 10000)
    if area:
        b = find_maxrect(area)
        print(len(area))
        a=b.rect()
        img.draw_rectangle(a)
#    print(clock.fps())
