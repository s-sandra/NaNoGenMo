"""
Author: Sandra Shtabnaya
DGST 301C: Creative Coding, UMW, Fall 2019
NaNoGenMo Novel: ASCII Flipbook
"""

import os
import cv2
from PIL import Image
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics



""" 
ASCII generator from https://gist.github.com/cdiener/10567484

:param f: 		the image name
:param SC:	 	scaling factor
:param GCF: 	intensity correction factor

:returns:		string of ascii art
"""
def ascii_gen(f, SC, GCF):
    chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))
    WCF = 7/4  # width correction factor

    img = Image.open(f)
    S = ( round(img.size[0]*SC*WCF), round(img.size[1]*SC) )
    img = np.sum( np.asarray( img.resize(S) ), axis=2)
    img -= img.min()
    img = (1.0 - img/img.max())**GCF*(chars.size-1)

    output = "\n".join( ("".join(r) for r in chars[img.astype(int)]) )
    return output


## video to convert to novel goes here ##
video_file = "your_video_name.mp4"

## folder name where video frames are stored goes here ##
output_folder = "your_folder_name"

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

## name of novel goes here ##
novel_name = "your_novel_name"


video = cv2.VideoCapture(video_file)
if not video.isOpened():
    video.open()

successful, image = video.read()
successful = True
frame_num = 0

# while there are frames to read
while successful:
    cv2.imwrite(output_folder + "\\frame%03d.jpg" % frame_num, image)
    frame_num += 1
    successful, image = video.read()
    
video.release()
	
FONT = "Courier"
FONT_SIZE = 14
INTENSITY = 1.6
SCALING = 1/10

file = os.listdir(output_folder)[0] # read first frame
output = ascii_gen(output_folder + '/' + file, SCALING, INTENSITY)
full_output = output
lines = output.split('\n')

width = pdfmetrics.stringWidth(lines[0], FONT, FONT_SIZE)
height = FONT_SIZE * 1.2 * len(lines) # 1.2 is standard line height
c = canvas.Canvas(novel_name + ".pdf", pagesize=(width, height))

for file in os.listdir(output_folder)[1:]:
    output = ascii_gen(output_folder + '/' + file, SCALING, INTENSITY)
    lines = output.split('\n')
    textobject = c.beginText()
    textobject.setFont(FONT, FONT_SIZE)
    textobject.setTextOrigin(0, height - 10)

    lines = output.split('\n')

    for line in lines:
        textobject.textLine(line)

    c.drawText(textobject)
    c.showPage()
    full_output += output

c.save()
os.system(novel_name + ".pdf")

text_file = open(novel_name + ".txt", "w")
n = text_file.write(full_output)
text_file.close()

print("word count: " + str(len(full_output.split(' '))))
