import findMatchSteamAPI as API
import CSGOsql, getJSONInfo, os, subprocess
from loggingsetup import autologf
import time

if __name__ == '__main__':
    start = time.time()
    autolog = autologf()
    #Update function for new users (IE users who have a row in the user table, but not the recentgame table)
    

    #Set variables early so time isn't wasted in the loop, these are all game codes that exist (there has to be a faster way to check this) 
    #ALSO LOOK INTO THIS (TODO)
    codesIngamecodes = CSGOsql.findAllCodes()
    codesInGamestats = CSGOsql.findAllCodesInStats()

    ListToUpdate = []
    #For every user in the user db, find the new codes and then download new ones
    for user in CSGOsql.findAllid():
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
        autolog.info(F"[UPDATELIST {ListToUpdate}]")
        for code in ListToUpdate:
            #Checks to see if the code is in the database, if it is then it doesn't download it, otherwise it downloads it
            if (code in codesIngamecodes and code in codesInGamestats):
                autolog.info(F"[DUPLICATE] Code: {code} Already in gamecodes and gamestats")
                continue
            autolog.info(F"[DOWNLOADING] {code}")
            getJSONInfo.downloadDems(code)
        
    

    #Only call if there are files within demoDownloads
    if len(os.listdir(os.path.join("./", "demoDownloads"))) > 0:
        subprocess.call(["python", os.path.join(os.getcwd(), "analyzeDemsMain.py")])
    
    end = time.time()
    print(end-start)
    exit(0)