"""
Filler team options:
1 - Use filler teams
2 - Just have some teams play less
3 - Enter a recommended game number, and the program will find the nearest number of teams that will work out perfectly

"""

"""
Randomize button to run it again with the same settings? But with random.shuffle, it won't be the same?
"""
import MainPage
def getMatches(teamNumber, numberOfGamesEach, canPlaySameTeamTimes):

    #Team names
    teams = [str(i+1) for i in range(teamNumber)]

    #Teams played (Each team tracks who they have played)
    teamsPlayed = [[] for i in range(len(teams)) ]

    #Shuffle the list of teams, otherwise, they it will be the exact same every time (May even want a randomize button to do the matches again?)
    #random.shuffle(teams)


    #Games recorded (Kept separate to do match separation, but match in index)
    gamesLeft = []
    gamesRight = []

    #Team options (While loop ends when there are no more options, so options must start with an element inside)
    options = [""]

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

        #Make sure there are options
        if len(options) > 0:
            #Choose the team that also has the lowest number of matches
            teamsToPlay = [len(teamsPlayed[i]) for i in options]
            play = options[teamsToPlay.index(min(teamsToPlay))]

            #Set up the match
            gamesLeft.append(int(teams[lowestPlayingTeam]))
            gamesRight.append(int(teams[play]))
            teamsPlayed[lowestPlayingTeam].append(teams[play])
            teamsPlayed[play].append(teams[lowestPlayingTeam])
        else:
            #If there are no options, then there will be filler games
            filler = True

    #FILLER
    fillerIndex = []
    
    #If filler is needed
    if filler == True:
        fillerNeeded = []
        #Select teams that need filler matches
        for y in range(len(teamsPlayed)):
            if teamsPlayed[y] != numberOfGamesEach:
                fillerNeeded.append(y)

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

    return [gamesLeft, gamesRight, fillerIndex]


def printGames(games, assignTeams, teamNameReturn):
    print("\n")
    if teamNameReturn == False:
        for i in range(len(games[0])):
            if i not in games[2]:
                print("{0} vs {1}".format(games[0][i], games[1][i]))
            else:
                print("{0} vs {1} ({1} as filler)".format(games[0][i], games[1][i]))
    else:
        for i in range(len(games[0])):
            if i not in games[2]:
                print("Match {0}: {1} vs {2}".format(i, assignTeams[games[0][i]-1], assignTeams[games[1][i]-1]))
            else:
                print("Match {0}: {1} vs {2} ({2} as filler)".format(i, assignTeams[games[0][i]-1], assignTeams[games[1][i]-1])) 
    print("\n\n")

#Now for separation!

"""
Idea 1:

The Shift Organization
Go through every team matching and shift them
Tries shifting the match up and down
If it increases the overall score of the separation on a side, then it completes that shift
If both ways increase the overall score, it will choose whichever increases it more

It then continues to try to move in that direction - ends when it stops increasing the overall score, or reaches the end of the list

If it decreases the overall score of the separation, it reverts to how it was before and moves on to shifting the next match
"""


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

def copyList(a):
    return [i[:] for i in a]


"""
if len(teamsNamed) != 0:
    print(calculateSeparationScore(games[0],games[1]))
    printGames(games, teamsNamed, True)
else:
    print(calculateSeparationScore(games[0],games[1]))
    printGames(games, None, False)
"""
