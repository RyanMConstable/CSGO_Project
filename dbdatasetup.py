import CSGOsql
import getJSONInfo


#This function populates the gamestats table using all game codes from the gamecodes table
def populateStats():
    codeList = CSGOsql.returnAllCodes()
    for code in codeList:
        #Check if code is in gamestats already, if not skip
        if CSGOsql.inGameStats(code):
            gameInfo = getJSONInfo.returnGameInfo(getJSONInfo.getJSONInfo(code))
            if gameInfo == None:
                print("Game info is empty")
                continue
            print("Adding stats")
            CSGOsql.addGameStats(gameInfo)
    return