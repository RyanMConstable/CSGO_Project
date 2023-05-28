import CSGOsql
import getJSONInfo
import time

#Need a function to populate the second table with game information from all games in the first table
def populateStats():
    codeList = CSGOsql.returnAllCodes()
    for code in codeList:
        gameInfo = getJSONInfo.returnGameInfo(getJSONInfo.getJSONInfo(code))
        if gameInfo == None:
            print("Game info is empty")
            continue
        print("Adding stats")
        CSGOsql.addGameStats(gameInfo)
    return