# -------------------------------------------------------------------------------

# Name:           MatchOrgAndSep.py

# Purpose:        File to organize team matches and separate them in an ideal fashion

# Author:         Warner.Lucas, McKeen.Kaden

#

# Created:        13/04/2018

# ------------------------------------------------------------------------------

import random
import CheckBox

#Function to organize teams and separate matches
def MatchMake(teams_named, games_per_team, max_games_per):
    #teams_named - List of team names
    #games_per_team - Number of games each team needs to play
    #max_games_per - Number of times teams can play one another
    
    #Total number of teams
    numberOfTeamsTotal = len(teams_named)

    #Randomize team order to get different match results each time
    random.shuffle(teams_named)

    games = getMatches(numberOfTeamsTotal, games_per_team, max_games_per)
    #games[0] - left side teams of matches
    #games[1] - right side teams of matches
    #games[2] - filler matches indices (match with right side teams (games[1])
    
    #Set up match separation
    true_match_indices = [i for i in range(len(games[0]))]
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
        games_before = copyList(games)
    
        for fake_match in range(len(games[0])):
            match = true_match_indices.index(fake_match)
            score_before = calculateSeparationScore(games[0],games[1])
            add_score = -1
            subtract_score = -1

            games_add = []
            for i in games:
                games_add.append(i[:])
        
            if match + 1 <= len(games[0])-1:
                games_add[0][match], games_add[0][match+1] = games_add[0][match+1], games_add[0][match]
                games_add[1][match], games_add[1][match+1] = games_add[1][match+1], games_add[1][match]
                add_score = calculateSeparationScore(games_add[0],games_add[1])
        
            games_subtract = []
            for i in games:
                games_subtract.append(i[:])
        
            if match - 1 >= 0:
                games_subtract[0][match], games_subtract[0][match-1] = games_subtract[0][match-1], games_subtract[0][match]
                games_subtract[1][match], games_subtract[1][match-1] = games_subtract[1][match-1], games_subtract[1][match]
                subtract_score = calculateSeparationScore(games_subtract[0],games_subtract[1])

            if add_score != -1:
                if add_score > score_before and add_score > subtract_score:
                    games = copyList(games_add)
                    true_match_indices[match], true_match_indices[match+1] = true_match_indices[match+1], true_match_indices[match]

                    improving = True
                    while improving:
                        match = true_match_indices.index(fake_match)
                        games_add = copyList(games)

                        score_before = calculateSeparationScore(games[0],games[1])
            
                        if match + 1 <= len(games[0])-1:
                            games_add[0][match], games_add[0][match+1] = games_add[0][match+1], games_add[0][match]
                            games_add[1][match], games_add[1][match+1] = games_add[1][match+1], games_add[1][match]
                            add_score = calculateSeparationScore(games_add[0],games_add[1])
                        
                            if add_score > score_before:
                                games = copyList(games_add)
                                true_match_indices[match], true_match_indices[match+1] = true_match_indices[match+1], true_match_indices[match]
                            else:
                                improving = False
                        else:
                            improving = False

            if subtract_score != -1:
                if subtract_score > score_before and subtract_score > add_score:
                    games = copyList(games_subtract)
                    true_match_indices[match], true_match_indices[match-1] = true_match_indices[match-1], true_match_indices[match]

                    improving = True
                    while improving:
                        match = true_match_indices.index(fake_match)
                        games_subtract = copyList(games)

                        score_before = calculateSeparationScore(games[0],games[1])
        
                        if match + 1 <= len(games[0])-1:
                            games_subtract[0][match], games_subtract[0][match-1] = games_subtract[0][match-1], games_subtract[0][match]
                            games_subtract[1][match], games_subtract[1][match-1] = games_subtract[1][match-1], games_subtract[1][match]
                            subtract_score = calculateSeparationScore(games_subtract[0],games_subtract[1])
                        
                            if subtract_score > score_before:
                                games = copyList(games_subtract)
                                true_match_indices[match], true_match_indices[match-1] = true_match_indices[match-1], true_match_indices[match]
                            else:
                                improving = False
                        else:
                            improving = False
        
        if games_before == games:
            changing = False
    
    #Returns the newly-separated matches
    if len(teams_named) != 0:
        return printGames(games, teams_named, True)
    else:
        return printGames(games, None, False)

#Calculates the separation score that exist between the matches
def calculateSeparationScore(matches_left, matches_right):
    score = 0
    team_match_indices = []
    for a in range(max(matches_right+matches_left)):
        team_indices_left = [i for i, x in enumerate(matches_left) if x == a+1]
        team_indices_right = [i for i, x in enumerate(matches_right) if x == a+1]
        team_match_indices.append(team_indices_left+team_indices_right)
        team_match_indices[-1].sort()

    for t in range(len(team_match_indices)):
        av_score = 0        
        for m in range(len(team_match_indices[t])-1):
            av_score += (team_match_indices[t][m+1]-team_match_indices[t][m])
        score += av_score**2

    return score

#Creates the match-ups between teams
def getMatches(team_number, num_of_games_each, can_play_team_times):
    #Team names
    teams = [str(i+1) for i in range(team_number)]

    #Teams played (Each team tracks who they have played)
    teams_played = [[] for i in range(len(teams)) ]

    #Games recorded (Kept separate to do match separation, but match in index)
    games_left = []
    games_right = []

    #Team options (While loop ends when there are no more options, so options must start with an element inside)
    options = [""]

    #Teams with least games will be pick or be picked, otherwise, the next index will be picked
    while len(options) != 0:
        team_least_played = teams_played.index(min(teams_played, key=len))
        if len(teams_played[team_least_played]) == num_of_games_each:
            filler = False
            break
        
        options = []
        #Get different possible options based on restrictions
        for i in range(len(teams)):
            if team_least_played != i and len(teams_played[i]) < num_of_games_each and teams_played[team_least_played].count(teams[i]) < can_play_team_times:
                options.append(i)
        
        #Make sure there are options
        if len(options) > 0:
            #Choose the team that also has the lowest number of matches
            teams_to_play = [len(teams_played[i]) for i in options]
            play = options[teams_to_play.index(min(teams_to_play))]
            
            #Set up the match
            games_left.append(int(teams[team_least_played]))
            games_right.append(int(teams[play]))
            teams_played[team_least_played].append(teams[play])
            teams_played[play].append(teams[team_least_played])
        else:
            #If there are no options, then there will be filler games
            filler = True
    
    #Tracking filler teams (If needed)
    filler_index = []
    
    #Check if filler matches are allowed
    for checkbox in CheckBox.checkboxes:
        if checkbox.id == 1:
            filler_allowed = checkbox.clicked
    
    #If filler is needed and allowed by the user
    if filler_allowed:
        #If filler is required
        if filler:
            filler_needed = []
            #Select teams that need filler matches
            for team_select in range(len(teams_played)):
                if teams_played[team_select] != num_of_games_each:
                    filler_needed.append(team_select)
    
            #Iterate through teams that need filler
            for i in filler_needed:
                #Find possible filler teams
                for j in range(len(teams)):
                    #Make sure the teams actually needs more filler matches
                    if len(teams_played[i]) < num_of_games_each:
                        #Check to make sure they haven't already played this team too many times
                        #Make sure that this team hasn't already been chosen as a filler a bunch (Using mode to determine whether times played is too high to have another)
                        gamesPlayed = [len(x) for x in teams_played]
                        if i != j and teams_played[int(i)].count(teams[j]) < can_play_team_times and len(teams_played[j]) <= max(set(gamesPlayed), key=gamesPlayed.count):
                            #Set up the match with the label 'filler' for the one team
                            games_left.append(int(teams[i]))
                            games_right.append(int(teams[j]))
                            filler_index.append(len(games_right)-1)
                            teams_played[i].append(teams[j])
                            teams_played[j].append("As Filler: " + teams[i])
    else:
        options = []        
    
    return [games_left, games_right, filler_index]


#Returns the nicely formatting strings to be printed in the PDF
def printGames(games, assign_teams, team_name_return):
    matches = []
    if team_name_return == False:
        for i in range(len(games[0])):
            if i not in games[2]:
                matches.append("{0} vs {1}".format(i+1, games[0][i], games[1][i]))
            else:
               matches.append("{0} vs {1} ({1} as filler)".format(i+1, games[0][i], games[1][i]))
    else:
        for i in range(len(games[0])):
            if i not in games[2]:
                matches.append("{0}: {1} vs {2}".format(i+1, assign_teams[games[0][i]-1], assign_teams[games[1][i]-1]))
            else:
                matches.append("{0}: {1} vs {2} ({2} as filler)".format(i+1, assign_teams[games[0][i]-1], assign_teams[games[1][i]-1]))

    return matches


#Copies a list to be identical, without actually making one directly equal to another and changing both simultaneously
def copyList(a):
    return [i[:] for i in a]
