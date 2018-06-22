# -------------------------------------------------------------------------------

# Name:           MainPage.py

# Purpose:        File for main page class

# Author:         Warner.Lucas, McKeen.Kaden

#

# Created:        13/04/2018

# ------------------------------------------------------------------------------

class MainPage:
    def __init__(self):
        global main_page
        main_page = loadImage("background.jpg")
        
    def update(self):
        image(main_page,0,0,width,height)
        noStroke()
        fill(10,190)
        rect(0,0,self.dim(180),height)
        
        rect(self.dim(200),self.dim(20,'y'),self.dim(550),height-self.dim(20,'y'),self.dim(10,'y'))
    def Del(self):
        del self
        clear()
    def dim(self,y, m = 'X'): 
        if m == 'X':
            return width*y/800
        else:
            return height*y/600
