from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import datetime
import math
#https://www.reportlab.com/docs/reportlab-userguide.pdf

def drawSchedule(c, monthDays, thisMonth, d, x_offset, y_offset, events, repeatingEvent, s, daysOfTheWeek):
    
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
    
    x_offset = 30
    y_offset = 30
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
    
    print(d)
    
    x_offset = 25#Main.width/30
    y_offset = 25#Main.width/30
    
    drawSchedule(c, monthDays, thisMonth, d, x_offset, y_offset, events, repeatingEvent, s, daysOfTheWeek)


def drawMatches(c, teams, font_size, wid, y_offset):
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    c.setFont('Helvetica', font_size)
    
    if len(teams) <= 10:
        collumn_range = 1
    else:
        collumn_range = 2
    
    for collumn in range(collumn_range):
        for t in range(len(teams)):
            if t // 10 == collumn:
                c.drawCentredString (int(wid/(collumn+1)), -(t%10)*20 + y_offset, teams[t])

def matches(c, width):
    font_size = 15
    wid = width
    teams = ['Team 1 vs Team 5', 'Team 2 vs Team 4', 'Team 3 vs Team 6', 'Team 4 vs Team 8', 'Team 1 vs Team 5', 'Team 2 vs Team 4', 'Team 3 vs Team 6', 'Team 4 vs Team 8', 'Team 1 vs Team 5', 'Team 2 vs Team 4', 'Team 3 vs Team 6', 'Team 4 vs Team 8', 'Team 1 vs Team 5', 'Team 2 vs Team 4', 'Team 3 vs Team 6', 'Team 4 vs Team 8']
    y_offset = 200
    
    drawMatches(c, teams, font_size, wid, y_offset)
    
def createPDF():
    width, height = letter
    
    pdfName = "SampleMatchSheet.pdf"
    
    c = canvas.Canvas(pdfName, pagesize=letter)
    #monthly_schedule(c)
    matches(c, 306)
    
    try:
        c.save()
    except IOError:
        print("\nPlease close the PDF file before generating anew")
