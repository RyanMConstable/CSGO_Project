from multiprocessing import Pool
from datetime import datetime
import getJSONInfo, os, CSGOsql, time


#Run this script every 30 seconds or so to check for new games, increase if load increases
if __name__ == '__main__':
    os.system("echo [START] Starting at time: {} >> analyzeLOG.txt".format(datetime.now()))
    #Sets the number of processes it should run, max is 60 on windows, so the max will be set to 40 just in case
    processes = len(os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))
    if processes <= 0:
        os.system("echo [INFO] No demos in the demoDownloads directory >> analyzeLOG.txt")
        os.system("echo [EXIT] Exiting >> analyzeLOG.txt")
        exit(0)
    elif processes > 40:
        os.system("echo [INFO] Processes set to 40 >> analyzeLOG.txt".format())
        processes = 40
    else:
        os.system("echo [DIRECTORIES] {} >> analyzeLOG.txt".format(os.listdir(os.path.join(os.getcwd(), 'demoDownloads'))))
    
    
    #This way they are not called multiple times, increases speed of program
    gamesIngamecodes = CSGOsql.findAllCodes()
    gamesIngamestats = CSGOsql.findAllCodesInStats()
    
    #Multiprocesses demoDownloads to speed up analyzing
    os.system("echo [SET1] >> analyzeLOG.txt")
    with Pool(processes) as p:
        os.system("echo [SET2] >> analyzeLOG.txt")
        x = p.map(getJSONInfo.analyzeDem, os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))
        os.system("echo [SET3] >> analyzeLOG.txt")
        #X is going to be a list of the gamecode at index 0 and the parsed info in index 1
        #Call functions to add them to the database below
        for game in x:
            os.system("echo [GAME?] {} >> analyzeLOG.txt".format(game))
            if game[0] in gamesIngamecodes:
                os.system("echo [INFO] Game is in gamecodes already >> analyzeLOG.txt")
                if game[0] in gamesIngamestats:
                    os.system("echo [INFO] Game is also in gamestats >> analyzeLOG.txt")
                else:
                    CSGOsql.addGameStats(game)
                    os.system("echo [ADD] Adding to gamestats >> analyzeLOG.txt")
            else:
                os.system("echo [DOUBLEADD] Game is being added to gamecodes and gamestats >> analyzeLOG.txt")
                CSGOsql.addGameCodes([game[0]])
                CSGOsql.addGameStats(game)
    os.system("echo [EXIT] Exiting >> analyzeLOG.txt")
    exit(0)
