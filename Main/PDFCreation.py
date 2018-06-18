from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import datetime
import math
import ScheduleBar
import Input
#https://www.reportlab.com/docs/reportlab-userguide.pdf

def drawSchedule(c, monthDays, thisMonth, d, x_offset, y_offset, events, repeatingEvent, s, daysOfTheWeek, wid):
    
    c.setFont('Helvetica', int(s/3))
    c.drawString(wid - int(wid/1.3), y_offset+450, "Monthly Schedule")
    
    on_number = 1
    box_y_range = int((monthDays[thisMonth]+d-1)/7 + (1-(((monthDays[thisMonth]+d-1)/7)%1)))
    event_in_box = [0 for i in range(monthDays[thisMonth])]

    for box_y in range(box_y_range):
        for box_x in range(7):
            if box_y == 0:
                c.setFont('Helvetica', int(s/6))
                c.drawString(box_x*s + x_offset + s/15, y_offset + box_y_range*s + s/10, text=daysOfTheWeek[box_x])
            
            c.setFont('Helvetica', int(s/8))
            c.line(box_x*s + x_offset, box_y*s + y_offset, (box_x+1)*s + x_offset, box_y*s + y_offset)
            c.line(box_x*s + x_offset, box_y*s + y_offset, box_x*s + x_offset, (box_y+1)*s + y_offset)
            if 7*box_y + (box_x+1) > d and on_number <= monthDays[thisMonth]:
                #Print day number
                c.drawString(float(box_x*s) + float(s)*1/15 + x_offset, float((box_y_range-box_y-1)*s) + float(s)*8.5/10 + y_offset, text=str(on_number))
                
                #Events
                for event in events:
                    if event[0] <= monthDays[thisMonth]:
                        if on_number == event[0] and event_in_box[on_number-1] < 4:
                            if len(event[1]) < 15:
                                c.drawString(float(box_x*s) + float(s)*1/15 + x_offset, float((box_y_range-box_y)*s) - float(s)*9.3/10 + float(s)*2/10*event_in_box[on_number-1] + y_offset, event[1][:15])
                            else:
                                c.drawString(float(box_x*s) + float(s)*1/15 + x_offset, float((box_y_range-box_y)*s) - float(s)*9.3/10 + float(s)*2/10*event_in_box[on_number-1] + y_offset, event[1][:13]+"...")
                        
                            event_in_box[on_number-1] += 1
                
                #Repeating events
                for repeat_e in repeatingEvent:
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


def monthly_schedule(c):
    
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    
    thisMonth = 0
    monthDays = [31,29,31,30,31,30,31,31,30,31,30,31]
    
    s = 80
    rows = 5
    collumns = 7
    
    topPadding = 50
    
    thisMonth = 0
    monthDays = [31,29,31,30,31,30,31,31,30,31,30,31]
    dayOnWhichMonthStarts = [1,4,4,0,2,5,0,3,6,1,4,6]
    daysOfTheWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    events = [[23, "Spesisal Day Of FuNnEsS"], [24, "Serious Day Of Seriousness."], [4, "Feast Day"]]
    repeatingEvent = [[0, "Garbage Pickup"],[0, "Bus Duties Broski"],[0, "Lazy Day"], [0, "Suh Dude"]]
    
    #Calculate on which day the month starts
    time = datetime.datetime.now()
    D = 1
    M = thisMonth + 1
    Y = time.year
    if M < 3:
        M = M + 12
        Y = Y - 1
    d = (math.floor(2.6 * M - 5.39) + math.floor((Y - (100 * (math.floor(Y / 100)))) / 4) + math.floor((math.floor(Y / 100)) / 4) + D + (Y - (100 * (math.floor(Y / 100)))) - (2 * (math.floor(Y / 100)))) - (7 * math.floor((math.floor(2.6 * M - 5.39) + math.floor((Y - (100 * (math.floor(Y / 100)))) / 4) + math.floor((math.floor(Y / 100)) / 4) + D + (Y - (100 * (math.floor(Y / 100)))) - (2 * (math.floor(Y / 100)))) / 7))
    
    x_offset = 25
    y_offset = 300
    
    drawSchedule(c, monthDays, thisMonth, d, x_offset, y_offset, events, repeatingEvent, s, daysOfTheWeek, 306)

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

def drawDailySchedule(c, sections, font_size, wid, y_offset):
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    c.setFont('Helvetica', font_size*1.5)
    c.drawString(wid - int(wid/1.3), y_offset+30, "Daily Schedule")
    c.setFont('Helvetica', font_size)
    if len(sections) <= 10:
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

def daily_schedule(c, other_schedule_shown):
    times = []
    for node in ScheduleBar.day_schedule_bar.nodes:
        times.append(node.time)
    times.sort()
    
    section_type = ScheduleBar.day_schedule_bar.types
    
    section_type_user = []
    for each_input in Input.inputs:
        if each_input.id >= 30 and each_input.id < 200:
            section_type_user.append(each_input.txt)
    
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
    
    if len(sections) <= 20 and other_schedule_shown == True:
        y_offset = 225
        drawDailySchedule(c, sections, font_size, wid, y_offset)
        return [False, None]
    else:
        if other_schedule_shown == True:
            c.showPage()
        y_offset = 700
        drawDailySchedule(c, sections, font_size, wid, y_offset)
        return [True, len(sections)]

def drawMatches(c, teams, font_size, wid, y_offset):
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    c.setFont('Helvetica', font_size*1.5)
    c.drawString(wid - int(wid/1.3), y_offset+30, "Matches")
    c.setFont('Helvetica', font_size)
    
    if len(teams) <= 10:
        for t in range(len(teams)):
            c.drawCentredString(wid, -t*20 + y_offset, teams[t])
    else:
        for t in range(len(teams)):
            if t <= int((len(teams)-1)/2):
                c.drawCentredString(wid - int(wid/3), -t*20 + y_offset, teams[t])
            else:
                if len(teams) % 2 == 0:
                    c.drawCentredString(wid + int(wid/3), -(t-int(len(teams)/2))*20 + y_offset, teams[t])
                else:
                    c.drawCentredString(wid + int(wid/3), -((t-1)-int(len(teams)/2))*20 + y_offset, teams[t])

def matches(c, daily_schedule_on_new_page, monthly_schedule_on):
    font_size = 15
    wid = 306
    
    for each_input in Input.inputs:
        if each_input.id < 30:
             teams.append(each_input.txt)
    
    if len(teams) == 0:
        team_number_input = None
        for each_input in Input.inputs:
            if each_input.id == 2000:
                team_number_input = each_input
                break
        
    if team_number_input.txt.isdigit() and team_number_input.txt != '':
        MatchOrgAndSep(int(team_number_input.txt))
    else:
        MatchOrgAndSep(10)
        #teams = ['Team 1 vs Team 5', 'Team 2 vs Team 4', 'Team 3 vs Team 6', 'Team 4 vs Team 8', 'Team 1 vs Team 5', 'Team 2 vs Team 4', 'Team 3 vs Team 6', 'Team 4 vs Team 8', 'Team 1 vs Team 5', 'Team 2 vs Team 4', 'Team 3 vs Team 6']
    
    if daily_schedule_on_new_page[0] == True:
        if daily_schedule_on_new_page[1] + len(teams) < 65:
            y_offset = 600 - daily_schedule_on_new_page[1]*10
            drawMatches(c, teams, font_size, wid, y_offset)
        else:
            c.showPage()
            y_offset = 700
            drawMatches(c, teams, font_size, wid, y_offset)
    else:
        if daily_schedule_on_new_page[1] != None or monthly_schedule_on:
            c.showPage()
            y_offset = 700
            drawMatches(c, teams, font_size, wid, y_offset)
        else:
            y_offset = 700
            drawMatches(c, teams, font_size, wid, y_offset)
    
def createPDF():
    width, height = letter
    
    pdfName = "SampleMatchSheet.pdf"
    
    c = canvas.Canvas(pdfName, pagesize=letter)
    
    monthly_schedule_on = True
    daily_schedule_on = True
    matches_on = True
    
    if monthly_schedule_on:
        monthly_schedule(c)
    if daily_schedule_on: 
        daily_schedule_on_new_page = daily_schedule(c, monthly_schedule_on)
    else:
        daily_schedule_on_new_page = [None, None]
    if matches_on:
        matches(c, daily_schedule_on_new_page, monthly_schedule_on)
            
    
    try:
        c.save()
    except IOError:
        print("\nPlease close the PDF file before generating anew")
        
def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
