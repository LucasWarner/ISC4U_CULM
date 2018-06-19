
# -------------------------------------------------------------------------------

# Name:           Main.py

# Purpose:        Main file for final project

# Author:         Warner.Lucas, McKeen.Kaden

#

# Created:        13/04/2018

# ------------------------------------------------------------------------------
import MainPage
import StartPage
import Button
import ScheduleBar
import Input
import PDFCreation
import MonthlySchedule
import CheckBox

#PDFCreation.createPDF()

def settings():
    #set fullscreen or (800,600)
    if full_bol() == "True":
        fullScreen()
    else:
        size(800,600)
        
def setup():
    global Start_Page, first_page
    
    textFont(createFont("Helvetica", dim(18,'y')))
    
    #Set up opening page
    first_page = True
    Start_Page = StartPage.StartPage(dim(500),dim(40, 'y'),dim(620),dim(15, 'y'),dim(40),full_bol())
    
def setup_2():
    global over_plus_button, over_minus_button, first_page, Main_Page, first_drop_menu, second_drop_menu, third_drop_menu, team_menu, time_menu, match_menu, daily, matches, monthly, team, vertical_Scrollbar, event_info, publish, team_num, node_num, locked
    
    Main_Page = MainPage.MainPage()
    first_page = False
    
    #Delete firstpage memory
    Start_Button.Del()
    Exit_Button.Del()
    Start_Page.Del()
    
    #Set up defaults for MainPage
    third_drop_menu = True
    second_drop_menu = True
    first_drop_menu = True
    
    team_menu = ["Teams & Matches","Match Options"]
    time_menu = ["Daily Schedule","Monthly Schedule"]
    match_menu = ["Event Information","Publish"]
    
    vertical_Scrollbar = Scrollbar(dim(750), dim(25, 'y'), 16, height-65, 2)
    locked = False
    team_num = 3
    team = False
    team_setup()
    
    matches = False
    matches_setup()
    
    publish = False
    publish_setup()
    
    event_info = False
    event_setup()

    monthly = False
    monthly_setup()
    
    daily=False
    node_num = 30
    ScheduleBar.Setup()
    daily_setup()
    over_plus_button=False
    over_minus_button=False
    
def draw():
    #Updates
    if first_page == True:
        update_1()
    else:
        update_2()
        
def update_1():
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

def update_2():
    global over_teams_button,over_scheduling_button,over_matchmaking_button,side_bar,clickable_list,Y,add_node, over_plus_button, over_minus_button
    
    #Refresh page and variables
    Main_Page.update()
    clickable_list=[]
    side_bar=[]
    
    over_teams_button = over_clickable(0, dim(40, 'y'), dim(150), dim(30, 'y'))
    side_bar.append(Button.Button(0, dim(40, 'y'), dim(150), dim(30, 'y'),0,"Matchmaking",True,first_drop_menu))
    Y=30
    if first_drop_menu==False:
        for opt in team_menu:
            side_bar.append(Button.Button(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'),0,str(opt),False,False,dim(14,'y')))
            clickable_list.append(over_clickable(0, dim(40+Y, 'y'), dim(150), dim(30, 'y')))
            Y+=30
            
    over_scheduling_button = over_clickable(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'))
    side_bar.append(Button.Button(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'),0,"Schedules",True,second_drop_menu))
    Y+=30
    if second_drop_menu==False:
        for opt in time_menu:
            side_bar.append(Button.Button(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'),0,str(opt),False,False,dim(14,'y')))
            clickable_list.append(over_clickable(0, dim(40+Y, 'y'), dim(150), dim(30, 'y')))
            Y+=30
            
    over_matchmaking_button = over_clickable(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'))
    side_bar.append(Button.Button(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'),0,"Info and Publish",True,third_drop_menu))
    Y+=30
    if third_drop_menu==False:
        for opt in match_menu:
            side_bar.append(Button.Button(0, dim(40+Y, 'y'), dim(150), dim(30, 'y'),0,str(opt),False,False,dim(14,'y')))
            clickable_list.append(over_clickable(0, dim(40+Y, 'y'), dim(150), dim(30, 'y')))
            Y+=30
            
    for item in side_bar:
        item.display(0,0,0,255,0,0,0,0)
        
    if daily:
        ScheduleBar.update()
        Schedule_Update()
        Input.update('daily')
        
    if team:
        Input.update('teams')
        team_update()
        
    if event_info:
        #event title
        #brief description of event
        #two text boxes
        #possibily add more
        Input.update('event')
        event_update()
        
    if matches:
        #numberOfGamesPerTeam
        #playAgainstOtherTeamMaxTimes
        #numberOfTeamsTotal
        #two text boxes
        Input.update('matches')
        matches_update()
        
    if publish:
        #button to save pdf(to desktop?)
        #check boxes for what to include
        publish_update()
        
    if monthly:
        #repeatingEvent
        #events
        #checkbox option
        #event name and date
        #[date,name]
        #two textboxes
        Input.update('monthly')
        monthly_update()
        MonthlySchedule.display()
        
def matches_setup():
    CheckBox.checkboxes.append(CheckBox.Checkbox(1,dim(400),dim(100,'y')))
    for j in range(2):
            Input.inputs.append(Input.input(j+300,dim(350),dim(80+(30*j),'y'),dim(25,'y'),dim(150),dim(18, 'y')))
    
def event_setup():
    for j in range(2):
            Input.inputs.append(Input.input(j+301,dim(350),dim(80+(30*j),'y'),dim(25,'y'),dim(150),dim(18, 'y')))
        
def monthly_setup():
    for j in range(2):
            Input.inputs.append(Input.input(j+303,dim(350),dim(80+(30*j),'y'),dim(25,'y'),dim(150),dim(18, 'y')))
    #checkbox id stuff
    
def publish_setup():
    #checkbox id stuff
    pass
    
def team_setup(s=''):
    if s=='a':
        Input.inputs.append(Input.input(team_num-1,dim(350),dim(80+(30*(team_num-1))-(vertical_Scrollbar.sPos-vertical_Scrollbar.yPos),'y'),dim(25,'y'),dim(150),dim(18, 'y')))
    elif s=='p':
        Input.inputs.pop()
        
    else:
        for j in range(team_num):
            Input.inputs.append(Input.input(j,dim(350),dim(80+(30*j)-(vertical_Scrollbar.sPos-vertical_Scrollbar.yPos),'y'),dim(25,'y'),dim(150),dim(18, 'y')))
        Input.inputs.append(Input.input(2000,dim(550),dim(80-(vertical_Scrollbar.sPos-vertical_Scrollbar.yPos),'y'),dim(25,'y'),dim(50),dim(18, 'y')))
            
def daily_setup(s=''):
    if s=='a':
        Input.inputs.append(Input.input(node_num,dim(350),dim(220+(30*(node_num-29)),'y'),dim(25,'y'),dim(150),dim(18, 'y')))
    elif s=='p':
        Input.inputs.pop()
        
    else:
        for j in range(len(ScheduleBar.day_schedule_bar.nodes)-1):
            Input.inputs.append(Input.input(j+30,dim(350),dim(220+(30*j),'y'),dim(25,'y'),dim(150),dim(18, 'y')))
         
def matches_update():
    for boxes in CheckBox.checkboxes:
        if boxes.id==1:
            boxes.render()
            print(boxes.clicked)
    
def event_update():
    pass
        
def monthly_update():
    global submit_event, submit_event_over
    submit_event_over = over_clickable(dim(510), dim(95, 'y'), dim(140), dim(30, 'y'))
    submit_event = Button.Button(dim(475), dim(95, 'y'), dim(180), dim(30, 'y'),dim(400),"Submit Event")
    submit_event.display(0,0,0,255,0,0,0,0)
    
def publish_update():
    pass
    
def team_update():
    global team_num,over_add_button,over_remove_button,ScrollY,locked
    
    fill(255)
    text("Teams & Matches",dim(380),dim(50,'y') )
    
    if team_num==3:
        text("If you would not like to display the team names in the \npdf just enter in the number of teams you would like in \nthe top right box",dim(250),dim(400,'y'))
        
    for each_input in Input.inputs:
        if each_input.id<30:
            each_input.y = dim(80+(30*each_input.id)-(vertical_Scrollbar.sPos-vertical_Scrollbar.yPos),'y')
        elif each_input.id==2000:
            each_input.y=dim(80-(vertical_Scrollbar.sPos-vertical_Scrollbar.yPos),'y')
            
    for j in range(team_num):
        if dim(80 + (30*j)-(vertical_Scrollbar.sPos-vertical_Scrollbar.yPos),'y')>70 and dim(80 + (30*j)-(vertical_Scrollbar.sPos-vertical_Scrollbar.yPos),'y')<750:
            text(str(j+1) + ". Name:",dim(240),dim(100 + (30*j)-(vertical_Scrollbar.sPos-vertical_Scrollbar.yPos),'y'))
            
    if team_num<30:
        over_add_button = over_clickable(dim(240), dim(100 + (30*(j+1))-(vertical_Scrollbar.sPos-vertical_Scrollbar.yPos), 'y'), dim(140), dim(30, 'y'))
        add_button = Button.Button(dim(240), dim(100 + (30*(j+1))-(vertical_Scrollbar.sPos-vertical_Scrollbar.yPos), 'y'), dim(140), dim(30, 'y'),dim(400),"Add Team")
        add_button.display(0,0,0,255,0,0,0,0)
    else:
        over_add_button = False
        
    if team_num>1:
        over_remove_button = over_clickable(dim(410), dim(100 + (30*(j+1))-(vertical_Scrollbar.sPos-vertical_Scrollbar.yPos), 'y'), dim(150), dim(30, 'y'))
        remove_button = Button.Button(dim(380), dim(100 + (30*(j+1))-(vertical_Scrollbar.sPos-vertical_Scrollbar.yPos), 'y'), dim(180), dim(30, 'y'),dim(400),"Remove Team")
        remove_button.display(0,0,0,255,0,0,0,0)
    else:
        over_remove_button = False
        
    scrollY = getPos()
    display()
    
    #mouse over for scrollbar
    if overEvent(): 
      over = True
    else:
      over = False
    # lock the scroll bar square to mouse
    if mousePressed and over: 
      locked = True
    # cancel lock on mouse button released
    if mousePressed == False:
      locked = False;
    # move scroll bar square with mouse
    if locked:
      vertical_Scrollbar.newsPos = constrain(mouseY-vertical_Scrollbar.sWidth/2, vertical_Scrollbar.sPosMin, vertical_Scrollbar.sPosMax) 
    # move scroll bar square with mouse smoothly
    if abs(vertical_Scrollbar.newsPos - vertical_Scrollbar.sPos) > 1: 
      vertical_Scrollbar.sPos = vertical_Scrollbar.sPos + (vertical_Scrollbar.newsPos-vertical_Scrollbar.sPos)/vertical_Scrollbar.loose
      
def Schedule_Update():
    global add_node,delete_node, range_10, range_15, range_30, over_plus_button, over_minus_button
    
    over_plus_button = over_clickable(520, dim(30, 'y'), dim(35), dim(40, 'y'))
    plus_button = Button.Button(dim(490), dim(50, 'y'), dim(150), dim(30, 'y'),dim(400),"+",False,False,40)
    plus_button.display(0,0,0,255,0,0,0,0)
    
    over_minus_button = over_clickable(425, dim(30, 'y'), dim(35), dim(40, 'y'))
    minus_button = Button.Button(dim(400), dim(50, 'y'), dim(150), dim(30, 'y'),dim(400),"-",False,False,55)
    minus_button.display(0,0,0,255,0,0,0,0)
    
    add_node = over_clickable(dim(525), dim(160, 'y'), dim(160), dim(30, 'y'))
    add_node_button = Button.Button(dim(490), dim(160, 'y'), dim(180), dim(30, 'y'),dim(400),"Add Time Node")
    add_node_button.display(0,0,0,255,0,0,0,0)
    
    delete_node = over_clickable(dim(280), dim(160, 'y'), dim(190), dim(30, 'y'))
    delete_node_button = Button.Button(dim(250), dim(160, 'y'), dim(180), dim(30, 'y'),dim(400),"Remove Time Node")
    delete_node_button.display(0,0,0,255,0,0,0,0)
    
    range_10 = over_clickable(dim(200), dim(190, 'y'), dim(160), dim(30, 'y'))
    range_10_button = Button.Button(dim(200), dim(190, 'y'), dim(180), dim(30, 'y'),dim(400),"10 Minute Range")
    range_10_button.display(0,0,0,255,0,0,0,0)
    
    range_15 = over_clickable(dim(380), dim(190, 'y'), dim(160), dim(30, 'y'))
    range_15_button = Button.Button(dim(380), dim(190, 'y'), dim(180), dim(30, 'y'),dim(400),"15 Minute Range")
    range_15_button.display(0,0,0,255,0,0,0,0)
    
    range_30 = over_clickable(dim(560), dim(190, 'y'), dim(160), dim(30, 'y'))
    range_30_button = Button.Button(dim(560), dim(190, 'y'), dim(180), dim(30, 'y'),dim(400),"30 Minute Range")
    range_30_button.display(0,0,0,255,0,0,0,0)
    
    for j in range(len(ScheduleBar.day_schedule_bar.nodes)-1):
        text(str(j+1) + ". Name:",dim(240),dim(240 + (30*j),'y'))
        
def mousePressed():
    global first_page,first_drop_menu,second_drop_menu, third_drop_menu, daily, team, monthly, publish, matches, event_info, add_node,delete_node,team_num,node_num, over_plus_button, over_minus_button
    
    if first_page == False:
        i=0
        
        if daily:
            if add_node:
                ScheduleBar.addNode()
                node_num+=1
                daily_setup('a')
            if delete_node:
                ScheduleBar.removeNode()
                node_num-=1
                daily_setup('p')
            if range_10:
                ScheduleBar.rangeOption(1)
            if range_15:
                ScheduleBar.rangeOption(2)
            if range_30:
                ScheduleBar.rangeOption(3)
            if over_plus_button:
                ScheduleBar.changeEndNodeTime(1)
                PDFCreation.createPDF()
            if over_minus_button:
                ScheduleBar.changeEndNodeTime(-1)
            
            ScheduleBar.mousepressed()
            Input.mousepressed()
            
        if team:
            Input.mousepressed()
            if over_add_button:
                team_num+=1
                team_setup('a')
            if over_remove_button:
                if team_num>3:
                    team_num-=1
                    team_setup('p')
                    
        if publish:
            Input.mousepressed()
            
        if event_info:
            Input.mousepressed()
            
        if matches:
            Input.mousepressed()
            CheckBox.mousepressed(1)
            
        if monthly:
            Input.mousepressed()
            if submit_event_over:
                for checkbox in checkboxes:
                    if checkbox.id == 0:
                        for each_input in Input.inputs:
                            if each_input.id == 303:
                                event_name = each_input.txt
                            elif each_input.id == 304:
                                event_date = each_input.txt
                        
                        if event_name != "" and event_date != "" and event_date.isnumeric():
                            MonthlySchedule.addEvent(checkbox.clicked, event_name, event_date)
            
            
        if first_drop_menu==False:
            if clickable_list[i]:
                team = not team
                daily, monthly, publish, matches, event_info = (False,)*5
            if clickable_list[i+1]:
                matches = not matches
                daily, team, monthly, publish, event_info = (False,)*5
            i+=2
            
        if second_drop_menu==False:
            if clickable_list[i]:
                daily = not daily
                team, event_info, publish, monthly, matches = (False,)*5
            if clickable_list[i+1]:
                monthly = not monthly
                team, event_info, publish, daily, matches = (False,)*5
            i+=2
            
        if third_drop_menu==False:
            if clickable_list[i]:
                event_info = not event_info
                team, daily, publish, monthly, matches = (False,)*5
            if clickable_list[i+1]:
                publish = not publish
                team, daily, event_info, monthly, matches = (False,)*5
                
                
        if over_teams_button:
            first_drop_menu= not first_drop_menu
            
        if over_scheduling_button:
            second_drop_menu= not second_drop_menu
            
        if over_matchmaking_button:
           third_drop_menu= not third_drop_menu
           
           
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
    if daily:
        ScheduleBar.mousereleased()
        
def keyPressed():
    if first_page == False:
        Input.keypressed()
          
def over_clickable(x, y, w, h):
    #All dimensions remain in constant ratios of window size
    return x <= mouseX <= x + w and y <= mouseY <= y + h

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

class Scrollbar(object): # scroll bar class
    def __init__ (self,xp, yp, sw, sh, l):
        global sWidth, sHeight, xPos, yPos, sPos, newsPos, sPosMin, sPosMax, loose, ratio
        self.sWidth = sw
        self.sHeight = sh
        self.wifthToHeight = sh - sw
        self.ratio = sh / self.wifthToHeight
        self.xPos = xp-self.sWidth/2
        self.yPos = yp
        self.sPos = yp
        self.newsPos = self.sPos
        self.sPosMin = self.yPos-1
        self.sPosMax = height-39-self.sHeight/6
        self.loose = l
        
def overEvent(): 
    #check for mouse overs for scrollbar square
    if mouseX > vertical_Scrollbar.xPos and mouseX < vertical_Scrollbar.xPos+vertical_Scrollbar.sWidth and mouseY > vertical_Scrollbar.yPos and mouseY < vertical_Scrollbar.yPos+vertical_Scrollbar.sHeight:
      return True
    else:
      return False
  
def constrain(val, minv, maxv): # set scroll bar square max and min yPosition
    return min(max(val, minv), maxv)

def getPos():
    #Convert sPos to be values between
    #0 and the total width of the scrollbar
    return vertical_Scrollbar.sPos * vertical_Scrollbar.ratio

def display():
    # scrollbar
    noStroke()
    fill(204)
    rect(vertical_Scrollbar.xPos, vertical_Scrollbar.yPos, vertical_Scrollbar.sWidth, vertical_Scrollbar.sHeight)
    # scrollbar square colour
    if overEvent() or locked:
        fill(100, 100, 100)
    else:
        fill(100, 120, 140)
    # scrollbar square
    rect(vertical_Scrollbar.xPos, vertical_Scrollbar.sPos, vertical_Scrollbar.sWidth, vertical_Scrollbar.sHeight/6)
