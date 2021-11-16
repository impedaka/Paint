from pygame import *
from tkinter import *
from tkinter import filedialog
root=Tk()
root.withdraw()#hides the extra window

font.init()
width,height=1200,900
screen=display.set_mode((width,height))
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
#config
tool=""
radius=10
bgcol=WHITE
col=BLACK
running=True
#bg image
bgPic = image.load("background.jpg")
newbgPic=transform.scale(bgPic, (width,height))
screen.blit(newbgPic, (0, 0)) #original image
#tool images
canvasRect=Rect(0,125,780,610)
pencilRect=Rect(225,35,25,25)
stampRect=Rect(200,200,25,25) #
eraserRect=Rect(225, 65, 25,25)
paletteRect=Rect(760,32,200,15)
#draw.rect(screen, BLACK, paletteRect)
draw.rect(screen,WHITE,canvasRect)
draw.rect(screen,BLACK, stampRect) #
cols=[BLACK,GREY,BROWN,RED, ORANGE,YELLOW,GREEN,BLUE, DARKBLUE,PURPLE]
for i in range(len(cols)):
    draw.rect(screen,cols[i],(i*22+752,32,15,15))

applePic=image.load("/paint/saveicon.png")
w=applePic.get_width()
h=applePic.get_height()
screenCap=screen.subsurface(canvasRect).copy()

#display words
'''
monFont=font.SysFont("Montserrat", 55)
wordPic=monFont.render("paint project", True, WHITE)
screen.blit(wordPic, (0,0))
'''
#save icon
SaveRect=Rect(1110,40,25,25)
Icon=image.load("saveicon.png")
SaveIcon=transform.scale(Icon, (25,25))
screen.blit(SaveIcon, (1110,40))

#load icon
LoadRect=Rect(1110,80,25,25)
loadicon=image.load("uploadicon.png")
newloadicon=transform.scale(loadicon, (25,25))
screen.blit(newloadicon, (1110, 80))

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
               
    mx,my=mouse.get_pos()#mouseX and mouseY positions
    mb=mouse.get_pressed()#mb is a tuple (0,0,0) if no button pressed
    #stamp
    #saves 
    if SaveRect.collidepoint(mx,my) and mb[0]:
        fname=filedialog.asksaveasfilename(defaultextension=".png")
        partialImage=screen.subsurface(canvasRect).copy()#takes a partial screen shot
        image.save(partialImage,fname)
    #loads
    if LoadRect.collidepoint(mx,my) and mb[0]:
        fname=filedialog.askopenfilename()
        loadimg=image.load(fname)
        newloadimg=transform.scale(loadimg, (780,610))
        screen.blit(newloadimg, (0,125))
        
    draw.rect(screen, GREY, pencilRect, 1)
    draw.rect(screen, GREY, eraserRect,1 )
    #selecting the tool
    if mb[0]:
        if pencilRect.collidepoint(mx,my):
           tool="pencil"
        if eraserRect.collidepoint(mx,my):
           tool="eraser"
        #if stampRect.collidepoint(mx,my):
           #tool="stamp"
    #screen.blit(screenCap, canvasRect)
    if canvasRect.collidepoint(mx,my) and mb[0]:
        screen.set_clip(canvasRect)#only the canvas area can be updated
        if tool=="pencil":
            draw.line(screen,col,(omx,omy),(mx,my), radius)     
        if tool=="eraser":
            draw.circle(screen,bgcol,(mx,my),radius)
        if tool=="stamp":
            if evt.type==MOUSEBUTTONUP:
                screen.blit(screenCap, canvasRect)
                screen.blit(applePic, (mx-w//2,my-h//2))
                screenCap=screen.subsurface(canvasRect).copy()
                screen.blit(applePic, (mx-w//2,my-h//2))
            
        #at the end of the "using the tools" section
        #you need to go back to "normal" state of updating the screen
        screen.set_clip(None)#back to "normal"


    #select (change) colour
    if paletteRect.collidepoint(mx,my) and mb[0]:
        col=screen.get_at((mx,my))
    omx,omy=mx,my
    display.flip()
            
quit()
