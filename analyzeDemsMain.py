from multiprocessing import Pool
import getJSONInfo, os



if __name__ == '__main__':
    processes = len(os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))
    if processes <= 0:
        print("No demos in the demoDownloads directory")
        exit(-1)
    elif processes > 30:
        print("Processes set to 30")
        processes = 30
    
    
    #Multiprocesses demoDownloads to speed up analyzing
    with Pool(len(os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))) as p:
        p.map(getJSONInfo.analyzeDem, os.listdir(os.path.join(os.getcwd(), 'demoDownloads')))