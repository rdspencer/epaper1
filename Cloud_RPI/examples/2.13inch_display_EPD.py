#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

#import 
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
from PIL import Image
   
from waveshare_epd import waveshare_epd 
from tcp_server import tcp_sver 
import socketserver
import traceback
import threading
import logging
import struct
import signal
import fcntl
import time
import math

from progressbar import *

logging.basicConfig(level=logging.INFO)  

class MyServer(tcp_sver.tcp_sver):
    def handle(self):
        try:
            self.client = self.request
            #get id
            self.Get_ID()  
            #unlock if password = 123456
            self.unlock('123456')
            #init epd setting
            epd = waveshare_epd.EPD(2.13)
            #set image size
            self.set_size(epd.width,epd.height)
            #font 
            font18 = ImageFont.truetype(os.path.join(picdir, 'Font01.ttc'), 18)
            font24 = ImageFont.truetype(os.path.join(picdir, 'Font01.ttc'), 24)
            font35 = ImageFont.truetype(os.path.join(picdir, 'Font02.ttf'), 35)
            
            #creat new Image and draw the image
            Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
            Himage = Himage.transpose(Image.ROTATE_90)
            draw = ImageDraw.Draw(Himage)
            draw.text((0, 0 ), 'hello world', font = font18, fill = 0)
            draw.text((0, 15), 'waveshare', font = font24, fill = 0)
            draw.text((0, 40), '2.13inch e-Paper', font = font24, fill = 0)        
            draw.text((0, 90), u'微雪电子', font = font35, fill = 0) 
            draw.line((5,65,25,85), fill = 0)
            draw.line((5,85,25,65), fill = 0)
            draw.rectangle((5 ,65,25,85), outline = 0)
            draw.rectangle((30,65,50,85), fill = 0)

            draw.line((55, 75, 75, 75), fill = 0)
            draw.line((65, 65, 65, 85), fill = 0)
            draw.arc((55, 65, 75, 85),0,360, fill = 0)  
            draw.chord((80,65,100,85), 0, 360, fill = 0) 

            Himage = Himage.transpose(Image.ROTATE_270)
            self.flush_buffer(epd.getbuffer(Himage))
            #open image files
            Himage = Image.open(os.path.join(picdir, '2in13d.bmp'))
            Himage = Himage.transpose(Image.ROTATE_270)
            #display
            self.flush_buffer(epd.getbuffer(Himage))  
            
            self.Send_cmd('S')                    
        except ConnectionResetError :
            self.Wait_write("lose connect.")
        except KeyboardInterrupt :
            self.close()
            os.system("clear")
        #except :
        #    pass
            
        
if __name__ == "__main__":
    ip=tcp_sver.get_host_ip()
    logging.info('{0}'.format(ip))
    socketserver.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer((ip, 6868, ), MyServer)    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        os.system("clear")
    #except :
    #    pass
        
        


