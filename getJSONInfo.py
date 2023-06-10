import os
import json


#Takes a single game code as input, downloads the file, then analyzes the file and downloads a json
#Opens the json and loads the json into a variable (can be improved), then returns the variable and the game code in a list
def getJSONInfo(code):
    #First tidys up the code
    code = code.strip()
    #Takes environment variables for paths to both CSGODM third party, and the CSGOreplay directory folder
    pathToCSGODm = os.environ['PATH_TO_CSGODM']
    pathToCSGOreplays = os.environ['PATH_TO_CSGOREPLAYS']
    pathToCSGOreplay = os.environ['PATH_TO_CSGOREPLAY']
    #Downloads, the given game using the path to the CSGODM
    os.system(pathToCSGODm + " download " + str(code))
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




#Takes the output from the above function and turns the json into the statistics we want to grab from the game for all 10 players
def returnGameInfo(jsonInputFormat):
    if jsonInputFormat[1] == None:
        return
    thisGame = jsonInputFormat[1]

    playersList = []
    dt = thisGame["date"]
    
    #In case it's not a long match, or any other game mode
    if thisGame["score_team1"] != 15 and thisGame["score_team1"] != 16 and thisGame["score_team2"] != 15 and thisGame["score_team2"] != 16:
        return
    
    
    for player in thisGame["team_ct"]["team_players"]:
        playersList.append([player["steamid"], player["name"], player["kill_count"], player["score"], player["tk_count"], player["assist_count"], player["death_count"], player["5k_count"], player["4k_count"], player["3k_count"], player["2k_count"], player["1k_count"], player["hs_count"], player["kd"], player["esea_rws"], player["shot_count"], player["hit_count"], player["flashbang_count"], player["smoke_count"], player["he_count"], player["molotov_count"], player["incendiary_count"], player["decoy_count"], player["round_count"], "ct", dt])
        
    for player in thisGame["team_t"]["team_players"]:
        playersList.append([player["steamid"], player["name"], player["kill_count"], player["score"], player["tk_count"], player["assist_count"], player["death_count"], player["5k_count"], player["4k_count"], player["3k_count"], player["2k_count"], player["1k_count"], player["hs_count"], player["kd"], player["esea_rws"], player["shot_count"], player["hit_count"], player["flashbang_count"], player["smoke_count"], player["he_count"], player["molotov_count"], player["incendiary_count"], player["decoy_count"], player["round_count"], "t", dt])
    
    return [jsonInputFormat[0], playersList]

#Deletes all files in the CSGO replays directory, returns nothing
def clearReplayDir():
    pathToCSGOreplays = os.path.abspath(r'C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/csgo/replays/')
    for file in os.listdir(os.path.join(pathToCSGOreplays)):
        os.remove(os.path.join(pathToCSGOreplays, file))
    return



print(getJSONInfo('CSGO-TmtKB-aMoKk-FqZYO-ZJO3z-ozioE'))