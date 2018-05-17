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
    def Del(self):
        del self
        clear()
