import findMatchSteamAPI as API
import CSGOsql, getJSONInfo, os
#1) Given a userid, and steamkey, find that users new list of codes
#2) Generate every users new games
#3) Update the users recentgamecode with the newest game code
#4) Check the list 

if __name__ == '__main__':
    #Update function for new users (IE users who have a row in the user table, but not the recentgame table)
    CSGOsql.updateNewGames()

    #Set variables early so time isn't wasted in the loop, these are all game codes that exit (there has to be a faster way to check this)
    codesIngamecodes = CSGOsql.findAllCodes()
    codesInGamestats = CSGOsql.findAllCodesInStats()

    #For every user in the user db, find the new codes and then download new ones
    for user in CSGOsql.findAllid():
        updateList = API.generateNewCodes(user[0], user[1])
        
        #If there are new codes update the recentgame code and download the demo
        if any(updateList):
            CSGOsql.newRecentGame(user[0], updateList[-1])
            for code in updateList:
                #Checks to see if the code is in the database
                if (code in codesIngamecodes and code in codesInGamestats):
                    continue
                #Checks to see if code is already in the directory folder
                elif (code in os.listdir(os.path.join(os.getcwd(), 'demoDownloads'))):
                    continue
                getJSONInfo.downloadDems(code)
        else:
            continue
        
        
    #Uncomment the below line if you wish to redownload-analyze all files possible for more info
    #CSGOsql.redownload()
    
    count = 0
    #Call analyze only if there are directories in demoDownloads
    while any(os.listdir(os.path.join(os.getcwd(), 'demoDownloads'))) or count >= 10:
        #os.system("echo [CALL] Starting Analyze File >> autoLOG.txt")
        os.system("python {}".format(os.path.join(os.getcwd(), "analyzeDemsMain.py")))
        #os.system("echo [CALL] Ending Analyze File >> autoLOG.txt")
        count+=1
    
    if count == 10:
        os.system("echo [COUNT ERROR] Analyze loop reached 10... Directories in demo downloads aren't being removed >> autoLog.txt")
    exit(0)