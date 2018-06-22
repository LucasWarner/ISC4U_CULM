# -------------------------------------------------------------------------------

# Name:           PDFCreation.py

# Purpose:        File to create the PDF (Monthly schedule, daily schedule, matchmaking)

# Author:         Warner.Lucas, McKeen.Kaden

#

# Created:        13/04/2018

# ------------------------------------------------------------------------------

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import datetime
import math
import ScheduleBar
import Input
import MatchOrgAndSep
import MonthlySchedule
import CheckBox
#https://www.reportlab.com/docs/reportlab-userguide.pdf

#Draw the monthly schedule
def drawSchedule(c, month_days, this_month, d, x_offset, y_offset, events, repeating_events, s, days_of_week, wid):
    
    #Draw title
    c.setFont('Helvetica', int(s/3))
    c.drawString(wid - int(wid/2), y_offset+510, "Monthly Schedule")
    
    #Setup draw variables
    on_number = 1
    box_y_range = int((month_days[this_month]+d-1)/7 + (1-(((month_days[this_month]+d-1)/7)%1)))
    event_in_box = [0 for i in range(month_days[this_month])]

    #Draw the boxes
    for box_y in range(box_y_range):
        for box_x in range(7):
            if box_y == 0:
                c.setFont('Helvetica', int(s/6))
                c.drawString(box_x*s + x_offset + s/15, y_offset + box_y_range*s + s/10, text=days_of_week[box_x])
            
            c.setFont('Helvetica', int(s/8))
            c.line(box_x*s + x_offset, box_y*s + y_offset, (box_x+1)*s + x_offset, box_y*s + y_offset)
            c.line(box_x*s + x_offset, box_y*s + y_offset, box_x*s + x_offset, (box_y+1)*s + y_offset)
            if 7*box_y + (box_x+1) > d and on_number <= month_days[this_month]:
                #Print day number
                c.drawString(float(box_x*s) + float(s)*1/15 + x_offset, float((box_y_range-box_y-1)*s) + float(s)*8.5/10 + y_offset, text=str(on_number))
                
                #Draw events
                for event in events:
                    if event[0] <= month_days[this_month]:
                        if on_number == event[0] and event_in_box[on_number-1] < 4:
                            if len(event[1]) < 15:
                                c.drawString(float(box_x*s) + float(s)*1/15 + x_offset, float((box_y_range-box_y)*s) - float(s)*9.3/10 + float(s)*2/10*event_in_box[on_number-1] + y_offset, event[1][:15])
                            else:
                                c.drawString(float(box_x*s) + float(s)*1/15 + x_offset, float((box_y_range-box_y)*s) - float(s)*9.3/10 + float(s)*2/10*event_in_box[on_number-1] + y_offset, event[1][:13]+"...")
                        
                            event_in_box[on_number-1] += 1
                
                #Draw repeating events
                for repeat_e in repeating_events:
                    if ((on_number-d) % 7) == repeat_e[0] and event_in_box[on_number-1] < 4:
                        if len(repeat_e[1]) < 15:
                            c.drawString(float(box_x*s) + float(s)*1/15 + x_offset, float((box_y_range-box_y)*s) - float(s)*9.3/10 + float(s)*2/10*event_in_box[on_number-1] + y_offset, repeat_e[1][:15])
                        else:
                            c.drawString(float(box_x*s) + float(s)*1/15 + x_offset, float((box_y_range-box_y)*s) - float(s)*9.3/10 + float(s)*2/10*event_in_box[on_number-1] + y_offset, repeat_e[1][:13]+"...")
                        
                        event_in_box[on_number-1] += 1
                
                #Increase day number
                on_number += 1

    c.line(7*s + x_offset, 0 + y_offset, 7*s + x_offset, box_y_range*s + y_offset)
    c.line(0 + x_offset, box_y_range*s + y_offset, 7*s + x_offset, box_y_range*s + y_offset)

#Set up the monthly schedule for the draw function
def monthly_schedule(c):
    
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    
    this_month = 0
    month_days = [31,29,31,30,31,30,31,31,30,31,30,31]
    
    s = 80
    rows = 5
    collumns = 7
    
    this_month = 0
    month_days = [31,29,31,30,31,30,31,31,30,31,30,31]
    first_day_of_month = [1,4,4,0,2,5,0,3,6,1,4,6]
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    #Pull events from MonthlySchedule, where the user has created their events
    events = MonthlySchedule.events
    repeating_events = MonthlySchedule.repeating_events
    d = MonthlySchedule.d
    
    x_offset = 25
    y_offset = 200
    
    #Draw the schedule
    drawSchedule(c, month_days, this_month, d, x_offset, y_offset, events, repeating_events, s, days_of_week, 306)

#Turn a raw_time value in minutes into a 'hour:minute' string to display to the user
def printTime(raw_time):   
    minutes = (raw_time + ScheduleBar.day_schedule_bar.start_time) - ((raw_time + ScheduleBar.day_schedule_bar.start_time) // 60)*60
    hours = ((raw_time + ScheduleBar.day_schedule_bar.start_time) // 60)
    
    if hours != hours % 13:
        hours = (hours % 13) + 1
    
    if len(str(minutes)) == 2:
        proper_time = "{0}:{1}".format(hours, minutes)
    else:
        proper_time = "{0}:{1}0".format(hours, minutes)
    return proper_time

#Draw the daily schedule
def drawDailySchedule(c, sections, font_size, wid, y_offset):
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    
    #Draw title
    c.setFont('Helvetica', font_size*1.5)
    c.drawString(wid - int(wid/2), y_offset+30, "Daily Schedule")
    c.setFont('Helvetica', font_size)
    
    #Determine where to draw, based on surrounding features that need to be drawn
    if len(sections) <= 6:
        for t in range(len(sections)):
            c.drawCentredString (wid, -t*20 + y_offset, sections[t])
    else:
        for t in range(len(sections)):
            if t <= int((len(sections)-1)/2):
                c.drawCentredString(wid - int(wid/3), -t*20 + y_offset, sections[t])
            else:
                if len(sections) % 2 == 0:
                    c.drawCentredString(wid + int(wid/3), -(t-int(len(sections)/2))*20 + y_offset, sections[t])
                else:
                    c.drawCentredString(wid + int(wid/3), -((t-1)-int(len(sections)/2))*20 + y_offset, sections[t])

#Set up the daily schedule for the draw function
def daily_schedule(c, other_schedule_shown):
    
    #Get the times from the daily schedule
    times = []
    for node in ScheduleBar.day_schedule_bar.nodes:
        times.append(node.time)
    times.sort()
    
    #Get the sections from the daily schedule
    section_type = ScheduleBar.day_schedule_bar.types
    
    #Get the user-inputted section names from the daily schedule
    section_type_user = []
    for each_input in Input.inputs:
        if each_input.id >= 30 and each_input.id < 200:
            section_type_user.append(each_input.txt)
    
    #Create the strings to be used to show times and sections
    sections = []
    for activities in range(len(times)-1):
        print_text = ''
        proper_time_1 = printTime(int(times[activities]))
        proper_time_2 = printTime(int(times[activities+1]))
        activity_type = section_type[activities]
        
        if section_type_user[activities] == "":
            sections.append("{0} : {1} - {2}".format(proper_time_1,proper_time_2,activity_type))
        else:
            sections.append("{0} : {1} - {2}".format(proper_time_1,proper_time_2,section_type_user[activities]))
    
    font_size = 15
    wid = 306
    
    #Determine where to draw, based on surrounding features that need to be drawn
    if len(sections) <= 12 and other_schedule_shown == True:
        y_offset = 125
        drawDailySchedule(c, sections, font_size, wid, y_offset)
        return [False, None]
    else:
        if other_schedule_shown == True:
            c.showPage()
        y_offset = 675
        drawDailySchedule(c, sections, font_size, wid, y_offset)
        return [True, len(sections)]

#Draw the matches
def drawMatches(c, teams, font_size, wid, y_offset):
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    c.setFont('Helvetica', font_size*1.5)
    c.drawString(wid - int(wid/2), y_offset+30, "Matches")
    c.setFont('Helvetica', font_size)
    
    #Determine where to draw, based on surrounding features that need to be drawn
    if len(teams) <= 10:
        for t in range(len(teams)):
            c.drawCentredString(wid, -t*20 + y_offset, teams[t])
    else:
        for t in range(len(teams)):
            if t <= int((len(teams)-1)/2):
                c.drawCentredString(wid - int(wid/2.4), -t*20 + y_offset, teams[t])
            else:
                if len(teams) % 2 == 0:
                    c.drawCentredString(wid + int(wid/2.4), -(t-int(len(teams)/2))*20 + y_offset, teams[t])
                else:
                    c.drawCentredString(wid + int(wid/2.4), -((t-1)-int(len(teams)/2))*20 + y_offset, teams[t])

#Set up the matches for the draw function
def matches(c, daily_schedule_on_new_page, monthly_schedule_on):
    font_size = 15
    wid = 306
    
    #Get the match information from the Match Options page
    matches = []
    teams = []
    for each_input in Input.inputs:
        if each_input.id < 30:
             teams.append(each_input.txt)
        if each_input.id == 300:
            games_each = each_input.txt
        if each_input.id == 301:
            play_other_max = each_input.txt
    
    if games_each.isnumeric() == False:
        games_each = 3
    if play_other_max.isnumeric() == False:
        play_other_max = 1
    
    #Determine whether to use numbers or titles (user inputted) for team names
    #Based on whether all name textboxes are empty
    if teams.count('') == len(teams):
        team_number_input = None
        for each_input in Input.inputs:
            if each_input.id == 2000:
                team_number_input = each_input
                break
        
        #Determine team names
        #Numerical names whose lenth is the user-inputted number
        if team_number_input.txt.isdigit() and team_number_input.txt != '':
            if int(team_number_input.txt) < 100:
                matches = MatchOrgAndSep.MatchMake(['Team '+str(i+1) for i in range(int(team_number_input.txt))], int(games_each), int(play_other_max))
        
        #Numerical names based on number of teams added
        else:
             matches = MatchOrgAndSep.MatchMake(['Team '+str(i+1) for i in range(len(teams))], int(games_each), int(play_other_max))
    #User inputted names
    else:
        matches = MatchOrgAndSep.MatchMake(teams, int(games_each), int(play_other_max))
    
    #Determine where to draw, based on surrounding features that need to be drawn
    if daily_schedule_on_new_page[0] == True:
        if daily_schedule_on_new_page[1] + len(matches) < 65:
            y_offset = 600 - daily_schedule_on_new_page[1]*10
            drawMatches(c, matches, font_size, wid, y_offset)
        else:
            c.showPage()
            y_offset = 700
            drawMatches(c, matches, font_size, wid, y_offset)
    else:
        if daily_schedule_on_new_page[1] != None or monthly_schedule_on:
            c.showPage()
            y_offset = 675
            drawMatches(c, matches, font_size, wid, y_offset)
        else:
            y_offset = 675
            drawMatches(c, matches, font_size, wid, y_offset)
    
def createPDF():
    width, height = letter
    
    pdfName = "SampleMatchSheet.pdf"
    
    #Create canvas
    c = canvas.Canvas(pdfName, pagesize=letter)
    
    #Draw title
    c.setFont('Helvetica', 30)
    for title_input in Input.inputs:
        if title_input.id == 302:
            PDF_title = title_input.txt
    c.drawString(50, 740, PDF_title)
    
    #Get the settings for which features will be included in the PDF
    monthly_schedule_on = CheckBox.checkboxes[3].clicked
    daily_schedule_on = CheckBox.checkboxes[2].clicked
    matches_on = CheckBox.checkboxes[1].clicked
    
    #Setup and draw the features
    if monthly_schedule_on:
        monthly_schedule(c)
    if daily_schedule_on: 
        daily_schedule_on_new_page = daily_schedule(c, monthly_schedule_on)
    else:
        daily_schedule_on_new_page = [None, None]
    if matches_on:
        matches(c, daily_schedule_on_new_page, monthly_schedule_on)
    
    #Save, unless the PDF is already open
    try:
        c.save()
    except IOError:
        print("\nPlease close the PDF file before generating anew")
