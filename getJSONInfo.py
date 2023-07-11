import os, json, subprocess


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
    
    
    #Set date of game played
    dt = thisGame["date"]
    
    #Loop for every player on team_ct, add parsed data (obnoxiously long)
    for player in thisGame["team_ct"]["team_players"]:
        thisPlayer = []
        thisPlayer.append(player["steamid"])
        thisPlayer.append(player["name"])
        thisPlayer.append(player["kill_count"])
        thisPlayer.append(player["score"])
        thisPlayer.append(player["tk_count"])
        thisPlayer.append(player["assist_count"])
        thisPlayer.append(player["death_count"])
        thisPlayer.append(player["5k_count"])
        thisPlayer.append(player["4k_count"])
        thisPlayer.append(player["3k_count"])
        thisPlayer.append(player["2k_count"])
        thisPlayer.append(player["1k_count"])
        thisPlayer.append(player["hs_count"])
        thisPlayer.append(player["kd"])
        thisPlayer.append(player["esea_rws"])
        thisPlayer.append(player["shot_count"])
        thisPlayer.append(player["hit_count"])
        thisPlayer.append(player["flashbang_count"])
        thisPlayer.append(player["smoke_count"])
        thisPlayer.append(player["he_count"])
        thisPlayer.append(player["molotov_count"])
        thisPlayer.append(player["incendiary_count"])
        thisPlayer.append(player["decoy_count"])
        thisPlayer.append(player["round_count"])
        thisPlayer.append("ct")
        thisPlayer.append(dt)
        thisPlayer.append(player['average_health_damage'])
        thisPlayer.append(player['clutch_count'])
        thisPlayer.append(player['clutch_won_count'])
        thisPlayer.append(player['clutch_loss_count'])
        thisPlayer.append(player['entry_kill_won_count'])
        thisPlayer.append(player['entry_kill_loss_count'])
        thisPlayer.append(player['entry_hold_kill_won_count'])
        thisPlayer.append(player['entry_hold_kill_loss_count'])
        thisPlayer.append(player['rank_old'])
        thisPlayer.append(player['rank_new'])
        thisPlayer.append(player['total_damage_health_done'])
        thisPlayer.append(player['total_damage_armor_done'])
        thisPlayer.append(player['total_damage_health_received'])
        thisPlayer.append(player['total_damage_armor_received'])
        thisPlayer.append(player['kill_per_round'])
        thisPlayer.append(player['assist_per_round'])
        thisPlayer.append(player['death_per_round'])
        thisPlayer.append(player['total_time_death'])
        thisPlayer.append(player['avg_time_death'])
        thisPlayer.append(player['1v1_won_count'])
        thisPlayer.append(player['1v2_won_count'])
        thisPlayer.append(player['1v3_won_count'])
        thisPlayer.append(player['1v4_won_count'])
        thisPlayer.append(player['1v5_won_count'])
        thisPlayer.append(player['1v1_loss_count'])
        thisPlayer.append(player['1v2_loss_count'])
        thisPlayer.append(player['1v3_loss_count'])
        thisPlayer.append(player['1v4_loss_count'])
        thisPlayer.append(player['1v5_loss_count'])
        thisPlayer.append(player['1v1_count'])
        thisPlayer.append(player['1v2_count'])
        thisPlayer.append(player['1v3_count'])
        thisPlayer.append(player['1v4_count'])
        thisPlayer.append(player['1v5_count'])
        playersList.append(thisPlayer)
        
    for player in thisGame["team_t"]["team_players"]:
        thisPlayer = []
        thisPlayer.append(player["steamid"])
        thisPlayer.append(player["name"])
        thisPlayer.append(player["kill_count"])
        thisPlayer.append(player["score"])
        thisPlayer.append(player["tk_count"])
        thisPlayer.append(player["assist_count"])
        thisPlayer.append(player["death_count"])
        thisPlayer.append(player["5k_count"])
        thisPlayer.append(player["4k_count"])
        thisPlayer.append(player["3k_count"])
        thisPlayer.append(player["2k_count"])
        thisPlayer.append(player["1k_count"])
        thisPlayer.append(player["hs_count"])
        thisPlayer.append(player["kd"])
        thisPlayer.append(player["esea_rws"])
        thisPlayer.append(player["shot_count"])
        thisPlayer.append(player["hit_count"])
        thisPlayer.append(player["flashbang_count"])
        thisPlayer.append(player["smoke_count"])
        thisPlayer.append(player["he_count"])
        thisPlayer.append(player["molotov_count"])
        thisPlayer.append(player["incendiary_count"])
        thisPlayer.append(player["decoy_count"])
        thisPlayer.append(player["round_count"])
        thisPlayer.append("t")
        thisPlayer.append(dt)
        thisPlayer.append(player['average_health_damage'])
        thisPlayer.append(player['clutch_count'])
        thisPlayer.append(player['clutch_won_count'])
        thisPlayer.append(player['clutch_loss_count'])
        thisPlayer.append(player['entry_kill_won_count'])
        thisPlayer.append(player['entry_kill_loss_count'])
        thisPlayer.append(player['entry_hold_kill_won_count'])
        thisPlayer.append(player['entry_hold_kill_loss_count'])
        thisPlayer.append(player['rank_old'])
        thisPlayer.append(player['rank_new'])
        thisPlayer.append(player['total_damage_health_done'])
        thisPlayer.append(player['total_damage_armor_done'])
        thisPlayer.append(player['total_damage_health_received'])
        thisPlayer.append(player['total_damage_armor_received'])
        thisPlayer.append(player['kill_per_round'])
        thisPlayer.append(player['assist_per_round'])
        thisPlayer.append(player['death_per_round'])
        thisPlayer.append(player['total_time_death'])
        thisPlayer.append(player['avg_time_death'])
        thisPlayer.append(player['1v1_won_count'])
        thisPlayer.append(player['1v2_won_count'])
        thisPlayer.append(player['1v3_won_count'])
        thisPlayer.append(player['1v4_won_count'])
        thisPlayer.append(player['1v5_won_count'])
        thisPlayer.append(player['1v1_loss_count'])
        thisPlayer.append(player['1v2_loss_count'])
        thisPlayer.append(player['1v3_loss_count'])
        thisPlayer.append(player['1v4_loss_count'])
        thisPlayer.append(player['1v5_loss_count'])
        thisPlayer.append(player['1v1_count'])
        thisPlayer.append(player['1v2_count'])
        thisPlayer.append(player['1v3_count'])
        thisPlayer.append(player['1v4_count'])
        thisPlayer.append(player['1v5_count'])
        playersList.append(thisPlayer)
    #Return the code, and the list
    return [jsonInputFormat[0], playersList]

###############################################################
##### New function to allow for multithreading procedures #####
###############################################################


#This function downloads a game code, only if the game is not in the folder already
def downloadDems(code):
    #Keep originalDir in case of adding new
    downloadDir = os.path.join(os.getcwd(), 'demoDownloads')
    downloadCodeDir = os.path.join(downloadDir, code)
    if code not in os.listdir(downloadDir):
        os.mkdir(downloadCodeDir)
        #Here we have a new directory with the name of the code, inside we want to just download the game
        try:
            subprocess.call(["csgodm", "download", code, "--output", downloadCodeDir, ">>" , "downloadLOG.txt"])
        except Exception as e:
            os.system("echo [EXCEPTION] downloadDems {} >> autoLOG.txt".format(e))
        #Check to see if any files were downloaded, if not, delete the directory
        if len(os.listdir(downloadCodeDir)) == 0:
            try:
                os.system("rd /s /q {}".format(downloadCodeDir))
            except Exception as e:
                os.system("echo [EXCEPTION] downloadDems 'rd /s /q' {} >> autoLOG.txt".format(e))
    return


#New analyzeDem function... Outputs the same code and returnParse function but is able to be done with multiprocessing
#Returns none if there is a weird error...
def analyzeDem(code):
    downloadDir = os.path.join(os.getcwd(), 'demoDownloads')
    codeDir = os.path.join(downloadDir, code)
    returnParse = None
    if len(os.listdir(codeDir)) == 0:
        return []
    if len(os.listdir(codeDir)) == 2:
        try:
            subprocess.call(["csgodm", "json", codeDir, "--output", codeDir, "--force-analyze", ">>", "analyzeLOG.txt"])
        except Exception as e:
            os.system("echo [EXCEPTION] analyzeDem {} >> autoLOG.txt".format(e))
    if len(os.listdir(codeDir)) == 3:
        try:
            for file in os.listdir(codeDir):
                if file.split('.')[-1] == 'json':
                    w = open(os.path.join(codeDir, file), "r", encoding = 'utf-8')
                    info = json.loads(w.read())
                    w.close()
                    returnParse = returnGameInfo([code, info])
        except Exception as e:
            os.system("echo [EXCEPTION] anaylzeDem CODE: 2 {} >> autoLOG.txt".format(e))
    if returnParse:
        return returnParse
    return

