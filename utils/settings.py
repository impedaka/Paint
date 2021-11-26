#import everything needed
from pygame import *
from random import *
from math import *
from tkinter import *
from tkinter import filedialog

#settings
root=Tk()
root.withdraw()#hides the extra window
font.init()
width,height=1200,900
screen=display.set_mode((width,height)) #screen size
RED=(237,28,36)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,162,232)
GREEN=(34,177,76)
YELLOW=(255,242,0)
WHITE=(255,255,255)
BROWN=(136,0,21)
ORANGE=(255,128,39)
DARKBLUE=(63,72,204)
PURPLE=(163,73,164)

#function for spray paint
def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

#config
tool="" #current tool
radius=10
bgcol=WHITE
col=BLACK
running=True
sz = 15 #spray paint circle size
fill=False #shapes start as outlines

#background image
bgPic = image.load("./images/background.jpg")
newbgPic=transform.scale(bgPic, (width,height))
screen.blit(newbgPic, (0, 0)) #original image

#tool borders
canvasRect=Rect(0,125,780,610)
pencilRect=Rect(225,35,25,25)
eraserRect=Rect(225, 65, 25,25)
paletteRect=Rect(760,32,200,15)
brushRect=Rect(305, 30, 50,65)
sprayRect=Rect(605, 30, 50, 65)

#select tools
pencil=image.load("./images/penciltool.png")
eraser=image.load("./images/erasertool.png")
brush=image.load("./images/brushtool.png")
pencilTool=transform.scale(pencil, (15,15))
brushTool=transform.scale(brush, (15,15))
eraserTool=transform.scale(eraser, (15,15))

#shape images
lineRect=Rect(365,35,20,15)#line, rect and ellipse
rectRect=Rect(430,35,20,15)
ellipseRect=Rect(405,35,20,15)
outlineRect=Rect(525, 35, 70, 15)
fillRect=Rect(525, 55, 70, 15)

#canvas is white
draw.rect(screen,WHITE,canvasRect)

#stamp rectangles
stamp1Rect=Rect(900,200,50,50)
stamp2Rect=Rect(1000,200,50,50)
stamp3Rect=Rect(1100,200,50,50)
stamp4Rect=Rect(900,300,50,50)
stamp5Rect=Rect(1000,300,50,50)
stamp6Rect=Rect(1100,300,50,50)
stamps=[stamp1Rect, stamp2Rect, stamp3Rect,stamp4Rect,stamp5Rect,stamp6Rect]

#load all stamp images
stamp1Pic=image.load("images/stamp1.png")
stamp2Pic=image.load("images/stamp2.png")
stamp3Pic=image.load("images/stamp3.png")
stamp4Pic=image.load("images/stamp4.png")
stamp5Pic=image.load("images/stamp5.png")
stamp6Pic=image.load("images/stamp6.png")

#get width and height of all stamps
w1=stamp1Pic.get_width()
h1=stamp1Pic.get_height()
w2=stamp2Pic.get_width()
h2=stamp2Pic.get_height()
w3=stamp3Pic.get_width()
h3=stamp3Pic.get_height()
w4=stamp4Pic.get_width()
h4=stamp4Pic.get_height()
w5=stamp5Pic.get_width()
h5=stamp5Pic.get_height()
w6=stamp6Pic.get_width()
h6=stamp6Pic.get_height()
stampPic=[stamp1Pic, stamp2Pic,stamp3Pic,stamp4Pic,stamp5Pic,stamp6Pic]
k=0

#load preview of stamps
for i in range(2):
    for j in range(3):
        draw.rect(screen, BLACK, stamps[k],2)
        stampPic[k]=transform.scale(stampPic[k], (50, 50))
        screen.blit(stampPic[k], (900+100*j, 200+100*i))
        k+=1
        
#load color preview
cols=[BLACK,GREY,BROWN,RED, ORANGE,YELLOW,GREEN,BLUE, DARKBLUE,PURPLE]
for i in range(len(cols)):
    draw.rect(screen,cols[i],(i*22+752,32,15,15))

#display words
monFont=font.SysFont("Montserrat", 55)
wordPic=monFont.render("MS-Paint", True, BLACK)
screen.blit(wordPic, (25,55))

#save icon
SaveRect=Rect(1110,40,25,25)
Icon=image.load("./images/saveicon.png")
SaveIcon=transform.scale(Icon, (25,25))
screen.blit(SaveIcon, (1110,40))

#load bg
loadBg1=Rect(900, 400, 75,50)
loadBg2=Rect(1000, 400, 75,50)
loadBg3=Rect(900, 500, 75,50)
loadBg4=Rect(1000, 500, 75,50)
loadBg=[loadBg1, loadBg2, loadBg3, loadBg4] #rectangle positions
Bg1=image.load("./images/bg1.png") #load bg images
Bg2=image.load("./images/bg2.jpg")
Bg3=image.load("./images/bg3.jpg")
Bg4=image.load("./images/bg4.jpg")
BgPic=[Bg1,Bg2,Bg3,Bg4] #showing the preview
newBg=[Bg1, Bg2, Bg3] #high resolution
p=0
for i in range(2): #show bg preview
    for j in range(2):
        draw.rect(screen, GREY, loadBg[p], 5)
        BgPic[p]=transform.scale(BgPic[p], (75, 50))
        screen.blit(BgPic[p], (900+100*j, 400+100*i))
        p+=1
        
#load icon
LoadRect=Rect(1110,80,25,25)
loadicon=image.load("./images/uploadicon.png")
newloadicon=transform.scale(loadicon, (25,25))
screen.blit(newloadicon, (1110, 80))

#hover, select, and neutral
tools=[pencilRect,eraserRect, lineRect,ellipseRect, rectRect, brushRect, sprayRect, stamp1Rect, stamp2Rect, stamp3Rect, stamp4Rect,stamp5Rect, stamp6Rect]
modes=[0,0,0,0,0,0,0,0,0,0,0,0,0]
toolVal=["pencil","eraser","line","ellipse","rect", "brush","spray","stamp1","stamp2","stamp3","stamp4","stamp5", "stamp6"]
                
#spray paint perview
sprayPic=image.load("./images/spray.png")
newsprayPic=transform.scale(sprayPic, (50,65))
screen.blit(newsprayPic, (605, 30))

#draw outline boxes
draw.rect(screen, GREY, outlineRect, 2)
draw.rect(screen, GREY, fillRect,2)

#extra
display.set_caption("Untitled - Paint") #title of the program
screenCap=screen.subsurface(canvasRect).copy() #screen capture
