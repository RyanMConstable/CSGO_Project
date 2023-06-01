#This file will contain the functions to find statistics of the gamestats table
import dbconnection

#Very useful stat function, type in the column name of the database, and the steam id and it will return the sum of that column
def selectCombinedUserStat(stat, steamid):
    query = "SELECT SUM({}) FROM gamestats WHERE steamid = '{}'".format(stat, steamid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result[0][0]