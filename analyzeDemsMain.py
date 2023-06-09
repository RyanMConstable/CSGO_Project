from multiprocessing import Pool
import getJSONInfo, os, CSGOsql, datetime, subprocess


#Run this script every 30 seconds or so to check for new games, increase if load increases
if __name__ == '__main__':
    #Sets the number of processes it should run, max is 60 on windows, so the max will be set to 40 just in case
    processes = len(os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))
    if processes <= 0:
        #os.system("echo [EXIT] Exiting no demos found >> autoLOG.txt")
        exit(0)
    elif processes > 8:
        os.system("echo [INFO] Processes set to 8 >> autoLOG.txt".format())
        processes = 8
    else:
        os.system("echo [DIRECTORIES] {} >> autoLOG.txt".format(os.listdir(os.path.join(os.getcwd(), 'demoDownloads'))))
    
    
    #This way they are not called multiple times, increases speed of program
    gamesIngamecodes = CSGOsql.findAllCodes()
    gamesIngamestats = CSGOsql.findAllCodesInStats()
    

    #Multiprocesses demoDownloads to speed up analyzing
    with Pool(processes) as p:
        try:
            x = p.map(getJSONInfo.analyzeDem, os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))
        except Exception as e:
            os.system("echo [ERROR] {} >> autoLOG.txt".format(e))
            exit(0)
        #X is going to be a list of the gamecode at index 0 and the parsed info in index 1
        #Call functions to add them to the database below
        #os.system("echo [X] {} >> autoLOG.txt".format(x))
        for game in x:
            currentTime = datetime.datetime.now()
            if game is None or game == []:
                os.system("echo [NONE] game is none >> autoLOG.txt")
                continue
            if game[0] in gamesIngamecodes:
                os.system("echo [INFO] Game is in gamecodes already >> autoLOG.txt")
                if game[0] in gamesIngamestats:
                    try:
                        os.system("echo [INFO] Game is also in gamestats {} >> autoLOG.txt".format(os.path.join(os.path.join(os.getcwd(), 'demoDownloads'), game[0])))
                        os.system("rd /s /q {}".format(os.path.join(os.path.join(os.getcwd(), 'demoDownloads'), game[0])))
                        #subprocess.call(["rm", "-r", os.path.join(os.path.join(os.getcwd(), 'demoDownloads'), game[0])])
                    except Exception as e:
                        os.system("echo [ERROR] {} >> autoLOG.txt".format(e))
                        os.system("echo [PATH] {} >> autoLOG.txt".format(os.path.join(os.path.join(os.getcwd(), 'demoDownloads'), game[0])))
                else:
                    CSGOsql.addGameStats(game)
                    os.system("echo [ADD] Adding {} to gamestats [TIME] {} >> addLOG.txt".format(game[0], currentTime))
            else:
                os.system("echo [DOUBLEADD] Game {} is being added to gamecodes and gamestats [TIME] {} >> addLOG.txt".format(game[0], currentTime))
                CSGOsql.addGameCodes([game[0]])
                CSGOsql.addGameStats(game)
    exit(0)
