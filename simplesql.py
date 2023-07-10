import dbconnection

#This is where sub CSGOsql.py queries should be, where only dbconnection is needed

#This function takes in a steamid and returns the most recent match code from the table
def findMostRecentGame(userid):
    query = "SELECT code FROM recentgame WHERE steamid = '{}'".format(userid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if any(result):
        return result[0][0]
    return