class MainPage:
    def __init__(self):
        global main_page
        import MatchOrgAndSep
        import MonthlySchedule
        #import PDFCreation
        main_page = loadImage("background.jpg")
        #teamsNamed = []
        #teamsNamed = ["a", "b", "c", "d", "e", "f","g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G"]
        #MatchOrgAndSep.MatchMake(teamsNamed)
        #PDFCreation()
        #MonthlySchedule.display()
        
    def update(self):
        image(main_page,0,0,width,height)
        
        fill(10,190)
        rect(0,0,self.dim(150),height)
        
        rect(self.dim(200),self.dim(20,'y'),self.dim(550),height-self.dim(40,'y'),self.dim(10,'y'))
    def Del(self):
        del self
        clear()
    def dim(self,y, m = 'X'): 
        if m == 'X':
            return width*y/800
        else:
            return height*y/600
