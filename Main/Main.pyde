
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
    #set fullscreen or (800,600)
    if full_bol() == "True":
        fullScreen()
    else:
        size(800,600)
def setup():
    global Start_Page, first_page, second_page
    #Set up opening page
    second_page = False
    first_page = True
    Start_Page = StartPage.StartPage(dim(20, 'y'),dim(500),dim(40, 'y'),dim(620),dim(15, 'y'),dim(40),full_bol())
    
def setup_2():
    global first_page, second_page, Main_Page, first_drop_menu, second_drop_menu, team_menu, time_menu, schedule, input, team
    #Delete firstpage memory
    Main_Page = MainPage.MainPage()
    first_page = False
    Start_Button.Del()
    Exit_Button.Del()
    Start_Page.Del()
    #Set up defaults for MainPage
    second_drop_menu=True
    first_drop_menu=True
    team_menu=["Add/Remove Teams"]
    time_menu=["Playing Times","Weekly Schedule","Month Schedule"]
    Match_menu=["Match Options","Preview"]
    second_page = True
    
    schedule=False
    input=False
    team =False
    
    ScheduleBar.Setup()
    Input.inputs.append(Input.input(0,dim(280),dim(200,'y'),dim(25,'y'),dim(150),dim(20, 'y')))
    
def draw():
    #Updates
    if first_page == True:
        update1(mouseX,mouseY)
    else:
        update2(mouseX,mouseY)
        
def update1(x, y):
    global over_start_button, over_exit_button, over_full, Start_Button, Exit_Button
    #Clickables and button inits
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
    text("Welcome to Overload, the organizational\nprogram you wish you'd always had."+
         "\nWe're there for whatever you need to \norganize. Easy, quick, and ready to go,"+
         "\nOverload is good for daily and monthly \nscheduling, tournaments and games,"+
         "\nas well as other more personal events. \nWith an array of useful and hand-crafted"+
         "\nsettings, we have what you need.",dim(55), dim(300, 'y'))

def update2(x,y):
    global over_test_button,over_test2_button,side_bar,clickable_list,Y
    #Refresh page and variables
    Main_Page.update()
    clickable_list=[]
    side_bar=[]
    over_test_button = over_clickable(0, dim(40, 'y'), dim(150), dim(30, 'y'))
    side_bar.append(Button.Button(0, dim(40, 'y'), dim(150), dim(30, 'y'),0,"Test",True,first_drop_menu))
    Y=30
    
    if first_drop_menu==False:
        for opt in team_menu:
            side_bar.append(Button.Button(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'),0,str(opt),False,False,14))
            clickable_list.append(over_clickable(0, dim(40+Y, 'y'), dim(150), dim(30, 'y')))
            Y+=30
    
    over_test2_button = over_clickable(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'))
    side_bar.append(Button.Button(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'),0,"Test2",True,second_drop_menu))
    Y+=30
    if second_drop_menu==False:
        for opt in time_menu:
            side_bar.append(Button.Button(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'),0,str(opt),False,False,14))
            clickable_list.append(over_clickable(0, dim(40+Y, 'y'), dim(150), dim(30, 'y')))
            Y+=30
    for elm in side_bar:
        elm.display(0,0,0,255,0,0,0,0)
    if schedule:
        ScheduleBar.update()
    if input:
        #A lot more work
        #Input.inputs.append(Input.input(0,dim(100),dim(200,'y'),dim(25,'y'),dim(150),dim(20, 'y'))
        Input.update()
def mousePressed():
    global first_page,second_page,first_drop_menu,second_drop_menu,schedule,input
    if second_page:
        i=0
        if schedule:        
            ScheduleBar.mousepressed()
        if input:
            Input.mousepressed()
        
        if first_drop_menu==False:
            if clickable_list[i]==True:
                #teams = not teams
                input = not input
                schedule, team = (False,)*2
            i+=1
        if second_drop_menu==False:
            if clickable_list[i]==True:
                schedule = not schedule
                input, team, weekly = (False,)*3
                '''
                if clickable_list[1]==True:
                    weekly = not weekly
                if clickable_list[2]==True:
                    monthly = not monthly
                '''
        if over_test_button:
            first_drop_menu= not first_drop_menu
        if over_test2_button:
            second_drop_menu= not second_drop_menu
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
