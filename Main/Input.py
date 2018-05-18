import time


letter_width = [['a', 1.9],
                ['b', 2.2],
                ['c', 1.8],
                ['d', 2.2],
                ['e', 1.9],
                ['f', 1.35],
                ['g', 2.2],
                ['h', 2.2],
                ['i', 1],
                ['j', 1.1],
                ['k', 2.1],
                ['l', 1],
                ['m', 3.3],
                ['n', 2.2],
                ['o', 2.2],
                ['p', 2.2],
                ['q', 2.2],
                ['r', 1.45],
                ['s', 1.8],
                ['t', 1.35],
                ['u', 2.15],
                ['v', 1.8],
                ['w', 2.5],
                ['x', 2.2],
                ['y', 1.8],
                ['z', 2],
                ['1', 2.2],
                ['2', 2.2],
                ['3', 2.2],
                ['4', 2.2],
                ['5', 2.2],
                ['6', 2.2],
                ['7', 2.2],
                ['8', 2.2],
                ['9', 2.2],
                ['0', 2.2],
                [' ', 1.3],
                ['.', 1.1]]


inputs = []


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
        self.hover = False

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
        text(self.txt, self.x, self.y-self.text_size/2)

    #Estimate width of text
    def estimate_string_width(string_check=""):
        width_score = 0
        letter_found = False
        for each_letter in string_check:
            for check_letter_list in range(len(letter_width)):
                if each_letter == letter_width[check_letter_list][0]:
                    width_score += letter_width[check_letter_list][1]
                    letter_found = True
                
                elif each_letter.lower() == letter_width[check_letter_list][0]:
                    width_score += letter_width[check_letter_list][1] * 1.2
                    letter_found = True
        
            if letter_found == False:
                width_score += 1.5
    
        return width_score


#Update button appearencs/check for button mouseovers
def update():
    global inputs
    
    over_input = False
    for each_input in inputs:
        each_input.draw_input()
        
        if over_clickable(each_input.x, each_input.y, each_input.wid, each_input.hei): #or input_count == activated_input:
            over_input = True
            each_input.hover = True
            
            if each_input.activated == True:
                cursor(TEXT)
            else:
                cursor(HAND)
        else:
            each_input.hover = False 
            cursor(ARROW)
    
        if each_input.txt != "":
            fill(0)
            textAlign(LEFT)
            
            width_score = each_input.estimate_string_width(each_input.txt)
            
            if width_score < 30:
                each_input.txt_show = each_input.txt
            else:
                minus_string = 0
                while width_score >= 30:
                    width_score = each_input.estimate_string_width(each_input.txt[minus_string:])
                    minus_string += 1
                
                each_input.txt_show = each_input.txt[minus_string-1:]
            
            text(each_input.txt_show, each_input.x, each_input.y + each_input.text_size)
            if (time.time()-time.time()%0.5) % 1 == 0:
                stroke(0)
                line_x = estimate_string_width(each_input.txt_show[each_input.edit_position:])*each_input.text_size/3.6
                line(each_input.x + line_x + each_input.text_size/5, each_input.y + each_input.hei/7, each_input.x + line_x + each_input.text_size/5, each_input.y + each_input.hei/1.3)
                
#Keypress to type in an input
def keypressed():
    global inputs
    
    activated_input = None
    for find_active in inputs:
        if find_active.activated:
            activated_input = find_active
    
    if activated_input != None:
        #Left Shift
        if keyCode == 37:
            if len(activated_input.txt_show) > activated_input.edit_position:
                activated_input.edit_position += 1
        
        #Right Shift
        if keyCode == 39:
            if activated_input.edit_position > 0:
                activated_input.edit_position -= 1
        #Enter
        #"""
        #if keyCode == 10:
            #user_input = text_inputed[activated_input]
            #text_inputed[activated_input] = ""
            #input_given(user_input)
            #activated_input = -1
        #"""
        #Delete   
        elif keyCode == 8:
            if len(activated_input.txt) > 0 and activated_input.edit_position >= 0:
                activated_input.txt = activated_input.txt[:len(activated_input.txt)-activated_input.edit_position-1] + activated_input.txt[len(activated_input.txt)-activated_input.edit_position:]
                    
        #If not an invalid key (Ex. page up/home) then add the key to the input box
        elif str(key) != "65535":
            if activated_input.edit_position == -1:
                activated_input.txt += str(key)
            else:
                activated_input.txt = activated_input.txt[:len(activated_input.txt)-activated_input.edit_position] + str(key) + activated_input.txt[len(activated_input.txt)-activated_input.edit_position:]
    
                
#Check for button click
def mousepressed():
    global inputs
    input_clicked = False
    
    activated_id = None
    
    for each_input in inputs:
        if each_input.activated:
            activated_id = each_input.id
    
    for each_input in inputs:
        if over_clickable(each_input.x, each_input.y, each_input.wid, each_input.hei):
            input_clicked = True
            if each_input.id != activated_id:
                for other_inputs in inputs:
                    other_inputs.activated = False
                
                activated_id = each_input.id
                each_input.activated = True
                each_input.edit_position = 0
            else:
                for cursor_position in range(len(each_input.txt_show)):
                    fill(0)
                    stroke(0)
                    if mouseX > each_input.x[input_count] + estimate_string_width(each_input.text_show[cursor_position:])*each_input.text_size/3.6:
                        each_input.edit_position = cursor_position
                        break
                    
    
    if input_clicked == False:
        for other_inputs in inputs:
            other_inputs.activated = False
            other_inputs.edit_position = -1

#Check for mouseovers
def over_clickable(x, y, width, height): 
    return x <= mouseX <= x + width and y <= mouseY <= y + height
