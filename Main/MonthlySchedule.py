import datetime

s = 78
rows = 5
collumns = 7

topPadding = 50

thisMonth = 2
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
d = (floor(2.6 * M - 5.39) + floor((Y - (100 * (floor(Y / 100)))) / 4) + floor((floor(Y / 100)) / 4) + D + (Y - (100 * (floor(Y / 100)))) - (2 * (floor(Y / 100)))) - (7 * floor((floor(2.6 * M - 5.39) + floor((Y - (100 * (floor(Y / 100)))) / 4) + floor((floor(Y / 100)) / 4) + D + (Y - (100 * (floor(Y / 100)))) - (2 * (floor(Y / 100)))) / 7))


def display():
    global x_offset, y_offset, d, events, repeating_events
    x_offset = 202
    y_offset = 200
    
    on_number = 1
    box_y_range = (monthDays[thisMonth]+d-1)/7 + (1-(((monthDays[thisMonth]+d-1)/7)%1))
    event_in_box = [0 for i in range(monthDays[thisMonth])]
    fill(255)
    rect(x_offset,y_offset,7*s,box_y_range*s)
    for box_y in range(box_y_range):
        for box_x in range(7):
            if box_y == 0:
                fill(0)
                textSize(s/6)
                text(daysOfTheWeek[box_x], box_x*s + x_offset + s/15, y_offset - s/10)
                line(box_x*s + x_offset, box_y*s + y_offset, (box_x+1)*s + x_offset, box_y*s + y_offset)
                line(box_x*s + x_offset, box_y*s + y_offset, box_x*s + x_offset, (box_y+1)*s + y_offset)
            if 7*box_y + (box_x+1) > d and on_numb er <= monthDays[thisMonth]:
                #Print day number
                fill(0)
                textSize(s/6)
                text(str(on_number), float(box_x*s) + float(s)*1/15 + x_offset, float((box_y+1)*s) - float(s)*8/10 + y_offset)
                
                textSize(s/8)
                #Events
                for event in events:
                    if event[0] <= monthDays[thisMonth]:
                        if on_number == event[0] and event_in_box[on_number-1] < 4:
                            if len(event[1]) < 15:
                                text(event[1][:15], float(box_x*s) + float(s)*1/15 + x_offset, float((box_y+1)*s) - float(s)*6.5/10 + float(s)*2/10*event_in_box[on_number-1] + y_offset)
                            else:
                                text(event[1][:13]+"...", float(box_x*s) + float(s)*1/15 + x_offset, float((box_y+1)*s) - float(s)*6.5/10 + float(s)*2/10*event_in_box[on_number-1] + y_offset)
                        
                            event_in_box[on_number-1] += 1
                
                #Repeating events
                for repeat_e in repeatingEvent:
                    if ((on_number-d) % 7) == repeat_e[0] and event_in_box[on_number-1] < 4:
                        if len(repeat_e[1]) < 15:
                            text(repeat_e[1][:15], float(box_x*s) + float(s)*1/15 + x_offset, float((box_y+1)*s) - float(s)*6.5/10 + float(s)*2/10*event_in_box[on_number-1] + y_offset)
                        else:
                            text(repeat_e[1][:13]+"...", float(box_x*s) + float(s)*1/15 + x_offset, float((box_y+1)*s) - float(s)*6.5/10 + float(s)*2/10*event_in_box[on_number-1] + y_offset)
                        
                        event_in_box[on_number-1] += 1
                
                #Increase day number
                on_number += 1
    
    line(7*s + x_offset, 0 + y_offset, 7*s + x_offset, box_y_range*s + y_offset)
    line(0 + x_offset, box_y_range*s + y_offset, 7*s + x_offset, box_y_range*s + y_offset)
