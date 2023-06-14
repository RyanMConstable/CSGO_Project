#! C:\Users\ry4nm\AppData\Local\Programs\Python\Python311\python.exe
import CSGOsql, time


if __name__ == '__main__':
    #Otherwise we want to automatically check for new games for every user
    CSGOsql.updateNewGames()
    
    startTime = time.time()
    #!!!!!!This needs to be quicker!!!!!!
    #Also, there is an error when multiple users have the same ending game for some reason...
    CSGOsql.updateAllUsers()
    
    #Tracks time for CSGOsql.updateAllUsers()
    totalTime = time.time()-startTime
    print(f'Time: {totalTime:.2f} sec')
    
    
    
    #Error #1:
    #Error when calling updateAllUsers... The first user downloads all the games and adds to the database, but then
    #Other users also download the games that the first user just added for some reason?