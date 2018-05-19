
# -------------------------------------------------------------------------------

# Name:           start_page.py

# Purpose:        start_page for final project

# Author:         Warner.Lucas, McKeen.Kaden

#

# Created:        13/04/2018

# ------------------------------------------------------------------------------
import MainPage
import StartPage
import Button
import ScheduleBar
import Input

def settings():
    if full_bol() == "True":
        fullScreen()
    else:
        size(800,600)
def setup():
    global Start_Page,first_page, second_page
    second_page = False
    first_page = True
    fill(0)
    Start_Page = StartPage.StartPage(dim(20, 'y'),dim(500),dim(40, 'y'),dim(620),dim(15, 'y'),dim(40),full_bol())
def setup_2():
    global first_page,second_page,Main_Page
    Main_Page = MainPage.MainPage()
    first_page = False
    Start_Button.Del()
    Exit_Button.Del()
    Start_Page.Del()
    #ScheduleBar.Setup()
    #Input.inputs.append(Input.input(0,dim(100),dim(200,'y'),dim(25,'y'),dim(150),dim(20, 'y')))
    second_page = True
def draw():
    if first_page == True:
        update1(mouseX,mouseY)
    else:
        update2(mouseX,mouseY)
def update1(x, y):
    global over_start_button, over_exit_button, over_full,Start_Button,Exit_Button
    over_start_button = over_clickable(dim(500), dim(460, 'y'), dim(200), dim(60, 'y'))
    over_exit_button = over_clickable(dim(500), dim(380, 'y'), dim(200), dim(60, 'y'))
    over_full =over_clickable(dim(620), dim(15, 'y'), dim(40), dim(40))
    Start_Button = Button.Button(dim(500), dim(460, 'y'), dim(200), dim(60, 'y'),dim(400),"Get Started")
    Exit_Button = Button.Button(dim(500), dim(380, 'y'), dim(200), dim(60, 'y'),dim(400),"Exit")
    
    #Start_Button
    if over_start_button:
        Start_Button.display(210,215,45,0,2,2,0,0)
    else:
        Start_Button.display(0,150,150,240)
    #Exit_Button
    if over_exit_button:
        Exit_Button.display(210,215,45,0,2,2,0,0)
    else:
        Exit_Button.display(0,150,150,240)
    #Opening Paragragh
    strokeWeight(2)
    stroke(240)
    fill(0,150,150)
    if width == 1600:
        rect(dim(40), dim(265, 'y'), dim(340), dim(300, 'y'), dim(40))
    else:
        rect(dim(40), dim(265, 'y'), dim(420), dim(300, 'y'), dim(40))
    fill(0)
    noStroke()
    text("Welcome to Overload, the organizational\nprogram you wish you'd always had. \nWe're there for whatever you need to \norganize. Easy, quick, and ready to go, \nOverload is good for daily and monthly \nscheduling, tournaments and games, \nas well as other more personal events. \nWith an array of useful and hand-crafted \nsettings, we have what you need.",dim(55), dim(300, 'y'))


def update2(x,y):
    Main_Page.update()
    #ScheduleBar.update()
    #Input.update()
    
def mousePressed():
    global first_page,second_page
    if first_page:
        if over_exit_button:
            exit()
        if over_start_button:
            setup_2()
        if over_full:
            Settings = open("settings.txt","w")
            if FullScreen == "True":
                Settings.write("FullScreen: False")
            else:
                Settings.write("FullScreen: True")
            Settings.close()
            clear()
            full_bol()
            setup()
            
    if second_page:
        pass
        #ScheduleBar.mousepressed()
        #Input.mousepressed()
        
def mouseReleased():
    pass
    #if second_page:
        #ScheduleBar.mousereleased()
        
def keyPressed():
    if second_page:
        #Input.keypressed()
        pass
        
        
        
def over_clickable(x, y, w, h):
    return x <= mouseX <= x + w and y <= mouseY <= y + h
#All dimensions remain in constant ratios of window size
def dim(y, m = 'X'): 
    if m == 'X':
        return width*y/800
    else:
        return height*y/600
def full_bol():
        global FullScreen
        Settings = open("settings.txt","r")
        for Line in Settings:
            FullScreen = str(Line[12:])
        Settings.close()
        return FullScreen
