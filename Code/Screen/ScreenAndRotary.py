#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch
from PIL import Image,ImageDraw,ImageFont
from RPi import GPIO

# Rotary encoder
clk = 17
dt = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 30
clkLastState = GPIO.input(clk)

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)
try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    # disp = LCD_2inch.LCD_2inch(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_2inch.LCD_2inch()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()

    while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
                if counter > 58:
                    counter = 0
            else:
                counter -= 1
                if counter < 11:
                    counter = 30

            print(counter)

            image = Image.open(
                f'/home/[user_name]/WiggleR/Pictures/small/2023-10-20-13-{counter}.jpg')
            image = image.rotate(180)
            disp.ShowImage(image)
        clkLastState = clkState
        time.sleep(0.01)
except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
finally:
    GPIO.cleanup()
    disp.module_exit()
