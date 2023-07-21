import requests, os
#This file should notify the discord that the new game has been added... for now

def notify():
    payload = {
        'content' : "-Summary of last game"
    }
    header = {
        'Authorization' : F'Bot {os.environ["DISCORD_TOKEN"]}'
    } 
    requests.post("https://discord.com/api/v9/channels/1105249488702030026/messages", data=payload, headers = header)
    requests.post("https://discord.com/api/v9/channels/1130926410517712926/messages", data=payload, headers = header)
    return