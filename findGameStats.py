#This file will contain the functions to find statistics of the gamestats table
import dbconnection

#Very useful stat function, type in the column name of the database, and the steam id and it will return the sum of that column
def selectCombinedUserStat(stat, steamid):
    query = "SELECT SUM({}) FROM gamestats WHERE steamid = '{}'".format(stat, steamid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result[0][0]


#Very useful stat function, type in the column name of the database, and the steam id and it will return the sum of that column
def selectCombinedUserStat(stat, steamid):
    query = "SELECT AVG({}) FROM gamestats WHERE steamid = '{}'".format(stat, steamid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result[0][0]


#Function to find how many games the user has within the table
def findNumberOfGames(steamid):
    query = "SELECT COUNT(*) FROM gamestats WHERE steamid = '{}'".format(steamid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result[0][0]


#Function to find all rows for a given user in the table
def returnAllUserRows(steamid):
    query = "SELECT name, totalkills, score, tk_count, assist, deaths, 5k, 4k, 3k, 2k, 1k, headshot, kd, rws, shot_count, hit_count, flashbang_thrown, smoke_thrown, he_thrown, incendiary_thrown, decoy_thrown, round_count FROM gamestats WHERE steamid = '{}'".format(steamid)
    result = dbconnection.executeQuery(dbconnection.createConnection(), query)
    if result is None or result == []:
        return
    return result

print(selectCombinedUserStat('rws', '76561198068939539'))