from multiprocessing import Pool
import getJSONInfo, os, CSGOsql


#Run this script every 30 seconds or so to check for new games, increase if load increases
if __name__ == '__main__':
    getJSONInfo.downloadDems('CSGO-prhLj-VOG5B-2AtSe-xD7Lc-sFzAC')
    #Sets the number of processes it should run, max is 60 on windows, so the max will be set to 40 just in case
    processes = len(os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))
    if processes <= 0:
        print("No demos in the demoDownloads directory")
        exit(-1)
    elif processes > 40:
        print("Processes set to 40")
        processes = 40
    
    
    #Multiprocesses demoDownloads to speed up analyzing
    with Pool(len(os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))) as p:
        x = p.map(getJSONInfo.analyzeDem, os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))
        #X is going to be a list of the gamecode at index 0 and the parsed info in index 1
        #Call functions to add them to the database below
        for game in x:
            if game[0] in CSGOsql.findAllCodes():
                print("Game is in gamecodes already")
                if game[0] in CSGOsql.findAllCodesInStats():
                    print("Game is also in gamestats")
                else:
                    CSGOsql.addGameStats(game[1])
                    print("Game is not yet in gamestats")
            else:
                print("Game is being added to gamecodes")
                CSGOsql.addGameCodes(game[0])