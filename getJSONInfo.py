import os
import json


#Takes a game code and returns the format [code, info], info can be None
def getJSONInfo(code):
    code = code.strip()
    pathToCSGODm = os.path.abspath(r'C:/\"Program Files (x86)\"/\"CSGO Demos Manager\"/csgodm.exe')
    pathToCSGOreplays = os.path.abspath(r'C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/csgo/replays')
    os.system(pathToCSGODm + " download " + str(code))
    files = os.listdir(pathToCSGOreplays)
    pathToJSON = None
    file = None
    info = None
    for file in files:
        if file.split(".")[-1] == "dem":
            pathToJSON = pathToCSGODm + " json " + r'C:/"Program Files (x86)"/Steam/steamapps/common/"Counter-Strike Global Offensive"/csgo/replays/' + file
            os.system(pathToJSON)
            break
    
    if pathToJSON:
        w = open(pathToCSGOreplays + "/" + file + ".json", "r", encoding = 'utf-8')
        info = json.loads(w.read())
        w.close()
    clearReplayDir()
    return [code, info]

#Takes the output from the above function and turns the json into the statistics we want to grab from the game for all 10 players
def returnGameInfo(jsonInputFormat):
    if jsonInputFormat[1] == None:
        return
    thisGame = jsonInputFormat[1]

    playersList = []
    dt = thisGame["date"]
    for player in thisGame["team_ct"]["team_players"]:
        playersList.append([player["steamid"], player["name"], player["kill_count"], player["score"], player["tk_count"], player["assist_count"], player["death_count"], player["5k_count"], player["4k_count"], player["3k_count"], player["2k_count"], player["1k_count"], player["hs_count"], player["kd"], player["esea_rws"], player["shot_count"], player["hit_count"], player["flashbang_count"], player["smoke_count"], player["he_count"], player["molotov_count"], player["incendiary_count"], player["decoy_count"], player["round_count"], "ct", dt])
        
    for player in thisGame["team_t"]["team_players"]:
        playersList.append([player["steamid"], player["name"], player["kill_count"], player["score"], player["tk_count"], player["assist_count"], player["death_count"], player["5k_count"], player["4k_count"], player["3k_count"], player["2k_count"], player["1k_count"], player["hs_count"], player["kd"], player["esea_rws"], player["shot_count"], player["hit_count"], player["flashbang_count"], player["smoke_count"], player["he_count"], player["molotov_count"], player["incendiary_count"], player["decoy_count"], player["round_count"], "t", dt])
    
    #returns [code, [playerListStats]]
    return [jsonInputFormat[0], playersList]

#Deletes all files in the CSGO replays directory, returns nothing
def clearReplayDir():
    pathToCSGOreplays = os.path.abspath(r'C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/csgo/replays/')
    for file in os.listdir(os.path.join(pathToCSGOreplays)):
        os.remove(os.path.join(pathToCSGOreplays, file))
    return