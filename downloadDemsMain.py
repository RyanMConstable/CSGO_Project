import findMatchSteamAPI as API
import CSGOsql, getJSONInfo, os, time
#1) Given a userid, and steamkey, find that users new list of codes
#2) Generate every users new games
#3) Update the users recentgamecode with the newest game code
#4) Check the list 

if __name__ == '__main__':
    #Update function for new users
    CSGOsql.updateNewGames()

    #Variable to track amount of time
    startTime = time.time()

    #Set variables early so time isn't wasted in the loop
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
                if (code in os.listdir(os.path.join(os.getcwd(), 'demoDownloads'))):
                    continue
                getJSONInfo.downloadDems(code)
        else:
            continue
    
    
    #Call analyze
    #os.system("echo [CALL] Starting Analyze File >> autoLOG.txt")
    os.system("python {}".format(os.path.join(os.getcwd(), "analyzeDemsMain.py")))
    #os.system("echo [CALL] Ending Analyze File >> autoLOG.txt")
    
    #Prints the amount of time to download all the user files   
    totalTime = time.time()-startTime
    #os.system("echo [EXIT] Exiting after: {} >> autoLOG.txt".format(f'Time: {totalTime:.2f} sec'))
    
    
    exit(0)