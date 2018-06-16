from reportlab.pdfbase.pdfmetrics import stringWidth

"""
Information we need from the outside:
    x/y position of the schedule bar
    start time/total time (end time - start time)
    smallest time interval (ie, 10, 15, 30 minutes - up to 60)
"""
#Should also add option to create intervals automatically



class schedule_bar(object):
    def __init__ (self, pos_x, pos_y, wid, hei, node_y, smallest_time_interval, time_minutes,  text_size, start_time):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.wid = wid
        self.hei = hei
        self.nodes = []
        self.divisions = [0]
        self.smallest_interval = smallest_time_interval
        self.time_total = time_minutes
        self.drag_change = (float(smallest_time_interval)/float(time_minutes))*float(wid)
        self.type_shown = None
        self.time_shown = None
        self.type_shown_id = -1
        self.types = ["Activity", "Activity"]
        self.text_size = text_size
        self.dragged = False
        self.start_time = start_time
        self.leftmost_clicked = False
        self.rightmost_clicked = False
        
    def create_bars(self, id, sort_index):
        if day_schedule_bar.types[id] == "Activity":
            fill(153, 217, 234)
        if day_schedule_bar.types[id] == "Break":
            fill(255, 140, 0)
        rect(day_schedule_bar.nodes[sort_index[id]].pos_x, day_schedule_bar.pos_y, day_schedule_bar.nodes[sort_index[id+1]].pos_x - day_schedule_bar.nodes[sort_index[id]].pos_x, day_schedule_bar.hei)


class node(object):
    def __init__ (self, x_pos, siz, time, colour=(0, 162, 232)):
        self.colour = colour
        self.pos_x = x_pos * day_schedule_bar.wid + day_schedule_bar.pos_x
        self.pos_y = day_schedule_bar.pos_y
        self.s = siz
        self.time = time
    
    def move (self):
        #Check for obstuction of other nodes
        obstructed = False
        sign_type = sign(mouseX - self.pos_x, None)
        for n_other in day_schedule_bar.nodes:
            if self.pos_x != n_other.pos_x:
                if sign(self.pos_x - n_other.pos_x, sign_type) == -sign_type and sign(int(self.pos_x + day_schedule_bar.drag_change*sign_type - n_other.pos_x), sign_type) == sign_type:
                    obstructed = True
        
        if obstructed == False:
            self.pos_x += day_schedule_bar.drag_change * sign_type
            self.time += day_schedule_bar.smallest_interval * sign_type
            day_schedule_bar.dragged = True


class text_display(object):
    def __init__ (self, txt, pos_x, pos_y):
        self.txt = txt
        self.pos_x = pos_x
        self.pos_y = pos_y
    

def Setup():
    global day_schedule_bar, drag_node, last_clicked
    day_schedule_bar = schedule_bar(230, 100, 540, 10, 50, 15, 705, 20, 480)
    day_schedule_bar.nodes.append(node(0, 20, 0))
    day_schedule_bar.nodes.append(node(((float(day_schedule_bar.time_total/2)) - (float(day_schedule_bar.time_total/2) % day_schedule_bar.smallest_interval)) / day_schedule_bar.time_total, 20, int((float(day_schedule_bar.time_total/2)) - (float(day_schedule_bar.time_total/2) % day_schedule_bar.smallest_interval))))
    day_schedule_bar.nodes.append(node(1, 20, day_schedule_bar.time_total))

    drag_node = -1
    last_clicked = -1



def update():
    #rect(45, 190, 410, 50)
    #make Bars
    noStroke()
    sort_index = [i for i in range(len(day_schedule_bar.nodes))]
    nodes_x = [int(i.pos_x) for i in day_schedule_bar.nodes]
    sort_index = [x for _,x in sorted(zip(nodes_x, sort_index))]
    for n in range(len(sort_index)):
        if n < len(sort_index)-1:
            day_schedule_bar.create_bars(n, sort_index)
    
    #Make nodes
    fill(0, 162, 232)
    ellipseMode(CENTER)
    for n in range (len(day_schedule_bar.nodes)):
        fill(day_schedule_bar.nodes[n].colour[0],day_schedule_bar.nodes[n].colour[1],day_schedule_bar.nodes[n].colour[2])
        ellipse(day_schedule_bar.nodes[n].pos_x, day_schedule_bar.nodes[n].pos_y + day_schedule_bar.hei/2, day_schedule_bar.nodes[n].s, day_schedule_bar.nodes[n].s)
    
    #Move nodes
    if drag_node != -1:
        for drag in range(int(abs(mouseX - day_schedule_bar.nodes[drag_node].pos_x) // day_schedule_bar.drag_change)):
            day_schedule_bar.nodes[drag_node].move()
    
    #Get rid of type/time tags if a node is being dragged
    if day_schedule_bar.dragged == True:
        day_schedule_bar.type_shown = None
        day_schedule_bar.time_shown = None
    
    
    #Show type name
    fill(255)
    textSize(day_schedule_bar.text_size)
    if day_schedule_bar.type_shown != None: 
        text(day_schedule_bar.type_shown.txt, day_schedule_bar.type_shown.pos_x, day_schedule_bar.type_shown.pos_y)
    
    #Show node time
    over = False
    if day_schedule_bar.dragged == False:
        for n in range (len(day_schedule_bar.nodes)):
            if over_clickable(day_schedule_bar.nodes[n].pos_x-day_schedule_bar.nodes[n].s/2, day_schedule_bar.nodes[n].pos_y-day_schedule_bar.nodes[n].s/2, day_schedule_bar.nodes[n].s, day_schedule_bar.nodes[n].s):
                over = True
                raw_time = int(day_schedule_bar.nodes[n].time)
                
                minutes = (raw_time + day_schedule_bar.start_time) - ((raw_time + day_schedule_bar.start_time) // 60)*60
                hours = ((raw_time + day_schedule_bar.start_time) // 60)
                
                if hours != hours % 13:
                    hours = (hours % 13) + 1
                
                if len(str(minutes)) == 2:
                    proper_time = "{0}:{1}".format(hours, minutes)
                else:
                    proper_time = "{0}:{1}0".format(hours, minutes)
                
                day_schedule_bar.time_shown = text_display(proper_time, day_schedule_bar.nodes[n].pos_x - (len(proper_time)-1)*6.3, day_schedule_bar.pos_y + day_schedule_bar.hei*3.5)
                text(day_schedule_bar.time_shown.txt, day_schedule_bar.time_shown.pos_x, day_schedule_bar.time_shown.pos_y)
                break
    
    if over == False:
        day_schedule_bar.time_shown = None
    else:
        day_schedule_bar.type_shown = None
    

def mousepressed():
    global drag_node, day_schedule_bar
    
    #Get rid of time if not clicking on that same node again
    if over_clickable(day_schedule_bar.nodes[last_clicked].pos_x - day_schedule_bar.nodes[last_clicked].s/2, day_schedule_bar.nodes[last_clicked].pos_y - day_schedule_bar.nodes[last_clicked].s/2, day_schedule_bar.nodes[last_clicked].s, day_schedule_bar.nodes[last_clicked].s) == False:
        day_schedule_bar.time_shown = None
    
    #Check for node clicked
    for n in range (len(day_schedule_bar.nodes)):
        if day_schedule_bar.nodes[n].pos_x != day_schedule_bar.pos_x and day_schedule_bar.nodes[n].pos_x != day_schedule_bar.pos_x + day_schedule_bar.wid:
            if over_clickable(day_schedule_bar.nodes[n].pos_x - day_schedule_bar.nodes[n].s/2, day_schedule_bar.nodes[n].pos_y - day_schedule_bar.nodes[n].s/2, day_schedule_bar.nodes[n].s, day_schedule_bar.nodes[n].s):
                drag_node = n
                day_schedule_bar.dragged = False
        else:
            if over_clickable(day_schedule_bar.nodes[n].pos_x - day_schedule_bar.nodes[n].s/2, day_schedule_bar.nodes[n].pos_y - day_schedule_bar.nodes[n].s/2, day_schedule_bar.nodes[n].s, day_schedule_bar.nodes[n].s):
                
                #Leftmost node clicked
                if day_schedule_bar.nodes[n].pos_x == day_schedule_bar.pos_x:
                    day_schedule_bar.leftmost_clicked = not day_schedule_bar.leftmost_clicked 
                    if day_schedule_bar.leftmost_clicked == True:
                        day_schedule_bar.nodes[n].colour = (255,255,0)
                    else:
                        day_schedule_bar.nodes[n].colour = (0, 162, 232)
                #Rightmost node clicked
                elif day_schedule_bar.nodes[n].pos_x == day_schedule_bar.pos_x + day_schedule_bar.wid:
                    day_schedule_bar.rightmost_clicked = not day_schedule_bar.rightmost_clicked
                    if day_schedule_bar.rightmost_clicked == True:
                        day_schedule_bar.nodes[n].colour = (255,255,0)
                    else:
                        day_schedule_bar.nodes[n].colour = (0, 162, 232)
    
    #Check if day schedule bar clicked
    if day_schedule_bar.type_shown == None:
        #If it wasn't a node that was pressed on (Because then we wouldn't want the bar to be activated)
        if drag_node == -1:
            if over_clickable(day_schedule_bar.pos_x, day_schedule_bar.pos_y, day_schedule_bar.wid, day_schedule_bar.hei):
                #Find closest left node
                sort_index = [i for i in range(len(day_schedule_bar.nodes))]
                nodes_x = [int(i.pos_x) for i in day_schedule_bar.nodes]
                sort_index = [x for _,x in sorted(zip(nodes_x, sort_index))]
                nodes_x.sort()
                nodes_x_reduced = [i for i in nodes_x if mouseX-i > 0]
                sort_index_reduced = [i for _,i in zip(nodes_x, sort_index) if mouseX-_ > 0]
                if len(sort_index_reduced) > 0:
                    day_schedule_bar.type_shown_id = nodes_x.index(max(nodes_x_reduced))
                    l_close = max(nodes_x_reduced)
                    r_close = day_schedule_bar.nodes[sort_index[nodes_x.index(max(nodes_x_reduced))+1]].pos_x
                    wid = stringWidth(day_schedule_bar.types[day_schedule_bar.type_shown_id],'Helvetica', 20)
                    day_schedule_bar.type_shown = text_display(day_schedule_bar.types[day_schedule_bar.type_shown_id], (l_close + (r_close - l_close)/2) - wid/2, day_schedule_bar.pos_y + day_schedule_bar.hei*3)
                    
    else:
        if over_clickable(day_schedule_bar.type_shown.pos_x, day_schedule_bar.pos_y, len(day_schedule_bar.type_shown.txt)*day_schedule_bar.text_size/1.6, day_schedule_bar.text_size*1.6):
            if day_schedule_bar.types[day_schedule_bar.type_shown_id] == "Activity":
                day_schedule_bar.types[day_schedule_bar.type_shown_id] = "Break"
                #Find closest left node
                sort_index = [i for i in range(len(day_schedule_bar.nodes))]
                nodes_x = [int(i.pos_x) for i in day_schedule_bar.nodes]
                sort_index = [x for _,x in sorted(zip(nodes_x, sort_index))]
                nodes_x.sort()
                nodes_x_reduced = [i for i in nodes_x if mouseX-i > 0]
                sort_index_reduced = [i for _,i in zip(nodes_x, sort_index) if mouseX-_ > 0]
                if len(sort_index_reduced) > 0:
                    day_schedule_bar.type_shown_id = nodes_x.index(max(nodes_x_reduced))
                    l_close = max(nodes_x_reduced)
                    r_close = day_schedule_bar.nodes[sort_index[nodes_x.index(max(nodes_x_reduced))+1]].pos_x
                    wid = stringWidth(day_schedule_bar.types[day_schedule_bar.type_shown_id],'Helvetica', 20)
                    day_schedule_bar.type_shown = text_display(day_schedule_bar.types[day_schedule_bar.type_shown_id], (l_close + (r_close - l_close)/2) - wid/2, day_schedule_bar.pos_y + day_schedule_bar.hei*3)
    
            elif day_schedule_bar.types[day_schedule_bar.type_shown_id] == "Break":
                day_schedule_bar.types[day_schedule_bar.type_shown_id] = "Activity"
                #Find closest left node
                sort_index = [i for i in range(len(day_schedule_bar.nodes))]
                nodes_x = [int(i.pos_x) for i in day_schedule_bar.nodes]
                sort_index = [x for _,x in sorted(zip(nodes_x, sort_index))]
                nodes_x.sort()
                nodes_x_reduced = [i for i in nodes_x if mouseX-i > 0]
                sort_index_reduced = [i for _,i in zip(nodes_x, sort_index) if mouseX-_ > 0]
                if len(sort_index_reduced) > 0:
                    day_schedule_bar.type_shown_id = nodes_x.index(max(nodes_x_reduced))
                    l_close = max(nodes_x_reduced)
                    r_close = day_schedule_bar.nodes[sort_index[nodes_x.index(max(nodes_x_reduced))+1]].pos_x
                    wid = stringWidth(day_schedule_bar.types[day_schedule_bar.type_shown_id],'Helvetica', 20)
                    day_schedule_bar.type_shown = text_display(day_schedule_bar.types[day_schedule_bar.type_shown_id], (l_close + (r_close - l_close)/2) - wid/2, day_schedule_bar.pos_y + day_schedule_bar.hei*3)
    
        
        else:
            day_schedule_bar.type_shown = None

#If mouse is released
def mousereleased():
    global day_schedule_bar, drag_node
    day_schedule_bar.dragged = False
    drag_node = -1

#Add a node
def addNode():
#If not already filled with nodes
    if len(day_schedule_bar.nodes)-1 < int(day_schedule_bar.wid/day_schedule_bar.drag_change):
        #Look for an open space
        found_open = False
        check_pos = day_schedule_bar.pos_x + day_schedule_bar.wid
        time_placed = day_schedule_bar.time_total
        while found_open == False:
            check_pos -= day_schedule_bar.drag_change
            time_placed -= day_schedule_bar.smallest_interval
            open_space = True
                    
            for n in day_schedule_bar.nodes:
                if int(n.pos_x) == int(check_pos):
                    open_space = False
                
            if open_space == True:
                day_schedule_bar.nodes.append(node((check_pos - day_schedule_bar.pos_x)/day_schedule_bar.wid, 20, time_placed))
                day_schedule_bar.types.append("Activity")
                found_open = True

#Remove a node
def removeNode():
    if len(day_schedule_bar.nodes) > 3:
        sort_index = [i for i in range(len(day_schedule_bar.nodes))]
        nodes_x = [int(i.pos_x) for i in day_schedule_bar.nodes]
        sort_index = [x for _,x in sorted(zip(nodes_x, sort_index))]
        nodes_x.sort()
        del day_schedule_bar.nodes[sort_index[-2]]
        del day_schedule_bar.types[-1]

#Change time range
def rangeOption(type):
    global day_schedule_bar
    
    
    old_interval = day_schedule_bar.smallest_interval 
    
    if type == 1:
        day_schedule_bar.smallest_interval = 10
    if type == 2:
        day_schedule_bar.smallest_interval = 15
    if type == 3:
        day_schedule_bar.smallest_interval = 30
    
    sort_index = [i for i in range(len(day_schedule_bar.nodes))]
    nodes_x = [int(i.pos_x) for i in day_schedule_bar.nodes]
    sort_index = [x for _,x in sorted(zip(nodes_x, sort_index))]
    nodes_x.sort()
    
    rightmost_index = sort_index[nodes_x.index(max(nodes_x))]
    leftmost_index = sort_index[nodes_x.index(min(nodes_x))]
    
    #Change end nodes based on new interval
    for n in range(len(day_schedule_bar.nodes)):
        if n == rightmost_index or n == leftmost_index:
            time = day_schedule_bar.nodes[n].time + day_schedule_bar.start_time
            remaining_time = time % day_schedule_bar.smallest_interval
            
            if time % day_schedule_bar.smallest_interval != 0:
                if day_schedule_bar.smallest_interval - remaining_time >= remaining_time:
                    day_schedule_bar.nodes[n].time += day_schedule_bar.smallest_interval - remaining_time
                else:
                    day_schedule_bar.nodes[n].time -= remaining_time
        
    #Change the time_total based on possible changing of the ends, as well as the drag_change
    day_schedule_bar.time_total = day_schedule_bar.nodes[2].time - day_schedule_bar.nodes[0].time
    day_schedule_bar.drag_change = (float(day_schedule_bar.smallest_interval)/float(day_schedule_bar.time_total))*float(day_schedule_bar.wid)
    
    #Change the rest of the nodes accordingly
    for n in range(len(day_schedule_bar.nodes)):
        if n != rightmost_index and n != leftmost_index:
            time = day_schedule_bar.nodes[n].time + day_schedule_bar.start_time
            remaining_time = time % day_schedule_bar.smallest_interval
            
            if time % day_schedule_bar.smallest_interval != 0:
                if day_schedule_bar.smallest_interval - remaining_time >= remaining_time:
                    day_schedule_bar.nodes[n].time += day_schedule_bar.smallest_interval - remaining_time
                else:
                    day_schedule_bar.nodes[n].time -= remaining_time
            
            day_schedule_bar.nodes[n].pos_x = (float(day_schedule_bar.nodes[n].time) / float(day_schedule_bar.time_total))*day_schedule_bar.wid + day_schedule_bar.pos_x


#Change times of end nodes
def changeEndNodeTime(direction):
    global day_schedule_bar
    if day_schedule_bar.leftmost_clicked:
        
        node_in_way = False
        for n in day_schedule_bar.nodes:
            if n.time - day_schedule_bar.smallest_interval*direction == 0:
                node_in_way = True
        
        if node_in_way == False:
            day_schedule_bar.start_time += day_schedule_bar.smallest_interval*direction
            day_schedule_bar.time_total -= day_schedule_bar.smallest_interval*direction
            
            for n in range(len(day_schedule_bar.nodes)):
                if day_schedule_bar.nodes[n].pos_x != day_schedule_bar.pos_x:
                    day_schedule_bar.nodes[n].time -= day_schedule_bar.smallest_interval*direction
                
    elif day_schedule_bar.rightmost_clicked:
        node_in_way = False
        for n in day_schedule_bar.nodes:
            if n.time - day_schedule_bar.smallest_interval*direction == day_schedule_bar.time_total:
                node_in_way = True
        
        if node_in_way == False and day_schedule_bar.time_total < 25*60:
            day_schedule_bar.time_total += day_schedule_bar.smallest_interval*direction
            for n in range(len(day_schedule_bar.nodes)):
                if day_schedule_bar.nodes[n].pos_x == day_schedule_bar.pos_x + day_schedule_bar.wid:
                    day_schedule_bar.nodes[n].time += day_schedule_bar.smallest_interval*direction
    
    if day_schedule_bar.smallest_interval == 10:
        rangeOption(1)
    if day_schedule_bar.smallest_interval == 15:
        rangeOption(2)
    if day_schedule_bar.smallest_interval == 30:
        rangeOption(3)

#Get sign of a number (If it is 0, it will return pre-defined value y
def sign(x, y):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return y
    
#Check for mouseovers
def over_clickable(x, y, wid, hei): 
    return x <= mouseX <= x + wid and y <= mouseY <= y + hei
