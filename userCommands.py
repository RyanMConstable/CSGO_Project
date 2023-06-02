import CSGOsql
import getJSONInfo
import findGameStats
import findMatchSteamAPI

#This file provides a command line interface for a user
#Use this until I make a frontend

#This function is just going to run a loop until the admin decides to stop
def mainChainCommand():
    userInput = ''
    while userInput != "q":
        print("Welcome to the backend user interface!")
        print("Press 'q' to quit")
        print("Print '1' to manually enter a new code to the database")
        print("Print '2' to find the total amount of X for a given user")
        print("Print '3' to find the total games within the table for a given user")
        print("Print '4' to find all rows for every game within the table for a given user")
        print("Print '5' to add more games for an existing user")
        userInput = input("Enter a command: ").lower()
        print()
        
        if userInput == '1':
            addNewCode()
        elif userInput == '2':
            print(findTotalCol())
        elif userInput == '3':
            print(findTotalGames())
        elif userInput == '4':
            for x in findAllRows():
                print(x)
        elif userInput == '5':
            findNewGames()
            
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

#This function allows the admin to enter a steam id and a stat they would like to find for the user
#It then finds the total amount of that stat that the user has 
def findTotalCol():
    userid = input("Enter a steam id: ")
    stat = input("Enter a column name from the db: ")
    try:
        result = findGameStats.selectCombinedUserStat(stat, userid)
    except:
        return -1
    return result


#Returns the number of games for a given steamid
def findTotalGames():
    userid = input("Enter a steam id: ")
    try:
        result = findGameStats.findNumberOfGames(userid)
    except:
        return -1
    return result


#Returns the user rows for a givne user
def findAllRows():
    userid = input("Enter a steam id: ")
    try: 
        result = findGameStats.returnAllUserRows(userid)
    except:
        return -1
    return result

#Adds new games for a user to the table
def findNewGames():
    userid = input("Enter a steam id:")
    steamAPIKey = input("Enter a steam API Key:")
    steamIDKey = input("Enter a steam ID Key:")
    try:
        listOfNewCodes = findMatchSteamAPI.generateNewCodes(steamAPIKey, userid, steamIDKey)
        CSGOsql.addGameCodes(listOfNewCodes)
    except:
        return -1
    return 1