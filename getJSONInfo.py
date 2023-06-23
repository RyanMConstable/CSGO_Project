import os, json, shutil, subprocess
from multiprocessing import Pool


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
        print(player['average_health_damage'])
        playersList.append([player["steamid"], player["name"], player["kill_count"], player["score"], player["tk_count"], player["assist_count"], player["death_count"], player["5k_count"], player["4k_count"], player["3k_count"], player["2k_count"], player["1k_count"], player["hs_count"], player["kd"], player["esea_rws"], player["shot_count"], player["hit_count"], player["flashbang_count"], player["smoke_count"], player["he_count"], player["molotov_count"], player["incendiary_count"], player["decoy_count"], player["round_count"], "ct", dt])
        
    for player in thisGame["team_t"]["team_players"]:
        playersList.append([player["steamid"], player["name"], player["kill_count"], player["score"], player["tk_count"], player["assist_count"], player["death_count"], player["5k_count"], player["4k_count"], player["3k_count"], player["2k_count"], player["1k_count"], player["hs_count"], player["kd"], player["esea_rws"], player["shot_count"], player["hit_count"], player["flashbang_count"], player["smoke_count"], player["he_count"], player["molotov_count"], player["incendiary_count"], player["decoy_count"], player["round_count"], "t", dt])
    
    #Return the code, and the list
    return [jsonInputFormat[0], playersList]

###############################################################
##### New function to allow for multithreading procedures #####
###############################################################


#This function downloads a game code
def downloadDems(code):
    #Keep originalDir in case of adding new
    originalDir = os.getcwd()
    os.chdir("demoDownloads")
    if code not in os.listdir():
        os.mkdir(code)
        os.chdir(code)
    else:
        os.chdir(code)
    #Here we have a new directory with the name of the code, inside we want to just download the game
    try:
        os.system("echo [DOWNLOADING] {} >> autoLOG.txt".format(code))
        os.system("csgodm download {} --output {}".format(code, os.getcwd()))
    except Exception as e:
        os.system("echo [EXCEPTION] {} >> autoLOG.txt".format(e))
    os.chdir(originalDir)
    return


#New analyzeDem function... Outputs the same code and returnParse function but is able to be done with multiprocessing
#Returns none if there is a weird error...
def analyzeDem(code):
    os.system("echo [ANALYZE] {} >> autoLOG.txt".format(code))
    originalDir = os.getcwd()
    os.chdir("demoDownloads")
    returnParse = None
    if len(os.listdir(os.path.join(os.getcwd(), code))) == 2:
        subprocess.call(["csgodm", "json", os.path.join(os.getcwd(), code), "--output", os.path.join(os.getcwd(), code), "--force-analyze"])
    if len(os.listdir(os.path.join(os.getcwd(), code))) == 3:
        for file in os.listdir(os.path.join(os.getcwd(), code)):
            if file.split('.')[-1] == 'json':
                w = open(os.path.join(os.path.join(os.getcwd(), code), file), "r", encoding = 'utf-8')
                info = json.loads(w.read())
                w.close()
                returnParse = returnGameInfo([code, info])
                os.system("rmdir {}".format(os.path.join(os.path.join(os.getcwd(), code))))
    os.chdir(originalDir)
    if returnParse:
        return returnParse
    return

