
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
    global first_page,second_page,Main_Page,tri1,tri2,test_list,test2_list,schedule,input
    Main_Page = MainPage.MainPage()
    first_page = False
    Start_Button.Del()
    Exit_Button.Del()
    Start_Page.Del()
    tri2=True
    tri1=True
    schedule=False
    #input=False
    test_list=["Schedule Bar","input","elm2"]
    test2_list=["a","b","c"]
    ScheduleBar.Setup()
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
        Start_Button.display(1,150,150,240)
    #Exit_Button
    if over_exit_button:
        Exit_Button.display(210,215,45,0,2,2,0,0)
    else:
        Exit_Button.display(1,150,150,240)
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
    global over_test_button,side_bar,clickable_list
    Main_Page.update()
    clickable_list=[]
    side_bar=[]
    over_test_button = over_clickable(0, dim(40, 'y'), dim(150), dim(30, 'y'))
    side_bar.append(Button.Button(0, dim(40, 'y'), dim(150), dim(30, 'y'),0,"Test",True,tri1))
    side_bar.append(Button.Button(0, dim(40, 'y'), dim(150), dim(30, 'y'),0,"Test2",True,tri2))
    Y=30
    if tri1==False:
        for opt in test_list:
            side_bar.append(Button.Button(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'),0,str(opt),False,False,14))
            clickable_list.append(over_clickable(0, dim(40+Y, 'y'), dim(150), dim(30, 'y')))
            Y+=30
    if tri2==False:
        for opt in test2_list:
            side_bar.append(Button.Button(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'),0,str(opt),False,False,14))
            clickable_list.append(over_clickable(0, dim(40+Y, 'y'), dim(150), dim(30, 'y')))
            Y+=30
    for elm in side_bar:
        elm.display(0,0,0,255,0,0,0,0)
    if schedule:
        ScheduleBar.update()
    #if input:
        #A lot more work
        #Input.inputs.append(Input.input(0,dim(100),dim(200,'y'),dim(25,'y'),dim(150),dim(20, 'y')))
        #Input.update()
    
def mousePressed():
    global first_page,second_page,tri1,schedule,input
    if second_page:
        if schedule:        
            ScheduleBar.mousepressed()
        #if input:
            #Input.mousepressed()
        
        
        
        if tri1==False:
            print(clickable_list)
            for but in clickable_list:
                if clickable_list[0]==True:
                    schedule = not schedule
                if clickable_list[1]==True:
                    input = not input
        if over_test_button:
            if tri1:
                tri1=False
            else:
                tri1=True
        
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
            
    
        
def mouseReleased():
    if second_page:
        ScheduleBar.mousereleased()
        
def keyPressed():
    if second_page:
        Input.keypressed()
        
        
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
