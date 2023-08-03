import requests, os
#This file should notify the discord that the new game has been added... for now



#In here we want to actually find what discords this should be sent to...
#We might want to send directly to users after a game?


#1 find all servers that the bot is in
#2 find all servers that the user is in
    
#3 If there is a text channel in a server that the user and the bot are both in
#4 If there is a channel with "bot" in the name, send it there, otherwise send to random 1 channel


def notify(game = None):
    payload = {
        'content' : "-Summary Time"
    }
    header = {
        'Authorization' : F'Bot {os.environ["DISCORD_TOKEN"]}'
    } 
    #Test discord directly below
    #requests.post("https://discord.com/api/v9/channels/1105249488702030026/messages", data=payload, headers = header)
    
    #Our main discord
    requests.post("https://discord.com/api/v9/channels/1091583699746836511/messages", data=payload, headers = header)
    return