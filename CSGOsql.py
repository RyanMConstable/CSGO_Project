#For importing exceptions...
try:
    import dbconnection, getJSONInfo, findMatchSteamAPI
except Exception as e:
    from . import dbconnection, getJSONInfo, findMatchSteamAPI


#This function adds a list of gamecodes to the database
#No duplicates
def addGameCodes(codes):
    #The following line creates a connection to the database
    #dbconnection.createConnection()
    for singleCode in codes:
        try:
            newquery = "INSERT INTO gamecodes (code) VALUES (%s)"
            val = ([singleCode])
            dbconnection.executeQuery(dbconnection.createConnection(), newquery, True, val)
        except Exception as e:
            #print("Error in addGameCodes: " + str(e))
            pass
    return



#input in the form of a list [matchCode, statsOfGame]
def addGameStats(playerStats):
    #Takes the id from the first table and stores in result
    query = "SELECT id FROM gamecodes WHERE code = '{}'".format(playerStats[0])
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result == []:
        return "Not in match table?"
    result = result[0][0]
    
    for player in playerStats[1]:
        query = "SELECT * FROM gamestats WHERE gameid = '{}' AND steamid = '{}'".format(result, player[0])
        newresult = dbconnection.executeQuery(dbconnection.createConnection(), query)
        if newresult == [] or newresult == None:
            #Insert the player into the new database
            newquery = "INSERT INTO gamestats (gameid, steamid, name, totalkills, score, tk_count, assist, deaths, 5k, 4k, 3k, 2k, 1k, headshot, kd, rws, shot_count, hit_count, flashbang_thrown, smoke_thrown, he_thrown, molly_thrown, incendiary_thrown, decoy_thrown, round_count, team, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            player.insert(0, result)
            val = (player)
            dbconnection.executeQuery(dbconnection.createConnection(), newquery, True, val)
    return


#This function returns all the codes in the first table
def returnAllCodes():
    query = "SELECT code from gamecodes"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result == None or result == []:
        return None
    
    #Fix the weird SQL format, probably a better and more efficient way to do (TODO)
    for i in range(0, len(result)):
        result[i] = result[i][0]
    return result

#This function takes in a steamid and returns the most recent match code from the table
def findMostRecentGame(userid):
    #This is the SQL query to find the most recent game id
    query = "SELECT gameid from gamestats WHERE steamid = {} order by date DESC limit 1".format(userid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    gameid = result[0][0]
    
    #Now we use the gameid to find the matchcode from the first table
    query = "SELECT code from gamecodes WHERE id = {}".format(gameid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    #Returns match code of the most recent game
    return result[0][0]


#This function will find all of the game codes that are in the first table but not the second 
#Then it will have those codes as a list and then populate the second table with them
def populateSecondTableFromFirst():
    query = "SELECT code from gamecodes WHERE code NOT IN (SELECT code FROM gamecodes WHERE id IN (SELECT gameid FROM gamestats))"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    for code in result:
        try:
            addGameStats(getJSONInfo.returnGameInfo(getJSONInfo.getJSONInfo(code[0])))
        except:
            continue
    return


#Find top X amount for a category with a query
def findTopX(category, num):
    if int(num) < 0 or int(num) > 100:
        return "Number must be between 0 and 100"
    
    query = "SELECT name, {} FROM gamestats ORDER BY {} DESC LIMIT {}".format(category, category, num)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    formatResult = ""
    for row in result:
        formatResult += row[0]
        formatResult += " "
        formatResult += str(row[1])
        formatResult += '\n'
    return formatResult

#Find top X for a specific user with a query
def findTop10user(category, userid, limit):
    query = "SELECT name, {} FROM gamestats WHERE steamid = {} ORDER BY {} DESC LIMIT {}".format(category, userid, category, limit)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    formatResult = ""
    for row in result:
        formatResult += row[0]
        formatResult += " "
        formatResult += str(row[1])
        formatResult += '\n'
    return formatResult


#Add the discorduser and steamid to the new table
def setDiscordUser(discordUser, steamid, steamidkey):
    #Here we want to validate the steamid, and steamidkey given
    if findMatchSteamAPI.validateUser(steamid, steamidkey) == False:
        return "Invalid steam id"
    
    query = "SELECT * FROM discorduser WHERE discordname = {}".format(discordUser)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    
    
    if result is None or result == []:
        print("Empty")
        newquery = "INSERT INTO discorduser (discordname, steamid, steamidkey) VALUES (%s, %s, %s)"
        result = dbconnection.executeQuery(dbconnection.createConnection(), newquery, True, (discordUser, steamid, steamidkey))
        print(result)
    else:
        print("User here, newid:" + str(steamid) + " newidkey:" + str(steamidkey))
        newquery = "UPDATE discorduser SET steamid = '{}', steamidkey = '{}' WHERE discordname = {}".format(steamid, steamidkey, discordUser)
        dbconnection.executeQuery(dbconnection.createConnection(), newquery, True)
    return


#Finds a steamid from a discorduser
def findSteamID(discordUser):
    query = "SELECT steamid, steamidkey FROM discorduser WHERE discordname = {}".format(discordUser)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return None
    return [result[0][0], result[0][1]]




################################### Below functions are for updating db ################################
#Might want to think about creating a new file to separate these...



#This function not only needs to add the games, but then update the most recent game in the recent game table
def updateGames(steamid, steamidkey):
    codes = findMatchSteamAPI.generateNewCodes(steamid, steamidkey)
    newRecentGame(steamid, codes[-1])
    codesToUpdate = []
    #Remove codes that are already in the database to save time
    for code in codes:
        try:
            query = "SELECT id from gamecodes WHERE code = '{}'".format(code)
            result = dbconnection.executeQuery(dbconnection.createConnection(), query)
            if result == []:
                codesToUpdate.append(code)
                continue
            query = "SELECT * from gamestats WHERE gameid = '{}'".format(result[0][0])
            result = dbconnection.executeQuery(dbconnection.createConnection(), query)
            if result == []:
                codesToUpdate.append(code)
        except Exception as e:
            print("Exception code remove: " + str(code))
            codesToUpdate.append(code)
    
    print("Original List:" + str(codes))
    print("Codes to update:" + str(codesToUpdate))    
    if codesToUpdate is None or codesToUpdate == []:
        print("Already updated...")
        return
    codes = codesToUpdate
    
    addGameCodes(codes)
    for code in codes:
        print("Attempting to add code: '{}'".format(code))
        try:
            addGameStats(getJSONInfo.returnGameInfo(getJSONInfo.getJSONInfo(code)))
            print("Successfully added game stats!")
        except Exception as e:
            print("Exception")
            print(e)
            continue
    return "Games Added"



#Update all users games...
def updateAllUsers():
    query = "SELECT steamid, steamidkey FROM discorduser"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return None
    #Here we want each id to call updategames
    for id in result:
        print("\n-------------------------------\nUpdating user:"+str(id[0])+"\n-------------------------------\n")
        updateGames(id[0], id[1])
    return "Complete!"



#Check if a given game is in the gamestats table
#returns boolean True if the game is in the table, otherwise Falses
def inGameStats(code):
    #Part 1 check code is in first database
    query = "SELECT id FROM gamecodes WHERE code = '{}'".format(code)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return False
    result = result[0][0]
    
    query = "SELECT * FROM gamestats WHERE gameid = {}".format(result)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return False
    return True


#Function to add to the recentgame table
def newRecentGame(steamid, code):
    query = "SELECT * FROM recentgame WHERE steamid = {}".format(steamid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        query = "INSERT INTO recentgame (steamid, code) VALUES (%s, %s)"
        result = dbconnection.executeQuery(dbconnection.createConnection(), query, True, (steamid, code))
    else:
        query = "UPDATE recentgame SET code = '{}' WHERE steamid = '{}'".format(code, steamid)
        result = dbconnection.executeQuery(dbconnection.createConnection(), query, True)
    return




#This function needs to be revamped... 
#SOURCE OF PROBLEM WITH MULTIPLE USERS DOWNLOADING SAME FILE

#Function to get every id from discorduser and check if they're in the the newestgame list
#If they're not use the oldest game to check first
def updateNewGames():
    #Get all steamids from the discorduser table
    query = "SELECT steamid FROM discorduser"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    
    #Check if the user id is in the recentgame table
    #If the id is not in the table, then we update the table
    listToUpdate = []
    for id in result:
        query = "SELECT steamid FROM recentgame WHERE steamid = '{}'".format(id[0])
        result = dbconnection.executeQuery(dbconnection.createConnection(), query)
        if result is None or result == []:
            listToUpdate.append(id[0])
            
    #Now for every user in listToUpdate, we update the recent game after searching the table
    for user in listToUpdate:
        #This query finds the oldest game from the given user in the table
        query = "SELECT gameid FROM gamestats WHERE steamid = '{}' ORDER BY date ASC LIMIT 1".format(user)
        result = dbconnection.executeQuery(dbconnection.createConnection(), query)
        
        #This finds the actual code
        if result is not None or result != []:
            query = "SELECT code FROM gamecodes WHERE id = '{}'".format(result[0][0])
            result = dbconnection.executeQuery(dbconnection.createConnection(), query)
            
            #This inserts the code into the recentgame
            if result is not None:
                query = "INSERT INTO recentgame (steamid, code) VALUES (%s, %s)"
                result = dbconnection.executeQuery(dbconnection.createConnection(), query, True, (user, result[0][0]))
        
    return



#Function to find all game codes in the first table to add to the second one
def addCodedbToStatdb():
    #Find id
    query = "SELECT id, code FROM gamecodes WHERE id NOT IN (SELECT gameid FROM gamestats) ORDER BY id DESC"
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    print(result)
    if result != []:
        for firstResult in result:
            try:
                addGameStats(getJSONInfo.returnGameInfo(getJSONInfo.getJSONInfo(firstResult[1])))
                print("Added: {}".format(firstResult[1]))
            except Exception as e:
                print("Exception, can't add: {}".format(firstResult[1]))
                print(e)
    return



############################################################################
#########################Finding Game Stats#################################
############################################################################

#Very useful stat function, type in the column name of the database, and the steam id and it will return the sum of that column
def selectCombinedUserStat(stat, steamid):
    query = "SELECT SUM({}) FROM gamestats WHERE steamid = '{}'".format(stat, steamid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result[0][0]


#Very useful stat function, type in the column name of the database, and the steam id and it will return the sum of that column
def selectAvgUserStat(stat, steamid):
    query = "SELECT AVG({}) FROM gamestats WHERE steamid = '{}'".format(stat, steamid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result[0][0]


#Function to find how many games the user has within the table
def findNumberOfGames(steamid):
    query = "SELECT COUNT(*) FROM gamestats WHERE steamid = '{}'".format(steamid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result[0][0]


#Function to find all rows for a given user in the table
def returnAllUserRows(steamid):
    query = "SELECT name, totalkills, score, tk_count, assist, deaths, 5k, 4k, 3k, 2k, 1k, headshot, kd, rws, shot_count, hit_count, flashbang_thrown, smoke_thrown, he_thrown, incendiary_thrown, decoy_thrown, round_count FROM gamestats WHERE steamid = '{}'".format(steamid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result



#Write a function to find all top categories for a user given an id
def findusertop(steamid):
    userStats = 'Your highest stats of all time:\n'
    userStats += 'Kills: ' + findTop10user('totalkills', steamid, 1).split(" ")[-1]
    userStats += 'Score: ' + findTop10user('score', steamid, 1).split(" ")[-1]
    userStats += 'Team kills: ' + findTop10user('tk_count', steamid, 1).split(" ")[-1]
    userStats += 'Assists: ' + findTop10user('assist', steamid, 1).split(" ")[-1]
    userStats += 'Deaths: ' + findTop10user('deaths', steamid, 1).split(" ")[-1]
    userStats += '5ks: ' + findTop10user('5k', steamid, 1).split(" ")[-1]
    userStats += '4ks: ' + findTop10user('4k', steamid, 1).split(" ")[-1]
    userStats += '3ks: ' + findTop10user('3k', steamid, 1).split(" ")[-1]
    userStats += '2ks: ' + findTop10user('2k', steamid, 1).split(" ")[-1]
    userStats += '1ks: ' + findTop10user('1k', steamid, 1).split(" ")[-1]
    userStats += 'Headshots: ' + findTop10user('headshot', steamid, 1).split(" ")[-1]
    userStats += 'KD: ' + findTop10user('kd', steamid, 1).split(" ")[-1]
    userStats += 'RWS: ' + findTop10user('rws', steamid, 1).split(" ")[-1]
    userStats += 'Shots Fired: ' + str(findTop10user('shot_count', steamid, 1)).split(" ")[-1]
    userStats += 'Hit Count: ' + str(findTop10user('hit_count', steamid, 1)).split(" ")[-1]
    return userStats

print(findusertop('76561198068939539'))