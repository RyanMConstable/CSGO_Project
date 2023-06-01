import CSGOsql
import getJSONInfo
#This file provides a command line interface for a user
#Use this until I make a frontend

#This function is just going to run a loop until the admin decides to stop
def mainChainCommand():
    userInput = ''
    while userInput != "q":
        print("Welcome to the backend user interface!")
        print("Press 'q' to quit")
        print("Print '1' to manually enter a new code to the database")
        userInput = input("Enter a command: ").lower()
        print()
        
        if userInput == '1':
            addNewCode()
        
        print()
    print("Exiting...")
    return


#Make a function that allows the admin to manually enter a new match code to both databases
def addNewCode():
    print("Enter a CSGO match sharing code")
    print("The format is 'CSGO-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX'")
    code = input("Enter code: ")
    print()
    try:
        CSGOsql.addGameCodes([code])
        CSGOsql.addGameStats(getJSONInfo.returnGameInfo(getJSONInfo.getJSONInfo(code)))
    except:
        print("Failure to add code: '{}'".format(code))
        return -1
    print("Entered code: '{}' to databases.".format(code))
    return
    