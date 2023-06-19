import findMatchSteamAPI as API
import CSGOsql, getJSONInfo, os, time
#1) Given a userid, and steamkey, find that users new list of codes
#2) Generate every users new games
#3) Update the users recentgamecode with the newest game code
#4) Check the list 


#Update function for new users
CSGOsql.updateNewGames()
print("Ending updateNewGames\n")


#Set variables early so time isn't wasted in the loop
codesIngamecodes = CSGOsql.findAllCodes
codesInGamestats = CSGOsql.findAllCodesInStats

#For every user in the user db, find the new codes and then download new ones
for user in CSGOsql.findAllid():
    updateList = API.generateNewCodes(user[0], user[1])
    
    #Set new update
    if len(updateList) > 1:
        CSGOsql.newRecentGame(user[0], updateList[-1])
    else:
        print("Already up to date\n")
        continue
    
    if any(updateList):
        for code in updateList:
            #Checks to see if the code is in the database
            if (code in codesIngamecodes and code in codesInGamestats):
                continue
            #Checks to see if code is already in the directory folder
            if (code in os.listdir(os.path.join(os.getcwd(), 'demoDownloads'))):
                continue
            getJSONInfo.downloadDems(code)
            

