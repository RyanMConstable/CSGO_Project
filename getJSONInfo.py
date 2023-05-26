import os
import json

#1 download command to download with share code
#2 Find where it downloaded, analyze it
#3 Download into JSON file
#4 Parse JSON file for DATA
#5 Add information to database
#6 Delete Files

def getJSONInfo(code):
    pathToCSGODm = os.path.abspath(r'C:/\"Program Files (x86)\"/\"CSGO Demos Manager\"/csgodm.exe')
    pathToCSGOreplays = os.path.abspath(r'C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/csgo/replays')
    os.system(pathToCSGODm + " download " + str(code))
    files = os.listdir(pathToCSGOreplays)
    pathToAnlyze = None
    for file in files:
        if file.split(".")[-1] == "dem":
            pathToAnlyze = pathToCSGODm + " analyze " + r'C:/"Program Files (x86)"/Steam/steamapps/common/"Counter-Strike Global Offensive"/csgo/replays/' + file
            os.system(pathToAnlyze)
    pathToJSON = None
    if pathToAnlyze:
        pathToJSON = pathToCSGODm + " json " + r'C:/"Program Files (x86)"/Steam/steamapps/common/"Counter-Strike Global Offensive"/csgo/replays/'
        os.system(pathToJSON)
    if pathToJSON:
        pathToJSON = pathToCSGODm + " json " + r'C:/"Program Files (x86)"/Steam/steamapps/common/"Counter-Strike Global Offensive"/csgo/replays/' + file
        w = open(pathToCSGOreplays + "/" + file)
        info = w.read()
        w.close()
        return [code, info]
    return

#Takes the output from the above function and turns the json into the statistics we want to grab from the game for all 10 players
def returnGameInfo(jsonInputFormat):

    gameJSON = jsonInputFormat[1]

    thisGame = json.loads(gameJSON)

    playersList = []
    
    for player in thisGame["team_ct"]["team_players"]:
        playersList.append([player["steamid"], player["name"], player["kill_count"], player["score"], player["tk_count"], player["assist_count"], player["death_count"], player["5k_count"], player["4k_count"], player["3k_count"], player["2k_count"], player["1k_count"], player["hs_count"], player["kd"], player["esea_rws"], player["shot_count"], player["hit_count"], player["flashbang_count"], player["smoke_count"], player["he_count"], player["molotov_count"], player["incendiary_count"], player["decoy_count"], player["round_count"]])
        
    for player in thisGame["team_t"]["team_players"]:
        playersList.append([player["steamid"], player["name"], player["kill_count"], player["score"], player["tk_count"], player["assist_count"], player["death_count"], player["5k_count"], player["4k_count"], player["3k_count"], player["2k_count"], player["1k_count"], player["hs_count"], player["kd"], player["esea_rws"], player["shot_count"], player["hit_count"], player["flashbang_count"], player["smoke_count"], player["he_count"], player["molotov_count"], player["incendiary_count"], player["decoy_count"], player["round_count"]])
    
    return [jsonInputFormat[0], playersList]