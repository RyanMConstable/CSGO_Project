import dbconnection

#This function takes in a steamid and returns the most recent match code from the discorduser table
def findMostRecentGame(userid):
    query = "SELECT gamecode FROM discorduser WHERE steamid = '{}'".format(userid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if any(result):
        return result[0][0]
    return