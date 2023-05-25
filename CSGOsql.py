import mysql.connector
import dbconnection

#This function adds a list of gamecodes to the database
#No duplicates
def addGameCodes(codes):
    #The following line creates a connection to the database
    #dbconnection.createConnection()
    for singleCode in codes:
        query = "SELECT * FROM gamecodes WHERE code = '{}'".format(singleCode)
        result = dbconnection.executeQuery(dbconnection.createConnection(), query)
        if result:
            continue
        newquery = "INSERT INTO gamecodes (code) VALUES (%s)"
        val = ([singleCode])
        dbconnection.executeQuery(dbconnection.createConnection(), newquery, True, val)
    return
