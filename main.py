from utils import * #imports utils

#while the program is running
while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False #close program with x button
            
        #holding the mouse down
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:#left click
                rx,ry=evt.pos
            if evt.button==4:#scroll up
                radius+=1 #change brush size
            if evt.button==5:#scroll down
                if radius<=1:
                    pass #cant make the brush smaller than 1
                else:
                    radius-=1
                    
        #holding the mouse up
        if evt.type==MOUSEBUTTONUP:
            if tool=="pencil" or tool=="eraser" or tool=="brush": #to show current tool used
                screen.blit(screenCap,canvasRect) #displays screenshot
                screenCap=screen.subsurface(canvasRect).copy()
                
            #making sure the stamps dont leave a trail
            if tool=="stamp1" and canvasRect.collidepoint(mx,my):
                screen.set_clip(canvasRect) #only shows in canvas
                screen.blit(screenCap, canvasRect) #paste screenshot
                screen.blit(stamp1Pic, (mx-w1//2,my-h1//2)) #paste stamp
                screen.set_clip(None) #back to "normal"
            if tool=="stamp2" and canvasRect.collidepoint(mx,my):
                screen.set_clip(canvasRect)
                screen.blit(screenCap, canvasRect)
                screen.blit(stamp2Pic, (mx-w2//2,my-h2//2))
                screen.set_clip(None)
            if tool=="stamp3" and canvasRect.collidepoint(mx,my):
                screen.set_clip(canvasRect)
                screen.blit(screenCap, canvasRect)
                screen.blit(stamp3Pic, (mx-w3//2,my-h3//2))
                screen.set_clip(None)
            if tool=="stamp4" and canvasRect.collidepoint(mx,my):
                screen.set_clip(canvasRect)
                screen.blit(screenCap, canvasRect)
                screen.blit(stamp4Pic, (mx-w4//2,my-h4//2))
                screen.set_clip(None)
            if tool=="stamp5" and canvasRect.collidepoint(mx,my):
                screen.set_clip(canvasRect)
                screen.blit(screenCap, canvasRect)
                screen.blit(stamp5Pic, (mx-w5//2,my-h5//2))
                screen.set_clip(None)
            if tool=="stamp6" and canvasRect.collidepoint(mx,my):
                screen.set_clip(canvasRect)
                screen.blit(screenCap, canvasRect)
                screen.blit(stamp6Pic, (mx-w6//2,my-h6//2))
                screen.set_clip(None)
            screenCap=screen.subsurface(canvasRect).copy()
            
    mx,my=mouse.get_pos()#mouseX and mouseY positions
    mb=mouse.get_pressed()#mb is a tuple (0,0,0) if no button pressed
    
    #allows file saving
    if SaveRect.collidepoint(mx,my) and mb[0]:
        fname=filedialog.asksaveasfilename(defaultextension=".png") #automatically saves as png
        if fname=="": #if you cancel save, it wont crash
            pass
        else:
            partialImage=screen.subsurface(canvasRect).copy()#takes a partial screen shot
            image.save(partialImage,fname) #save image
            
    #allows file loading
    if LoadRect.collidepoint(mx,my) and mb[0]:
        fname=filedialog.askopenfilename()
        dot=fname.rfind(".")
        exten=fname[dot+1:] #find extension name
        if fname!="" and (exten =="png" or exten=="jpg" or exten=="jpeg"): #wont crash if you try to load unsupported file or cancel
            loadimg=image.load(fname) #load image
            newloadimg=transform.scale(loadimg, (780,610))
            screen.blit(newloadimg, (0,125)) #paste loaded image
            screenCap=screen.subsurface(canvasRect).copy()
        else:
            pass

    #clear bg
    if loadBg4.collidepoint(mx,my) and mb[0]:
        draw.rect(screen, WHITE, canvasRect)
        screenCap=screen.subsurface(canvasRect).copy()
        
    #load backgrounds
    for i in range(3):
        if loadBg[i].collidepoint(mx,my) and mb[0]:
            newBg[i]=transform.scale(newBg[i], (780,610))
            screen.blit(newBg[i], (0,125))
            screenCap=screen.subsurface(canvasRect).copy()
            
    #mode colors
    for i in range(len(tools)):
        if modes[i]==0:
                draw.rect(screen,GREY,tools[i],2)
        elif modes[i]==1:
                draw.rect(screen,BLUE,tools[i],2)
        else:
                draw.rect(screen,RED,tools[i],2)
            
    #change mode if hover, click or neutral 
    for i in range(len(tools)):
        if tools[i].collidepoint(mx,my) and mb[0]:
            modes=[0,0,0,0,0,0,0,0,0,0,0,0,0]
            modes[i]=2
        if modes[i]!=2 and tools[i].collidepoint(mx,my):
            modes[i]=1
        if not tools[i].collidepoint(mx,my) and modes[i]!=2:
            modes[i]=0
            
    #selecting the tool
    if mb[0]:
        for i in range(len(toolVal)):
            if tools[i].collidepoint(mx,my):
                tool=toolVal[i]
        if fillRect.collidepoint(mx,my):
            fill=True
        if outlineRect.collidepoint(mx,my):
            fill=False
            
    #only draw on canvas while clicking
    if canvasRect.collidepoint(mx,my) and mb[0]:
        mouse.set_visible(False) #hide cursor when clicking on canvas
        myRect=Rect(rx, ry, mx-rx, my-ry) #to change size using starting position and new position
        myRect.normalize() #negative numbers for ellipse tool
        dist=distance(omx,omy,mx,my)
        distx=mx-omx
        disty=my-omy
        screen.set_clip(canvasRect)#only the canvas area can be updated

        #freehand draw-shows current tool by having an image follow the cursor
        if tool=="pencil":
            screen.blit(screenCap, canvasRect)
            draw.line(screen,col,(omx,omy),(mx,my), 3)
            screenCap=screen.subsurface(canvasRect).copy()
            screen.blit(pencilTool,(mx,my))
        if tool=="eraser":
            screen.blit(screenCap, canvasRect)
            for i in range(1,int(dist),1): #makes the eraser smooth         
                dx=omx+distx*i/dist  #run
                dy=omy+disty*i/dist  #rise
                draw.circle(screen,bgcol,(int(dx),int(dy)),radius) 
            screenCap=screen.subsurface(canvasRect).copy()
            screen.blit(eraserTool,(mx,my))
            
        #brush+spray paint   
        if tool=="brush": #has imagine following cursor
            screen.blit(screenCap, canvasRect)
            for i in range(1,int(dist),1):          
                dx=omx+distx*i/dist  #run
                dy=omy+disty*i/dist  #rise
                draw.circle(screen,col,(int(dx),int(dy)),radius)
            screenCap=screen.subsurface(canvasRect).copy()
            screen.blit(brushTool,(mx,my))
        if tool=="spray":
            for i in range(10):
                rx = randint(-radius, radius) #random range using radius
                ry = randint(-radius, radius)
                dist = distance(mx, my, mx + rx, my + ry) 
                if dist < radius:
                    draw.circle(screen, col, (mx - rx, my - ry), 1) #draws random dotes of the same size

        #basic shapes
        if tool=="line":
            screen.blit(screenCap, canvasRect)
            draw.line(screen, col, (rx,ry),(mx,my), radius) #start and end
        if tool=="ellipse":
            screen.blit(screenCap, canvasRect)
            if fill==False: #option to fill shape
                draw.ellipse(screen, col, myRect, radius)
            else:
                draw.ellipse(screen, col, myRect)
        if tool=="rect":
            screen.blit(screenCap, canvasRect)
            if fill==False:
                draw.rect(screen, col, myRect, radius)
            else:
                draw.rect(screen, col, myRect)

        #stamp pictures
        if tool=="stamp1":
            screen.blit(screenCap, canvasRect)
            if mb[0]:
                screen.blit(stamp1Pic, (mx-w1//2, my-h1//2)) #paste certain stamp
        if tool=="stamp2":
            screen.blit(screenCap, canvasRect)
            if mb[0]:
                screen.blit(stamp2Pic, (mx-w2//2, my-h2//2))
        if tool=="stamp3":
            screen.blit(screenCap, canvasRect)
            if mb[0]:
                screen.blit(stamp3Pic, (mx-w3//2, my-h3//2))
        if tool=="stamp4":
            screen.blit(screenCap, canvasRect)
            if mb[0]:
                screen.blit(stamp4Pic, (mx-w4//2, my-h4//2))
        if tool=="stamp5":
            screen.blit(screenCap, canvasRect)
            if mb[0]:
                screen.blit(stamp5Pic, (mx-w5//2, my-h5//2))
        if tool=="stamp6":
            screen.blit(screenCap, canvasRect)
            if mb[0]:
                screen.blit(stamp6Pic, (mx-w6//2, my-h6//2))
        screen.set_clip(None)
    else:
        mouse.set_visible(True) #show mouse cursor if not clicking
        
    if paletteRect.collidepoint(mx,my) and mb[0]: #select (change) colour
        col=screen.get_at((mx,my)) #get the color
        
    omx,omy=mx,my #old positions is assigned to the current position
    
    display.flip()
            
quit()
