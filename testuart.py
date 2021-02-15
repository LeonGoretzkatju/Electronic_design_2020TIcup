# Blob Detection and uart transport
import sensor, image, time
from pyb import UART
import json
enable_lens_corr = False # turn on for straighter lines...打开以获得更直的线条…
min_degree = 0
max_degree = 179
# For color tracking to work really well you should ideally be in a very, very,
# very, controlled enviroment where the lighting is constant...
yellow_threshold   = (0, 100, 10, 127, 0, 57)
# You may need to tweak the above settings for tracking green things...
# Select an area in the Framebuffer to copy the color settings.

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock() # Tracks FPS.

uart = UART(3, 115200)
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob

while(True):
    img = sensor.snapshot() # Take a picture and return the image.

    blobs = img.find_blobs([yellow_threshold])
    if blobs:
        max_blob=find_max(blobs)
        print('sum :', len(blobs))
        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())

        output_str="[%d,%d]" % (max_blob.cx(),max_blob.cy()) #方式1
        #output_str=json.dumps([max_blob.cx(),max_blob.cy()]) #方式2
        print('色块像素',max_blob.pixels())
        print('色块框面积',max_blob.area())
        print('you send:',output_str)
        uart.write(output_str+'\r\n')
    #    area = 2*max_blob.rect()
    #    for l in img.find_lines(threshold = 1000, theta_margin = 25, rho_margin = 25):
    #        if (min_degree <= l.theta()) and (l.theta() <= max_degree):
    #            img.draw_line(l.line(), color = (255, 0, 0))
    else:
        print('not found!')
