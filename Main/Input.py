# -------------------------------------------------------------------------------

# Name:           Input.py

# Purpose:        File for input class

# Author:         Warner.Lucas, McKeen.Kaden

#

# Created:        13/04/2018

# ------------------------------------------------------------------------------

import time

from reportlab.pdfbase.pdfmetrics import stringWidth

#List to hold all of the program's inputs
inputs = []

#Input class to hold information on each input
class input(object):
    def __init__(self, id, x, y, hei, wid, text_size):
        self.id = id
        self.x = x
        self.y = y
        self.hei = hei
        self.wid = wid
        self.text_size = text_size
        self.txt = ""
        self.txt_show = ""
        self.edit_position = 0
        self.activated = False
        self.txt_width = 0
        self.show_start = 0 
        self.show_end = 0
        self.hover = False
    
    #Draws the input
    def draw_input(self):
        if self.activated == True:
            stroke(0)
        else:
            noStroke()
        
        #Rectangle
        fill(255)
        rect(self.x, self.y, self.wid, self.hei)
    
        #Text
        textSize(self.text_size)
        textAlign(LEFT)
        noStroke()


#Update button appearencs/check for button mouseovers
def update(update_section):
    global inputs
    
    #Check which inputs to update (Depends on the active page)
    over_input = False
    allowed_inputs = []
    for each_input in inputs:
        
        #If input is on the page (Not scrolled off)
        if each_input.y>70 and each_input.y<750:
            if each_input.id < 30 and update_section == 'teams' or each_input.id==2000 and update_section == 'teams':
                each_input.draw_input()
                allowed_inputs.append(each_input)
                
                if over_clickable(each_input.x, each_input.y, each_input.wid, each_input.hei):
                    cursor(TEXT)
                    over_input = True
        
            if each_input.id == 2000 and update_section == 'teams':
                each_input.draw_input()
                allowed_inputs.append(each_input)
                    
                if over_clickable(each_input.x, each_input.y, each_input.wid, each_input.hei):
                    cursor(TEXT)
                    over_input = True
            
            if each_input.id == 302 and update_section == 'event':
                each_input.draw_input()
                allowed_inputs.append(each_input)
                
                if over_clickable(each_input.x, each_input.y, each_input.wid, each_input.hei):
                    cursor(TEXT)
                    over_input = True
                    
            if each_input.id <=304 and each_input.id >= 303 and update_section == 'monthly':
                each_input.draw_input()
                allowed_inputs.append(each_input)
                
                if over_clickable(each_input.x, each_input.y, each_input.wid, each_input.hei):
                    cursor(TEXT)
                    over_input = True
                    
            if each_input.id <= 301 and each_input.id >= 300 and update_section == 'matches':
                each_input.draw_input()
                allowed_inputs.append(each_input)
                
                if over_clickable(each_input.x, each_input.y, each_input.wid, each_input.hei):
                    cursor(TEXT)
                    over_input = True
                    
            if each_input.id < 180 and each_input.id >= 30 and update_section == 'daily':
                if each_input.y>218 and each_input.y<750:
                    each_input.draw_input()
                    allowed_inputs.append(each_input)
                    
                    if over_clickable(each_input.x, each_input.y, each_input.wid, each_input.hei):
                        cursor(TEXT)
                        over_input = True
    
    
    #If this input is one of those being displayed on screen
    for each_input in allowed_inputs:
        if each_input.txt != "":
            fill(0)
            textAlign(LEFT)
            
            #Calculates the positions and placement of the text
            width_score = stringWidth(each_input.txt,'Helvetica', each_input.text_size)
            if width_score < 140:
                each_input.txt_show = each_input.txt
                add_one = 1
            elif each_input.edit_position > each_input.show_start and each_input.edit_position < each_input.show_end:
                each_input.txt_show = each_input.txt[each_input.show_start:each_input.show_end]
                each_input.show_end = 0
                add_one = 0
            else:
                add_one = 0
                each_input.show_start = 0
                each_input.show_end = len(each_input.txt)
                while width_score >= 140:
                    if each_input.show_end - each_input.edit_position < each_input.edit_position - each_input.show_start:
                        each_input.show_start += 1
                    else:        
                        each_input.show_end -= 1

                    width_score = stringWidth(each_input.txt[each_input.show_start:each_input.show_end],'Helvetica', each_input.text_size)
                    
                    each_input.txt_show = each_input.txt[each_input.show_start:each_input.show_end]
            
            #Draws the input text
            text(each_input.txt_show, each_input.x, each_input.y + each_input.text_size)
            
            #Draws the input box cursor line to show users where they are in the text
            if each_input.activated == True:
                if (time.time()-time.time()%0.5) % 1 == 0:
                    stroke(0)
                    line_x = stringWidth(each_input.txt_show[:each_input.edit_position-each_input.show_start],'Helvetica', each_input.text_size)
                    strokeWeight(1)
                    line(each_input.x + line_x, each_input.y + each_input.hei/6, each_input.x + line_x, each_input.y + each_input.hei/1.2)
    
    #Changes cursor
    if over_input == False:
        cursor(ARROW)


#Keypress to type in an input
def keypressed():
    global inputs
    
    #Find active input
    activated_input = None
    for find_active in inputs:
        if find_active.activated:
            activated_input = find_active
    
    #Type in input, assuming one is active
    if activated_input != None:
        #Left arrow key (Shifts cursor)
        if keyCode == 37:
            if activated_input.edit_position > 0:
                activated_input.edit_position -= 1
        #Right arrow key (Shifts cursor)
        elif keyCode == 39:
            if activated_input.edit_position < len(activated_input.txt):
                activated_input.edit_position += 1
        
        #Delete key
        elif keyCode == 127:
            if len(activated_input.txt) > 0 and len(activated_input.txt) > activated_input.edit_position:
                activated_input.txt = activated_input.txt[:activated_input.edit_position] + activated_input.txt[activated_input.edit_position+1:]
        
        #Backspace   
        elif keyCode == 8:
            if len(activated_input.txt) > 0 and activated_input.edit_position > 0:
                activated_input.txt = activated_input.txt[:activated_input.edit_position-1] + activated_input.txt[activated_input.edit_position:]
                activated_input.edit_position -= 1
    
        #If not an invalid key (Always as an id of 65535 - for example, page up/home) then add the key to the input box
        elif str(key) != "65535":
            activated_input.txt = activated_input.txt[:activated_input.edit_position] + str(key) + activated_input.txt[activated_input.edit_position:]
            activated_input.edit_position += 1


#Check for button click
def mousepressed(mousepressed_section):
    global inputs
    
    #Check which inputs to check for mouse presses (Depends on the active page)
    allowed_inputs = []
    
    for each_input in inputs:
        if each_input.id == 302 and mousepressed_section == 'event':
            allowed_inputs.append(each_input)
                    
        if each_input.id <=304 and each_input.id >= 303 and mousepressed_section == 'monthly':
            allowed_inputs.append(each_input)
                
        if each_input.id <= 301 and each_input.id >= 300 and mousepressed_section == 'matches':
            allowed_inputs.append(each_input)
                
        if each_input.id < 180 and each_input.id >= 30 and mousepressed_section == 'daily':
            allowed_inputs.append(each_input)
             
        if each_input.id < 30 and mousepressed_section == 'teams':
            allowed_inputs.append(each_input)
        
        if each_input.id == 2000 and mousepressed_section == 'teams':
            allowed_inputs.append(each_input)
    
    #Finds activated input
    activated_input = None
    for each_input in allowed_inputs:
        if each_input.activated == True:
            activated_input = each_input.id
    
    #If an input is clicked
    input_clicked = None
    for each_input in allowed_inputs:
        if over_clickable(each_input.x, each_input.y, each_input.wid, each_input.hei):
            input_clicked = each_input.id
            
            #If this input isn't already active (Make active)
            if activated_input != input_clicked:
                each_input.activated = True
                
                for cursor_position in range(len(each_input.txt_show)):
                    fill(0)
                    stroke(0)
                    if mouseX < each_input.x + stringWidth(each_input.txt_show[:cursor_position],'Helvetica', each_input.text_size):
                        if each_input.txt != each_input.txt_show:
                            each_input.edit_position = each_input.txt.index(each_input.txt_show) + cursor_position
                            break
                        else:
                            each_input.edit_position = cursor_position + 2
                            break
            
            #If this input is already active (Change text position to location of cursor)
            else:
                found_position = False
                for cursor_position in range(len(each_input.txt_show)):
                    fill(0)
                    stroke(0)
                    if mouseX < each_input.x + stringWidth(each_input.txt_show[:cursor_position],'Helvetica', each_input.text_size):
                        if each_input.txt != each_input.txt_show:
                            each_input.edit_position = each_input.txt.index(each_input.txt_show) + cursor_position
                            found_position = True
                            break
                        else:
                            each_input.edit_position = cursor_position
                            found_position = True
                            break
                
                if found_position == False and mouseX > each_input.x + stringWidth(each_input.txt_show,'Helvetica', each_input.text_size):
                    if each_input.txt != each_input.txt_show:
                        each_input.edit_position = each_input.txt.index(each_input.txt_show) + len(each_input.txt_show)
                    else:
                        each_input.edit_position = len(each_input.txt_show)
    
    #Deactivate any input that may have been active before, but wasn't clicked on
    for each_input in allowed_inputs:
        if each_input.id != input_clicked:
            each_input.activated = False    
    
    #Deactive all inputs if none were clicked on
    if input_clicked == None:
        for other_inputs in allowed_inputs:
            other_inputs.activated = False
        
#Check for mouseovers
def over_clickable(x, y, width, height): 
    return x <= mouseX <= x + width and y <= mouseY <= y + height
