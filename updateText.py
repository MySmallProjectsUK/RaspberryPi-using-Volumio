# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont

import os



# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
#draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 2
#shape_width = 20
top = padding
#bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = padding
# Draw an ellipse.
#draw.ellipse((x, top , x+shape_width, bottom), outline=255, fill=0)
#x += shape_width+padding
# Draw a rectangle.
#draw.rectangle((x, top, x+shape_width, bottom), outline=255, fill=0)
#x += shape_width+padding
# Draw a triangle.
#draw.polygon([(x, bottom), (x+shape_width/2, top), (x+shape_width, bottom)], outline=255, fill=0)
#x += shape_width+padding
# Draw an X.
#draw.line((x, bottom, x+shape_width, top), fill=255)
#draw.line((x, top, x+shape_width, bottom), fill=255)
#x += shape_width+padding

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('Minecraftia.ttf', 8)

# Write two lines of text.
#x = 0
#top = 0
draw.text((x, top),    'Hello',  font=font, fill=255)
#draw.text((x, top+20), 'World!', font=font, fill=255)

#f = os.popen('date')
#f2= os.popen('./example | grep "title: "')
#now = f.read()
#data = f2.read()
#print "Today is", now
#print "Playing: ", data

#draw.text((x, top+10), data, font=font, fill=255)


# Display image.
#disp.image(image)
disp.display()

#i = 0
#while i < 120:
#	print "Number %d \n" % i
#	i = i +1

print "starting loop"

data0=""
data1=""
data2=""
data3=""
updateCount = 0

while (True):
	updateCount+=1
	print "Data" , data2 , ", x: " , x
	time.sleep(0.20)
	
        # Clear image buffer by drawing a black filled box.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

	#get data
	if(updateCount > 10):
		f2 = os.popen('./mpdGetInfo | grep "title: " | sed  "s/title: //g"')		
		f1 = os.popen('./mpdGetInfo | grep "artist: " | sed  "s/artist: //g"')
		f3 = os.popen('./mpdGetInfo | grep "album: " | sed  "s/album: //g"') 
		f0 = os.popen('./mpdGetInfo | grep "elaspedTime: " | sed  "s/elaspedTime: //g"')
		data1 = f1.read()
		data2 = f2.read()
		data3 = f3.read()
		data0 = f0.read()

		updateCount = 0

	if( not data0):
		fdata0 = 0
	else:
		fdata0 = float(data0)

	# if just started track, then show at pos +60
	if(fdata0 < 10): x = -60
	#print "fdata3:",fdata3

	# show it
	draw.text((0, top), data1, font=font, fill=255)
	draw.text((-x, top+10), data2, font=font, fill=255)
	draw.text((0, top+20), data3, font=font, fill=255)

	#Draw the image buffer
	disp.image(image)
	disp.display()
	
	x = x + 5
	if (x > width):
		x = -width


print "All Done"


