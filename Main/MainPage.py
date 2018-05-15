class MainPage:
    def __init__(self):
        import random
        import MatchOrgAndSep
        import MonthlySchedule
        main_page = loadImage("background.jpg")
        image(main_page,0,0,width,height)
        
        
        
        
        
        
        teamsNamed = []
        teamsNamed = ["a", "b", "c", "d", "e", "f","g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G"]
        random.shuffle(teamsNamed)
        #Total number of teams
        if len(teamsNamed) != 0:
            numberOfTeamsTotal = len(teamsNamed)
        else:
            numberOfTeamsTotal = 10

        #Number of games each team needs to play
        numberOfGamesPerTeam = 3

        #Number of times teams can play one another
        playAgainstOtherTeamMaxTimes = 1

        separationIterations = 5

        games = MatchOrgAndSep.getMatches(numberOfTeamsTotal, numberOfGamesPerTeam, playAgainstOtherTeamMaxTimes)
        #games[0] = left side teams of matches
        #games[1] = right side teams of matches
        #games[2] = filler matches indices (match with right side teams (games[1])

        #Filler matches teams/issues
        if len(games[0]) + len(games[2]) < int((numberOfTeamsTotal*numberOfGamesPerTeam)/2):
            if len(games[0]) == numberOfTeamsTotal*numberOfGamesPerTeam + len(games[2]):
                s = "\nFiller teams: "
                for i in games[2]:
                    s += str(games[1][i]) + ", "
                print(s[:-2])
            else:
                print("No filler games possible to balance playing time")
                print("Games Achieved: " + str(len(games[0]) + len(games[2])))
                print("Games Needed: " + str(int((numberOfTeamsTotal*numberOfGamesPerTeam)/2)))
        trueMatchIndices = [i for i in range(len(games[0]))]

        changing = True

        while changing:
            gamesBefore = MatchOrgAndSep.copyList(games)
    
            for fakeMatch in range(len(games[0])):
                match = trueMatchIndices.index(fakeMatch)
                scoreBefore = MatchOrgAndSep.calculateSeparationScore(games[0],games[1])
                addScore = -1
                subtractScore = -1

                gamesAdd = []
                for i in games:
                    gamesAdd.append(i[:])
        
                if match + 1 <= len(games[0])-1:
                    gamesAdd[0][match], gamesAdd[0][match+1] = gamesAdd[0][match+1], gamesAdd[0][match]
                    gamesAdd[1][match], gamesAdd[1][match+1] = gamesAdd[1][match+1], gamesAdd[1][match]
                    addScore = MatchOrgAndSep.calculateSeparationScore(gamesAdd[0],gamesAdd[1])
        
                gamesSubtract = []
                for i in games:
                    gamesSubtract.append(i[:])
        
                if match - 1 >= 0:
                    gamesSubtract[0][match], gamesSubtract[0][match-1] = gamesSubtract[0][match-1], gamesSubtract[0][match]
                    gamesSubtract[1][match], gamesSubtract[1][match-1] = gamesSubtract[1][match-1], gamesSubtract[1][match]
                    subtractScore = MatchOrgAndSep.calculateSeparationScore(gamesSubtract[0],gamesSubtract[1])

                if addScore != -1:
                    if addScore > scoreBefore and addScore > subtractScore:
                        games = MatchOrgAndSep.copyList(gamesAdd)
                        trueMatchIndices[match], trueMatchIndices[match+1] = trueMatchIndices[match+1], trueMatchIndices[match]

                        improving = True
                        while improving:
                            match = trueMatchIndices.index(fakeMatch)
                            gamesAdd = MatchOrgAndSep.copyList(games)

                            scoreBefore = MatchOrgAndSep.calculateSeparationScore(games[0],games[1])
            
                            if match + 1 <= len(games[0])-1:
                                gamesAdd[0][match], gamesAdd[0][match+1] = gamesAdd[0][match+1], gamesAdd[0][match]
                                gamesAdd[1][match], gamesAdd[1][match+1] = gamesAdd[1][match+1], gamesAdd[1][match]
                                addScore = MatchOrgAndSep.calculateSeparationScore(gamesAdd[0],gamesAdd[1])
                        
                                if addScore > scoreBefore:
                                    games = MatchOrgAndSep.copyList(gamesAdd)
                                    trueMatchIndices[match], trueMatchIndices[match+1] = trueMatchIndices[match+1], trueMatchIndices[match]
                                else:
                                    improving = False
                            else:
                                improving = False

                if subtractScore != -1:
                    if subtractScore > scoreBefore and subtractScore > addScore:
                        games = MatchOrgAndSep.copyList(gamesSubtract)
                        trueMatchIndices[match], trueMatchIndices[match-1] = trueMatchIndices[match-1], trueMatchIndices[match]

                        improving = True
                        while improving:
                            match = trueMatchIndices.index(fakeMatch)
                            gamesSubtract = MatchOrgAndSep.copyList(games)

                            scoreBefore = MatchOrgAndSep.calculateSeparationScore(games[0],games[1])
        
                            if match + 1 <= len(games[0])-1:
                                gamesSubtract[0][match], gamesSubtract[0][match-1] = gamesSubtract[0][match-1], gamesSubtract[0][match]
                                gamesSubtract[1][match], gamesSubtract[1][match-1] = gamesSubtract[1][match-1], gamesSubtract[1][match]
                                subtractScore = MatchOrgAndSep.calculateSeparationScore(gamesSubtract[0],gamesSubtract[1])
                        
                                if subtractScore > scoreBefore:
                                    games = MatchOrgAndSep.copyList(gamesSubtract)
                                    trueMatchIndices[match], trueMatchIndices[match-1] = trueMatchIndices[match-1], trueMatchIndices[match]
                                else:
                                    improving = False
                            else:
                                improving = False
        
            if gamesBefore == games:
                changing = False



        if len(teamsNamed) != 0:
            #print(calculateSeparationScore(games[0],games[1]))
            MatchOrgAndSep.printGames(games, teamsNamed, True)
        else:
            #print(calculateSeparationScore(games[0],games[1]))
            MatchOrgAndSep.printGames(games, None, False)
            
            
        MonthlySchedule.display()
