from multiprocessing import Pool
import getJSONInfo, os


#Run this script every 30 seconds or so to check for new games, increase if load increases
if __name__ == '__main__':
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
        p.map(getJSONInfo.analyzeDem, os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))