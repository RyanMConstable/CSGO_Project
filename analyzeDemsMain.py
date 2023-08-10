from multiprocessing import Pool
import getJSONInfo, os, CSGOsql, datetime, discordMessage
from loggingsetup import autologf, addlogf



#This script is called from downloadDemsMain and is run to analyze all games in the folder
if __name__ == '__main__':
    autolog = autologf()
    addlog = addlogf()
    processes = len(os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))
    if processes <= 0:
        exit(0)
    elif processes > 8:
        autolog.warning('[INFO] Processes set to 8')
        processes = 8
    else:
        autolog.info(F"[DIRECTORIES] {os.listdir(os.path.join(os.getcwd(), 'demoDownloads'))}")
    
    
    #This way they are not called multiple times, increases speed of program, increases amount of memory used
    #These all return dictionaries, even if empty dictionaries
    gamesIngamecodes = CSGOsql.findAllCodes()
    gamesIngamestats = CSGOsql.findAllCodesInStats()
    gamesIngameinfo = CSGOsql.findAllCodesIngameinfo()

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
                
                #This is for gameinfo table
                if game[0] in gamesIngameinfo:
                    autolog.info(F"[INFO] Game is also in gameinfo {os.path.join(os.path.join(os.getcwd(), 'demoDownloads'), game[0])}")
                else:
                    CSGOsql.addGameInfo(game)
                    addlog.info(F"[ADD] Adding {game[0]} to gameinfo [TIME] {currentTime}")
                
                #this is for gamestats table
                if game[0] in gamesIngamestats:
                    try:
                        autolog.info(F"[INFO] Game is also in gamestats {os.path.join(os.path.join(os.getcwd(), 'demoDownloads'), game[0])}")
                        os.system("rd /s /q {}".format(os.path.join(os.path.join(os.getcwd(), 'demoDownloads'), game[0])))
                    except Exception as e:
                        autolog.critical(F"[ERROR] {e}\n")
                        autolog.critical(F"[PATH] {os.path.join(os.path.join(os.getcwd(), 'demoDownloads'), game[0])}")
                else:
                    CSGOsql.addGameStats(game)
                    addlog.info(F"[ADD] Adding {game[0]} to gamestats [TIME] {currentTime}")
                    #discordMessage.notify(game)
                    
            else:
                addlog.info(F"[DOUBLEADD] Game {game[0]} is being added to gamecodes and gamestats [TIME] {currentTime}")
                CSGOsql.addGameCodes([game[0]])
                CSGOsql.addGameStats(game)
                CSGOsql.addGameInfo(game)
                #discordMessage.notify()
    exit(0)
