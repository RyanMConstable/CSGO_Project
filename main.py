#! C:\Users\ry4nm\AppData\Local\Programs\Python\Python311\python.exe
import CSGOsql, time


if __name__ == '__main__':
    #Otherwise we want to automatically check for new games for every user
    CSGOsql.updateNewGames()
    
    startTime = time.time()
    #!!!!!!This needs to be quicker!!!!!!
    CSGOsql.updateAllUsers()
    
    #Tracks time for CSGOsql.updateAllUsers()
    totalTime = time.time()-startTime
    print(f'Time: {totalTime:.2f} sec')
    