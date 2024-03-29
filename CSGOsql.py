import os, dbconnection, getJSONInfo, findMatchSteamAPI


##################################################
################# HELPER FUNCTIONS ###############
##################################################

#Gets the id of the game from gamecodes that the code corresponds to
def findGameCodeID(gameCode):
    query = F"SELECT id FROM gamecodes WHERE code = '{gameCode}'"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None:
        return None
    return result[0][0]



##################################################
##################################################
##################################################



################################################################################
################    IMPORTANT ADD TO DB FUNCTIONS                   ############
################################################################################



#This function adds a list of gamecodes to the gamecodes tables
def addGameCodes(codes):
    for singleCode in codes:
        try:
            newquery = "INSERT INTO gamecodes (code) VALUES (%s)"
            val = ([singleCode])
            dbconnection.executeQuery(dbconnection.createConnection(), newquery, True, val)
        except Exception as e:
            pass
    return



#input in the form of a list [matchCode, statsOfGame]
#Adds to the gamestats table
def addGameStats(playerStats):
    gameid = findGameCodeID(playerStats[0])
    if gameid == [] or gameid == None:
        return "Not in match table?"
    result = gameid
    
    for player in playerStats[1]:
        query = F"SELECT * FROM gamestats WHERE gameid = '{result}' AND steamid = '{player[0]}'"
        newresult = dbconnection.executeQuery(dbconnection.createConnection(), query)
        if newresult == [] or newresult == None:
            newquery = "INSERT INTO gamestats (gameid, steamid, name, totalkills, score, tk_count, assist, deaths, 5k, 4k, 3k, 2k, 1k, headshot, kd, rws, shot_count, hit_count, flashbang_thrown, smoke_thrown, he_thrown, molly_thrown, incendiary_thrown, decoy_thrown, round_count, team, date, adr, clutches, clutch_won_count, clutch_loss_count, entry_kill_won_count, entry_kill_loss_count, entry_hold_kill_won_count, entry_hold_kill_loss_count, rank_old, rank_new, total_health_damage, total_armor_damage, total_health_damage_taken, total_armor_damage_taken, kill_per_round, assist_per_round, death_per_round, total_time_death, avg_time_death, 1v1_won_count, 1v2_won_count, 1v3_won_count, 1v4_won_count, 1v5_won_count, 1v1_loss_count, 1v2_loss_count, 1v3_loss_count, 1v4_loss_count, 1v5_loss_count, 1v1_count, 1v2_count, 1v3_count, 1v4_count, 1v5_count, killsonround, team_damage, teamflashcount, enemyflashcount, teamflashduration, enemyflashduration, uniquemsgs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            player.insert(0, result)
            val = (player)
            dbconnection.executeQuery(dbconnection.createConnection(), newquery, True, val)
    return

#Input in the same form as gamestats, adds to gameinfo table
def addGameInfo(gameInfo):
    gameid = findGameCodeID(gameInfo[0])
    if gameid == [] or gameid == None:
        return "Not in match table?"
    result = gameid
    
    query = F"SELECT * FROM gameinfo WHERE id = '{result}'"
    newresult = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if newresult == [] or newresult == None:
        newquery = "INSERT INTO gameinfo (id, duration, map_name, score_team1, score_team2, score_half1_team1, score_half1_team2, score_half2_team1, score_half2_team2, team_surrender, team_winner, most_killing_weapon, most_damaging_weapon, overtimes, kill_count, clutch_count, trade_kill_count, flashbang_thrown_count, smoke_thrown_count, he_thrown_count, decoy_thrown_count, molotov_thrown_count, incendiary_thrown_count, damage_health_count, damage_armor_count, jump_kill_count, crouch_kill_count, headshot_count, death_count, assist_count, entry_kill_count, knife_kill_count, teamkill_count, clutch_lost_count, clutch_won_count, shot_count, hit_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        gameInfo[2].insert(0, result)
        val = (gameInfo[2])
        dbconnection.executeQuery(dbconnection.createConnection(), newquery, True, val)
    return



#Adds to the discorduser table, this is now called through the flask website
def newUser(discordUser, steamid, steamidkey, gamecode):
    newRecentGame(steamid, gamecode)
    
    if findMatchSteamAPI.trueValidation(steamid, steamidkey, gamecode) == False:
        return "Invalid steam id"
    
    query = F"SELECT * FROM discorduser WHERE discordname = {discordUser}"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    
    
    if result is None or result == []:
        newquery = "INSERT INTO discorduser (discordname, steamid, steamidkey, gamecode) VALUES (%s, %s, %s, %s)"
        result = dbconnection.executeQuery(dbconnection.createConnection(), newquery, True, (discordUser, steamid, steamidkey, gamecode))
    else:
        newquery = F"UPDATE discorduser SET discordname = '{discordUser}', steamidkey = '{steamidkey}', gamecode = '{gamecode}'  WHERE steamid = {steamid}"
        dbconnection.executeQuery(dbconnection.createConnection(), newquery, True)
    return

#Function to add to set the gamecode in discorduser
def newRecentGame(steamid, code):
    query = F"UPDATE discorduser SET gamecode = '{code}' WHERE steamid = '{steamid}'"
    dbconnection.executeQuery(dbconnection.createConnection(), query, True)
    return

##################################################################################
#################     END OF ADD FUNCTIONS              ##########################
##################################################################################



##################################################################################
#################     GAMECODE INTERACTIONS             ##########################
##################################################################################

#This function returns all the codes in the first table
def returnAllCodes():
    query = "SELECT code from gamecodes"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result == None or result == []:
        return None
    
    for i in range(0, len(result)):
        result[i] = result[i][0]
    return result


##################################################################################
#################     END OF GAMECODE FUNCTIONS         ##########################
##################################################################################








##################################################################################
#################             STAT QUERIES              ##########################
##################################################################################





####### FUNCTIONS TO FIND THE HIGHEST X AMOUNT ON A GIVEN CATEGORY #########

#Removed upper limit, may have to change if weird things happen
def findTopX(category, limit):
    if int(limit) < 1:
        print("1 <= num")
        return
    query = F"SELECT name, {category} FROM gamestats ORDER BY {category} DESC LIMIT {limit}"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result

#Find top X for a specific user with a query
#Returns only the list of numbers from each game
def findTopUser(category, userid, limit):
    query = F"SELECT {category} FROM gamestats WHERE steamid = {userid} ORDER BY {category} DESC LIMIT {limit}"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result

#function to find the top 1 user
def findTop1user(category, userid):
    query = F"SELECT name, {category} FROM gamestats WHERE steamid = {userid} ORDER BY {category} DESC LIMIT 1"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result[0][1]


#Function to find user and stat, used for leaderboard, the highest users
def finduserandstat(category):
    query = F"SELECT name, {category} FROM gamestats ORDER BY {category} DESC LIMIT 1"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return str(result[0][0]) + ": " + str(result[0][1])
#####################################################################




#Very useful stat function, type in the column name of the database, and the steam id and it will return the sum of that column
def selectCombinedUserStat(stat, steamid):
    query = F"SELECT SUM({stat}) FROM gamestats WHERE steamid = '{steamid}'"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result[0][0]


#Very useful stat function, type in the column name of the database, and the steam id and it will return the avg of that column
def selectAvgUserStat(stat, steamid, limiter):
    query = F"SELECT AVG({stat}) FROM (SELECT {stat} FROM gamestats WHERE steamid = '{steamid}' ORDER BY date DESC LIMIT {limiter}) as test"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result[0][0]

#Very useful stat function, type in the column name of the database, and the steam id and it will return the sum of that column
def selectSumUserStat(stat, steamid, limiter):
    query = F"SELECT SUM({stat}) FROM (SELECT {stat} FROM gamestats WHERE steamid = '{steamid}' ORDER BY date DESC LIMIT {limiter}) as test"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result[0][0]


#Function to find how many games the user has within the table
def findNumberOfGames(steamid):
    query = F"SELECT COUNT(*) FROM gamestats WHERE steamid = '{steamid}'"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result[0][0]


#Function to find all rows for a given user in the table
def returnAllUserRows(steamid):
    query = F"SELECT name, totalkills, score, tk_count, assist, deaths, 5k, 4k, 3k, 2k, 1k, headshot, kd, rws, shot_count, hit_count, flashbang_thrown, smoke_thrown, he_thrown, incendiary_thrown, decoy_thrown, round_count FROM gamestats WHERE steamid = '{steamid}'"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result


#Function to find the bottom X Users
def findBottom(category, limit):
    query = F"SELECT name, {category} FROM gamestats WHERE {category} > 0.0 ORDER BY {category} ASC LIMIT {limit}"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result



#Function to find highest X game stats
def findGameStats(steamID, category, ORDER, gamecode = None):
    selection = "totalkills, score, tk_count, assist, deaths, 5k, 4k, 3k, 2k, 1k, headshot, kd, rws, shot_count, hit_count, flashbang_thrown, he_thrown, molly_thrown"
    selection += ", incendiary_thrown, decoy_thrown, round_count, date, adr, clutches, clutch_won_count, clutch_loss_count, entry_kill_won_count, entry_kill_loss_count"
    selection += ", entry_hold_kill_won_count, entry_hold_kill_loss_count, rank_old, rank_new, total_health_damage, total_armor_damage, total_health_damage_taken, "
    selection += "total_armor_damage_taken, kill_per_round, assist_per_round, death_per_round, total_time_death, avg_time_death, 1v1_won_count, 1v2_won_count, "
    selection += "1v3_won_count, 1v4_won_count, 1v5_won_count, 1v1_loss_count, 1v2_loss_count, 1v3_loss_count, 1v4_loss_count, 1v5_loss_count, 1v1_count, 1v2_count, "
    selection += "1v3_count, 1v4_count, 1v5_count, killsonround"
    query = ""
    if gamecode == None:
        query = F"SELECT {selection} FROM gamestats WHERE steamid = '{steamID}' ORDER BY {category} {ORDER} LIMIT 1"
    elif findGameCodeID(gamecode) != None:
        query = F"SELECT {selection} FROM gamestats WHERE gameid = {findGameCodeID(gamecode)} AND steamid = '{steamID}'"
    
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result == [] or result == None:
        return
    return result


#Function to find the position a player is in given id, category, and reverse order
def findPos(steamID, category, ORDER = 'DESC'):
    query = F"SELECT Position FROM (SELECT ROW_NUMBER() OVER(ORDER BY {category} {ORDER}) AS Position"
    query += F", steamid, name, totalkills FROM csgochadtable.gamestats) as sortedInfo WHERE steamid = '{steamID}' limit 1"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result != [] and result != None:
        return result[0][0]
    return


#Return number of rows in gamestats
def findNumStats():
    query = "SELECT COUNT(*) FROM gamestats"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result != [] and result != None:
        return result[0][0]
    return


#find all users info
def findGameInfo(gameid = None):
    if gameid == None:
        query = "SELECT gameid FROM gamestats ORDER BY gameid DESC LIMIT 1"
        result = dbconnection.executeQuery(dbconnection.createConnection(), query)
        if result == [] or result == None:
            return
        gameid = result[0][0]
    #Here we want to find all the game info
    query = F"SELECT name, adr, team_damage, tk_count, teamflashcount, enemyflashcount, teamflashduration, enemyflashduration, uniquemsgs FROM gamestats WHERE gameid = {gameid}"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    return result

##################################################################################
#################     END OF STAT FUNCTIONS             ##########################
##################################################################################






##################################################################################
#################     RANDOM QUERY FUNCTIONS            ##########################
##################################################################################

#Finds a steamid from a discorduser
def findSteamID(discordUser):
    query = F"SELECT steamid, steamidkey FROM discorduser WHERE discordname = {discordUser}"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return [result[0][0], result[0][1]]


#Check if a given game is in the gamestats table
#returns boolean True if the game is in the table, otherwise Falses
def inGameStats(code):
    #Part 1 check code is in first database
    result = findGameCodeID(code)
    if result is None or result == []:
        return False
    
    query = F"SELECT * FROM gamestats WHERE gameid = {result}"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return False
    return True


#Returns dictionary of game codes in gamecodes
def findAllCodes():
    query = "SELECT code FROM gamecodes"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    #Create a dictionary here
    codeDict = {}
    if any(result):
        for code in result:
            if code[0] not in codeDict:
                codeDict[code[0]] = True
    return codeDict

#Returns dictionary of game codes in gamestats
def findAllCodesInStats():
    #Now we want to find these game codes
    query = "SELECT code FROM gamecodes WHERE id IN (SELECT DISTINCT gameid FROM gamestats)"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    #Create a dictionary here
    codeDict = {}
    if any(result):
        for code in result:
            if code[0] not in codeDict:
                codeDict[code[0]] = True
    return codeDict

#Returns dictionary of game codes in gameinfo
def findAllCodesIngameinfo():
    query = "SELECT code FROM gamecodes WHERE id IN (SELECT id FROM gameinfo)"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    codeDict = {}
    if any(result):
        for code in result:
            if code[0] not in codeDict:
                codeDict[code[0]] = True
    return codeDict

#Returns list of steamid and steamidkeys
def findAllid():
    query = "SELECT steamid, steamidkey FROM discorduser"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result


#New function to find a users steamid from a name
def findSteamID2(name):
    query = F"SELECT steamid FROM gamestats WHERE name = '{name}' ORDER BY date DESC LIMIT 1"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if any(result):
        return result[0][0]
    return


#Find a discordid from a steamuser
def findDiscordID(steamid):
    query = F"SELECT discordname FROM discorduser WHERE steamid = '{steamid}'"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if any(result):
        return result[0][0]
    return

##################################################################################
#################     END OF RANDOM FUNCTIONS           ##########################
##################################################################################




##################################################################################
#################     STATS FOR GAME INFO               ##########################
##################################################################################
def findGameInfoLastGame():
    query = F"SELECT * FROM gameinfo ORDER BY id DESC LIMIT 1"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if any(result):
        return result[0]
    return