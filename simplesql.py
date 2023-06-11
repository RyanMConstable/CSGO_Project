try:
    import dbconnection
except:
    from . import dbconnection

#This function takes in a steamid and returns the most recent match code from the table
def findMostRecentGame(userid):
    query = "SELECT code FROM recentgame WHERE steamid = '{}'".format(userid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    gameid = result[0][0]
    return gameid
    
    
    #OLD CODE BELOW
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