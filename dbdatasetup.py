import CSGOsql
import getJSONInfo


#Need a function to populate the second table with game information from all games in the first table
def populateStats():
    codeList = CSGOsql.returnAllCodes()
    for code in codeList:
        gameInfo = getJSONInfo.returnGameInfo(getJSONInfo.getJSONInfo(code))
        if gameInfo == None:
            continue
        CSGOsql.addGameStats(gameInfo)
    return