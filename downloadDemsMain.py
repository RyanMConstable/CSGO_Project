import findMatchSteamAPI as API
import CSGOsql, getJSONInfo, os, subprocess
from loggingsetup import autolog
#1) Given a userid, and steamkey, find that users new list of codes
#2) Generate every users new games
#3) Update the users recentgamecode with the newest game code
#4) Check the list 

if __name__ == '__main__':
    
    #Update function for new users (IE users who have a row in the user table, but not the recentgame table)
    CSGOsql.updateNewGames()

    #Set variables early so time isn't wasted in the loop, these are all game codes that exist (there has to be a faster way to check this)
    codesIngamecodes = CSGOsql.findAllCodes()
    codesInGamestats = CSGOsql.findAllCodesInStats()

    ListToUpdate = []
    #For every user in the user db, find the new codes and then download new ones
    for user in CSGOsql.findAllid():
        #HERE WE SHOULD CHECK FOR NEWER GAME IN TABLE?
        updateList = API.generateNewCodes(user[0], user[1])
        if any(updateList):
            CSGOsql.newRecentGame(user[0], updateList[-1])
        for code in updateList:
            if code not in ListToUpdate:
                ListToUpdate.append(code)
        
    for code in os.listdir(os.path.join(os.getcwd(), 'demoDownloads')):
        if code not in ListToUpdate:
            ListToUpdate.append(code)
        
    #If there are new codes update the recentgame code and download the demo
    if any(ListToUpdate):
        os.system("echo [UPDATELIST] {} >> autoLOG.txt".format(ListToUpdate))
        for code in ListToUpdate:
            #Checks to see if the code is in the database
            if (code in codesIngamecodes and code in codesInGamestats):
                os.system("echo [DUPLICATE] Code: {} Already in gamecodes and gamestats >> autoLOG.txt".format(code))
                continue
            os.system("echo [DOWNLOADING] {} >> autoLOG.txt".format(code))
            getJSONInfo.downloadDems(code)
        
        
    #Uncomment the below line if you wish to redownload-analyze all files possible for more info
    #CSGOsql.redownload()
    

    #Call analyze only if there are directories in demoDownloads
    #Calls up to 10 times, if it calls more than twice there is most likely an issue (enable logging at that point)
    #os.system("echo [CALL] Starting Analyze File >> autoLOG.txt")
    subprocess.call(["python", os.path.join(os.getcwd(), "analyzeDemsMain.py")])
    #os.system("echo [CALL] Ending Analyze File >> autoLOG.txt")

    autolog.shutdown()
    exit(0)