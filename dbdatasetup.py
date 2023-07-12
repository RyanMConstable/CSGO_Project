import CSGOsql
import getJSONInfo


#This function populates the gamestats table using all game codes from the gamecodes table
#This should only be used in a testing environment
def populateStats():
    codeList = CSGOsql.returnAllCodes()
    for code in codeList:
        #Check if code is in gamestats already, if not skip
        if CSGOsql.inGameStats(code):
            gameInfo = getJSONInfo.returnGameInfo(getJSONInfo.getJSONInfo(code))
            if gameInfo == None:
                continue
            CSGOsql.addGameStats(gameInfo)
    return