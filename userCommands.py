#This file provides a command line interface for a user
#Use this until I make a frontend

#This function is just going to run a loop until the admin decides to stop
def mainChainCommand():
    userInput = ''
    while userInput != "q":
        userInput = input("Type q to quit\nEnter a command: ").lower()
        print()
    print("Exiting...")
    return