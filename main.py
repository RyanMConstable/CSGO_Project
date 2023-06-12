#! C:\Users\ry4nm\AppData\Local\Programs\Python\Python311\python.exe
import userCommands, CSGOsql


if __name__ == '__main__':
    #userCommands.mainChainCommand() #This runs the admin functionalities
    
    #Otherwise we want to automatically check for new games for every user
    CSGOsql.updateNewGames()
    
    #!!!!!!This needs to be quicker!!!!!!
    CSGOsql.updateAllUsers()