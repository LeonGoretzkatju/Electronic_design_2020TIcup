# 多颜色多模板匹配示例
#
# 这个例子显示了使用OpenMV的多色跟踪。

import sensor, image, time
from image import SEARCH_EX, SEARCH_DS

# 颜色跟踪阈值(L Min, L Max, A Min, A Max, B Min, B Max)
# 下面的阈值跟踪一般红色/绿色的东西。你不妨调整他们...
thresholds = [(16, 63, -14, 16, -35, -10)] # generic_blue_thresholds
# 不要超过16个颜色阈值
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
#sensor.set_auto_gain(False) # must be turned off for color tracking
#sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

# 只有比“pixel_threshold”多的像素和多于“area_threshold”的区域才被
# 下面的“find_blobs”返回。 如果更改相机分辨率，
# 请更改“pixels_threshold”和“area_threshold”。 “merge = True”合并图像中所有重叠的色块。

templates = ["/B0.bmp"] #保存多个模板

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs(thresholds, pixels_threshold=800, area_threshold=1000):
        #img.draw_rectangle(blob.rect())
        #img.draw_cross(blob.cx(), blob.cy())
        #print(blob.code())

        img = img.to_grayscale()
        #for t in templates:
        template = image.Image(templates[0])
        #对每个模板遍历进行模板匹配
        r = img.find_template(template, 0.70, step=4,roi=(80,60,500,500)) #, roi=(10, 0, 60, 60))
        #find_template(template, threshold, [roi, step, search]),threshold中
        #的0.7是相似度阈值,roi是进行匹配的区域（左上顶点为（10，0），长80宽60的矩形），
        #注意roi的大小要比模板图片大，比frambuffer小。
        #把匹配到的图像标记出来
        if r:
            img.draw_rectangle(r, color=0)
            print(blob.code(), t) #打印模板名字
            #如果为红色, blob.code()==1; 如果为绿色, blob.code==2.
            #如果为数字0, t=="0.pgm"; 如果为数字1, t=="1.pgm".


    #print(clock.fps())
