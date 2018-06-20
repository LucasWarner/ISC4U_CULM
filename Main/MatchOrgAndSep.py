import random
import CheckBox

#Function to organize teams and separate matches
def MatchMake(teamsNamed, numberOfGamesPerTeam, playAgainstOtherTeamMaxTimes):
    #teamsNamed - List of team names
    #numberOfGamesPerTeam - Number of games each team needs to play
    #playAgainstOtherTeamMaxTimes - Number of times teams can play one another
    
    #Total number of teams
    numberOfTeamsTotal = len(teamsNamed)

    #Randomize team order to get different match results each time
    random.shuffle(teamsNamed)

    games = getMatches(numberOfTeamsTotal, numberOfGamesPerTeam, playAgainstOtherTeamMaxTimes)
    #games[0] - left side teams of matches
    #games[1] - right side teams of matches
    #games[2] - filler matches indices (match with right side teams (games[1])
    
    #Set up match separation
    trueMatchIndices = [i for i in range(len(games[0]))]
    changing = True
    
    """
    The Shift Separation (Created by Kaden McKeen)
    Loop through every match and try shifting it up and down
    If it increases the overall score of the separation on one side, then it will complete the shift in that direction
    If both ways increase the overall score, it will choose whichever increases it more
    
    It then continues to try to move in that direction and stops when the overall separation score stops increasing, or when it reaches the end of the list
    
    If the shift decreases the overall score of the separation, it reverts to before the shift and moves on trying to shift the next match
    
    It will loop through and do this several times, until no more changes are made (ie, no shifting for any match increases the separation score)
    This means (theoretically), it acheives the absolute best results possible
    """
    
    while changing:
        gamesBefore = copyList(games)
    
        for fakeMatch in range(len(games[0])):
            match = trueMatchIndices.index(fakeMatch)
            scoreBefore = calculateSeparationScore(games[0],games[1])
            addScore = -1
            subtractScore = -1

            gamesAdd = []
            for i in games:
                gamesAdd.append(i[:])
        
            if match + 1 <= len(games[0])-1:
                gamesAdd[0][match], gamesAdd[0][match+1] = gamesAdd[0][match+1], gamesAdd[0][match]
                gamesAdd[1][match], gamesAdd[1][match+1] = gamesAdd[1][match+1], gamesAdd[1][match]
                addScore = calculateSeparationScore(gamesAdd[0],gamesAdd[1])
        
            gamesSubtract = []
            for i in games:
                gamesSubtract.append(i[:])
        
            if match - 1 >= 0:
                gamesSubtract[0][match], gamesSubtract[0][match-1] = gamesSubtract[0][match-1], gamesSubtract[0][match]
                gamesSubtract[1][match], gamesSubtract[1][match-1] = gamesSubtract[1][match-1], gamesSubtract[1][match]
                subtractScore = calculateSeparationScore(gamesSubtract[0],gamesSubtract[1])

            if addScore != -1:
                if addScore > scoreBefore and addScore > subtractScore:
                    games = copyList(gamesAdd)
                    trueMatchIndices[match], trueMatchIndices[match+1] = trueMatchIndices[match+1], trueMatchIndices[match]

                    improving = True
                    while improving:
                        match = trueMatchIndices.index(fakeMatch)
                        gamesAdd = copyList(games)

                        scoreBefore = calculateSeparationScore(games[0],games[1])
            
                        if match + 1 <= len(games[0])-1:
                            gamesAdd[0][match], gamesAdd[0][match+1] = gamesAdd[0][match+1], gamesAdd[0][match]
                            gamesAdd[1][match], gamesAdd[1][match+1] = gamesAdd[1][match+1], gamesAdd[1][match]
                            addScore = calculateSeparationScore(gamesAdd[0],gamesAdd[1])
                        
                            if addScore > scoreBefore:
                                games = copyList(gamesAdd)
                                trueMatchIndices[match], trueMatchIndices[match+1] = trueMatchIndices[match+1], trueMatchIndices[match]
                            else:
                                improving = False
                        else:
                            improving = False

            if subtractScore != -1:
                if subtractScore > scoreBefore and subtractScore > addScore:
                    games = copyList(gamesSubtract)
                    trueMatchIndices[match], trueMatchIndices[match-1] = trueMatchIndices[match-1], trueMatchIndices[match]

                    improving = True
                    while improving:
                        match = trueMatchIndices.index(fakeMatch)
                        gamesSubtract = copyList(games)

                        scoreBefore = calculateSeparationScore(games[0],games[1])
        
                        if match + 1 <= len(games[0])-1:
                            gamesSubtract[0][match], gamesSubtract[0][match-1] = gamesSubtract[0][match-1], gamesSubtract[0][match]
                            gamesSubtract[1][match], gamesSubtract[1][match-1] = gamesSubtract[1][match-1], gamesSubtract[1][match]
                            subtractScore = calculateSeparationScore(gamesSubtract[0],gamesSubtract[1])
                        
                            if subtractScore > scoreBefore:
                                games = copyList(gamesSubtract)
                                trueMatchIndices[match], trueMatchIndices[match-1] = trueMatchIndices[match-1], trueMatchIndices[match]
                            else:
                                improving = False
                        else:
                            improving = False
        
        if gamesBefore == games:
            changing = False
    
    #Returns the newly-separated matches
    if len(teamsNamed) != 0:
        return printGames(games, teamsNamed, True)
    else:
        return printGames(games, None, False)

#Calculates the separation score that exist between the matches
def calculateSeparationScore(matchesLeft, matchesRight):
    score = 0
    teamMatchIndices = []
    for a in range(max(matchesRight+matchesLeft)):
        teamIndicesLeft = [i for i, x in enumerate(matchesLeft) if x == a+1]
        teamIndicesRight = [i for i, x in enumerate(matchesRight) if x == a+1]
        teamMatchIndices.append(teamIndicesLeft+teamIndicesRight)
        teamMatchIndices[-1].sort()

    for t in range(len(teamMatchIndices)):
        avScore = 0        
        for m in range(len(teamMatchIndices[t])-1):
            avScore += (teamMatchIndices[t][m+1]-teamMatchIndices[t][m])
        score += avScore**2

    return score

#Creates the match-ups between teams
def getMatches(teamNumber, numberOfGamesEach, canPlaySameTeamTimes):
    #Team names
    teams = [str(i+1) for i in range(teamNumber)]

    #Teams played (Each team tracks who they have played)
    teamsPlayed = [[] for i in range(len(teams)) ]

    #Games recorded (Kept separate to do match separation, but match in index)
    gamesLeft = []
    gamesRight = []

    #Team options (While loop ends when there are no more options, so options must start with an element inside)
    options = [""]

    print("Happened0")
    #Teams with least games will be pick or be picked, otherwise, the next index will be picked
    while len(options) != 0:
        lowestPlayingTeam = teamsPlayed.index(min(teamsPlayed, key=len))
        if len(teamsPlayed[lowestPlayingTeam]) == numberOfGamesEach:
            filler = False
            break
        
        options = []
        #Get different possible options based on restrictions
        for i in range(len(teams)):
            if lowestPlayingTeam != i and len(teamsPlayed[i]) < numberOfGamesEach and teamsPlayed[lowestPlayingTeam].count(teams[i]) < canPlaySameTeamTimes:
                options.append(i)
        
        #print(options)
        print("Lowest above: " + str(lowestPlayingTeam))
        #Make sure there are options
        if len(options) > 0:
            #Choose the team that also has the lowest number of matches
            teamsToPlay = [len(teamsPlayed[i]) for i in options]
            play = options[teamsToPlay.index(min(teamsToPlay))]
            print("Lowest below: " + str(play))
            #Set up the match
            gamesLeft.append(int(teams[lowestPlayingTeam]))
            gamesRight.append(int(teams[play]))
            teamsPlayed[lowestPlayingTeam].append(teams[play])
            teamsPlayed[play].append(teams[lowestPlayingTeam])
        else:
            #If there are no options, then there will be filler games
            filler = True
    
    print("Happened1")
    
    #Tracking filler teams (If needed)
    fillerIndex = []
    
    #Check if filler matches are allowed
    for checkbox in CheckBox.checkboxes:
        if checkbox.id == 1:
            filler_allowed = checkbox.clicked
    
    #print("Happened0")
    #If filler is needed and allowed by the user
    if filler_allowed:
        if filler:
            fillerNeeded = []
            #Select teams that need filler matches
            for team_select in range(len(teamsPlayed)):
                if teamsPlayed[team_select] != numberOfGamesEach:
                    fillerNeeded.append(team_select)
    
            #Iterate through teams that need filler
            for i in fillerNeeded:
                #Find possible filler teams
                for j in range(len(teams)):
                    #Make sure the teams actually needs more filler matches
                    if len(teamsPlayed[i]) < numberOfGamesEach:
                        #Check to make sure they haven't already played this team too many times
                        #Make sure that this team hasn't already been chosen as a filler a bunch (Using mode to determine whether times played is too high to have another)
                        gamesPlayed = [len(x) for x in teamsPlayed]
                        if i != j and teamsPlayed[int(i)].count(teams[j]) < canPlaySameTeamTimes and len(teamsPlayed[j]) <= max(set(gamesPlayed), key=gamesPlayed.count):
                            #Set up the match with the label 'filler' for the one team
                            gamesLeft.append(int(teams[i]))
                            gamesRight.append(int(teams[j]))
                            fillerIndex.append(len(gamesRight)-1)
                            teamsPlayed[i].append(teams[j])
                            teamsPlayed[j].append("As Filler: " + teams[i])
    else:
        options = []        
    
    return [gamesLeft, gamesRight, fillerIndex]


#Returns the nicely formatting strings to be printed in the PDF
def printGames(games, assignTeams, teamNameReturn):
    matches = []
    if teamNameReturn == False:
        for i in range(len(games[0])):
            if i not in games[2]:
                matches.append("{0} vs {1}".format(i+1, games[0][i], games[1][i]))
            else:
               matches.append("{0} vs {1} ({1} as filler)".format(i+1, games[0][i], games[1][i]))
    else:
        for i in range(len(games[0])):
            if i not in games[2]:
                matches.append("{0}: {1} vs {2}".format(i+1, assignTeams[games[0][i]-1], assignTeams[games[1][i]-1]))
            else:
                matches.append("{0}: {1} vs {2} ({2} as filler)".format(i+1, assignTeams[games[0][i]-1], assignTeams[games[1][i]-1]))

    return matches


#Copies a list to be identical, without actually making one directly equal to another and changing both simultaneously
def copyList(a):
    return [i[:] for i in a]
