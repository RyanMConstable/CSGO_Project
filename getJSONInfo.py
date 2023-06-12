import os, json, subprocess, re

pathToCSGODm = os.environ['PATH_TO_CSGODM']
pathToCSGOreplays = os.environ['PATH_TO_CSGOREPLAYS']
pathToCSGOreplay = os.environ['PATH_TO_CSGOREPLAY']


#Takes a single game code as input, downloads the file, then analyzes the file and downloads a json
#Opens the json and loads the json into a variable (can be improved), then returns the variable and the game code in a list
def getJSONInfo(code):
    #First tidys up the code
    code = code.strip()
    #Downloads, the given game using the path to the CSGODM, logs it to log.txt
    os.system(pathToCSGODm + " download " + str(code) + " > log.txt")
    
    files = os.listdir(pathToCSGOreplays)
    pathToJSON = None
    info = None
    
    #For the files in the directory, find the demo file
    for file in files:
        if file.split(".")[-1] == "dem":
            print("Demo found")
            pathToJSON = pathToCSGODm + " json " + os.path.join(pathToCSGOreplay, file)
            os.system(pathToJSON)
            break
    
    #If pathToJSON is not None, then empty it and load it to a json file
    if pathToJSON:
        newfile = os.path.join(pathToCSGOreplays, file) + ".json"
        w = open(newfile, "r", encoding = 'utf-8')
        info = json.loads(w.read())
        w.close()
        
    #Remove files from the directory
    clearReplayDir()
    
    #Return a list with index 0 being the given code, and index 1 being the information from the json file
    return [code, info]




#Takes a list in the format [gameCode, jsonLoadedVariable] and parses the information for what we want.
#It then returns a list including the game code, and another list containing each player and their stats in another list
def returnGameInfo(jsonInputFormat):
    #If the json variable in the list is none, then return
    if jsonInputFormat[1] == None:
        return
    
    #Initialize thisGame to the json loaded variable
    thisGame = jsonInputFormat[1]

    #Initialize playerlist
    playersList = []
    
    #Check to ensure that it's a long match and not any other type of game
    if thisGame["score_team1"] != 15 and thisGame["score_team1"] != 16 and thisGame["score_team2"] != 15 and thisGame["score_team2"] != 16:
        return
    
    #Set date of game played
    dt = thisGame["date"]
    
    #Loop for every player on team_ct, add parsed data (obnoxiously long)
    for player in thisGame["team_ct"]["team_players"]:
        playersList.append([player["steamid"], player["name"], player["kill_count"], player["score"], player["tk_count"], player["assist_count"], player["death_count"], player["5k_count"], player["4k_count"], player["3k_count"], player["2k_count"], player["1k_count"], player["hs_count"], player["kd"], player["esea_rws"], player["shot_count"], player["hit_count"], player["flashbang_count"], player["smoke_count"], player["he_count"], player["molotov_count"], player["incendiary_count"], player["decoy_count"], player["round_count"], "ct", dt])
        
    for player in thisGame["team_t"]["team_players"]:
        playersList.append([player["steamid"], player["name"], player["kill_count"], player["score"], player["tk_count"], player["assist_count"], player["death_count"], player["5k_count"], player["4k_count"], player["3k_count"], player["2k_count"], player["1k_count"], player["hs_count"], player["kd"], player["esea_rws"], player["shot_count"], player["hit_count"], player["flashbang_count"], player["smoke_count"], player["he_count"], player["molotov_count"], player["incendiary_count"], player["decoy_count"], player["round_count"], "t", dt])
    
    #Return the code, 
    return [jsonInputFormat[0], playersList]



#Deletes all files in the CSGO replays directory, returns nothing
#We want to keep the replays folder, but delete everything in it
def clearReplayDir():
    for file in os.listdir(pathToCSGOreplays):
        os.remove(os.path.join(pathToCSGOreplays, file))
    return


getJSONInfo('CSGO-TmtKB-aMoKk-FqZYO-ZJO3z-ozioE')