# -------------------------------------------------------------------------------

# Name:           CheckBox.py

# Purpose:        File for checkbox class

# Author:         Warner.Lucas, McKeen.Kaden

#

# Created:        13/04/2018

# ------------------------------------------------------------------------------

checkboxes=[]

class Checkbox(object):
    def __init__(self,id,x,y,clicked=False):
        self.id = id
        self.x = x
        self.y = y
        self.clicked = clicked
    #def setup(self):
        
    
    def render(self):
        stroke(0)
        if self.is_over():
            fill(200)
        else:
            fill(255)
        rect(self.x, self.y, 20, 20)
        if self.clicked:
            line(self.x, self.y, self.x+20, self.y+20)
            line(self.x, self.y+20, self.x+20, self.y)
    
    def click(self):
        if self.is_over():
            self.clicked= not self.clicked
    
    def is_over(self):
        return mouseX>self.x and mouseX<self.x+20 and mouseY>self.y and mouseY<self.y+20
    
def mousepressed(id):
    for each_box in checkboxes:
        if each_box.id == id:
            each_box.click()
