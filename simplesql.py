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