import os, json, shutil, subprocess, threading
from multiprocessing import Pool

pathToCSGOreplays = os.environ['PATH_TO_CSGOREPLAYS']
pathToCSGOreplay = os.environ['PATH_TO_CSGOREPLAY']


#Takes a single game code as input, downloads the file, then analyzes the file and downloads a json
#Opens the json and loads the json into a variable (can be improved), then returns the variable and the game code in a list
def getJSONInfo(code):
    #First tidys up the code
    code = code.strip()
    #Downloads, the given game using the path to the CSGODM, logs it to log.txt
    os.system("csgodm download " + str(code) + " > log.txt")
    
    files = os.listdir(pathToCSGOreplays)
    pathToJSON = None
    info = None
    
    #For the files in the directory, find the demo file
    for file in files:
        if file.split(".")[-1] == "dem":
            print("Demo found")
            pathToJSON = "csgodm json " + os.path.join(pathToCSGOreplay, file)
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
    
    #Return the code, and the list
    return [jsonInputFormat[0], playersList]



#Deletes all files in the CSGO replays directory, returns nothing
#We want to keep the replays folder, but delete everything in it
def clearReplayDir():
    for file in os.listdir(pathToCSGOreplays):
        os.remove(os.path.join(pathToCSGOreplays, file))
    return


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
    subprocess.call(["csgodm", "download", code, "--output", os.getcwd()])
    os.chdir(originalDir)
    return


#New analyzeDem function... Outputs the same code and returnParse function but is able to be done with multiprocessing
def analyzeDem(code):
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
    os.chdir(originalDir)
    if returnParse:
        return [code, returnParse]
    return




if __name__ == '__main__':
    with Pool(len(os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))) as p:
        p.map(analyzeDem, os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))
        
        
#Saving call to analyze games
#subprocess.call(["csgodm", "json", os.getcwd(), "--output", os.getcwd(), "--force-analyze"])