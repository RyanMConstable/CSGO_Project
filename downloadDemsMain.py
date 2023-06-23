import findMatchSteamAPI as API
import CSGOsql, getJSONInfo, os, time
#1) Given a userid, and steamkey, find that users new list of codes
#2) Generate every users new games
#3) Update the users recentgamecode with the newest game code
#4) Check the list 

if __name__ == '__main__':
    #Update function for new users
    CSGOsql.updateNewGames()
    os.system("echo [INFO] Ending updateNewGames >> autoLOG.txt")

    #Variable to track amount of time
    startTime = time.time()

    #Set variables early so time isn't wasted in the loop
    codesIngamecodes = CSGOsql.findAllCodes()
    codesInGamestats = CSGOsql.findAllCodesInStats()

    #For every user in the user db, find the new codes and then download new ones
    for user in CSGOsql.findAllid():
        os.system("echo [INFO] User: {} >> autoLOG.txt".format(str(user[0])))
        updateList = API.generateNewCodes(user[0], user[1])
        updateList = ['CSGO-65zTr-n7ATe-MsdXS-PDo78-DBF4C', 'CSGO-ZvdK8-iqdX7-V4BvA-EBQfh-GusnC']
        
        #If there are new codes update the recentgame code and download the demo
        if any(updateList):
            os.system("echo [INFO] Updating: {} >> autoLOG.txt".format(str(updateList)))
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
            os.system("echo [INFO] Already up to date >> autoLOG.txt")
            continue
    
    
    #Call analyze
    os.system("echo [CALL] Starting Analyze File >> autoLOG.txt")
    #os.system("python {}".format(os.path.join(os.getcwd(), "analyzeDemsMain.py")))
    os.system("echo [CALL] Ending Analyze File >> autoLOG.txt")
    
    #Prints the amount of time to download all the user files     
    totalTime = time.time()-startTime
    os.system("echo [EXIT] Exiting after: {} >> autoLOG.txt".format(f'Time: {totalTime:.2f} sec'))
    
    
    exit(0)