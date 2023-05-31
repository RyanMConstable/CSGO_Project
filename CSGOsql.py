import dbconnection
#temp import below

#This function adds a list of gamecodes to the database
#No duplicates
def addGameCodes(codes):
    #The following line creates a connection to the database
    #dbconnection.createConnection()
    for singleCode in codes:
        query = "SELECT * FROM gamecodes WHERE code = '{}'".format(singleCode)
        result = dbconnection.executeQuery(dbconnection.createConnection(), query)
        if result:
            continue
        newquery = "INSERT INTO gamecodes (code) VALUES (%s)"
        val = ([singleCode])
        dbconnection.executeQuery(dbconnection.createConnection(), newquery, True, val)
    return



#Going to need a second function to add to the new stats table
#1 Query game code table to find the id of a specific match code
#2 If the code is in the table, use the id and then fill the new table with game stats information

#input in the form of a list [matchCode, statsOfGame]
def addGameStats(playerStats):
    #Takes the id from the first table and stores in result
    query = "SELECT id FROM gamecodes WHERE code = '{}'".format(playerStats[0])
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result == None or result == []:
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