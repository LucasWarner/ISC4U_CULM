class MainPage:
    def __init__(self):
        import MatchOrgAndSep
        import MonthlySchedule
        main_page = loadImage("background.jpg")
        image(main_page,0,0,width,height)
        
        teamsNamed = []
        teamsNamed = ["a", "b", "c", "d", "e", "f","g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G"]
        MatchOrgAndSep.MatchMake(teamsNamed)
            
            
        MonthlySchedule.display()
    def Del(self):
        del self
        clear()
