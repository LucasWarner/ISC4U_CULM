# -------------------------------------------------------------------------------

# Name:           StartPage.py

# Purpose:        File for start page class

# Author:         Warner.Lucas, McKeen.Kaden

#

# Created:        13/04/2018

# ------------------------------------------------------------------------------

class StartPage(object):
    def __init__ (self,tx,ty,x,y,s,FS):
        start_page = loadImage("Cover.jpeg")
        yes = loadImage("CheckMark.png")
        no = loadImage("RedNo.png")
        image(start_page,0,0,width,height)
        if FS == "True":
            image(yes,x,y,s,s)
        else:
            image(no,x,y,s,s)
        fill(0)
        text("FullScreen:",tx,ty)
    def Del(self):
        del self
        clear()
    
        
    
