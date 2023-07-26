from multiprocessing import Pool
import getJSONInfo, os, CSGOsql, datetime, discordMessage
from loggingsetup import autologf, addlogf



#This script is called from downloadDemsMain and is run to analyze all games in the folder
if __name__ == '__main__':
    autolog = autologf()
    addlog = addlogf()
    #Sets the number of processes it should run, max is 60 on windows, so the max will be set to 40 just in case
    processes = len(os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))
    if processes <= 0:
        exit(0)
    elif processes > 8:
        autolog.warning('[INFO] Processes set to 8')
        processes = 8
    else:
        autolog.info(F"[DIRECTORIES] {os.listdir(os.path.join(os.getcwd(), 'demoDownloads'))}")
    
    
    #This way they are not called multiple times, increases speed of program
    gamesIngamecodes = CSGOsql.findAllCodes()
    gamesIngamestats = CSGOsql.findAllCodesInStats()
    

    #Multiprocesses demoDownloads to speed up analyzing
    with Pool(processes) as p:
        try:
            x = p.map(getJSONInfo.analyzeDem, os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))
        except Exception as e:
            autolog.critical(F"[ERROR] {e}")
            exit(0)
        for game in x:
            currentTime = datetime.datetime.now()
            if game is None or game == []:
                autolog.warning("[NONE] Game is none")
                continue
            if game[0] in gamesIngamecodes:
                autolog.info("[INFO] Game is in gamecodes already")
                if game[0] in gamesIngamestats:
                    try:
                        autolog.info(F"[INFO] Game is also in gamestats {os.path.join(os.path.join(os.getcwd(), 'demoDownloads'), game[0])}")
                        os.system("rd /s /q {}".format(os.path.join(os.path.join(os.getcwd(), 'demoDownloads'), game[0])))
                        #subprocess.call(["rm", "-r", os.path.join(os.path.join(os.getcwd(), 'demoDownloads'), game[0])])
                    except Exception as e:
                        autolog.critical(F"[ERROR] {e}\n")
                        autolog.critical(F"[PATH] {os.path.join(os.path.join(os.getcwd(), 'demoDownloads'), game[0])}")
                else:
                    CSGOsql.addGameStats(game)
                    addlog.info(F"[ADD] Adding {game[0]} to gamestats [TIME] {currentTime}")
                    discordMessage.notify(game)
            else:
                addlog.info(F"[DOUBLEADD] Game {game[0]} is being added to gamecodes and gamestats [TIME] {currentTime}")
                CSGOsql.addGameCodes([game[0]])
                CSGOsql.addGameStats(game)
                discordMessage.notify()
    exit(0)
