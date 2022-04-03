import json
from pymongo import MongoClient

## ---- CONFIG ---- ##

link = "put-your-link-here"
# Should look something like this https://ibb.co/8mjzx4P
# You can find this in your MongoDB panel

bot_token = "put-the-token-here"
# The token of the bot that'll manage your hosting
# Make sure all intents are enabled

your_domain = "https://example.com"
# Put your domain here

server_id = "discord-server-id-here"
# The id of the server where the host's config will be edited

owner_id = ["discord-user-id-here", "discord-user-id-2-here"] # you can add as many as you want
# The id of the bot admin

## ---- CONFIG --- ##

dbclient = MongoClient(link)

imageHost_GetGDB = dbclient.get_database('imageHost')
imageHostDB = imageHost_GetGDB.v2
imageHostDBDomains = imageHost_GetGDB.info

def getDbLink():
    return link

def getBotToken():
    return bot_token

def getDomain():
    return your_domain

def getID():
    return server_id

def getOwnerID():
    return owner_id

def requestDataWithID(id):
    try:
        var = imageHostDB.find_one({"id": id}, {"_id": False})
        var1 = str(var).replace("'", '"')
        return json.loads(var1)

    except Exception:
        return 404

def requestDataWithDiscordID(discordId):
    try:
        var = imageHostDB.find_one({"discordId": discordId}, {"_id": False})
        var1 = str(var).replace("'", '"')
        return json.loads(var1)

    except Exception:
        return 404

def requestDataWithUserName(username):
    try:
        var = imageHostDB.find_one({"userName": username}, {"_id": False})
        var1 = str(var).replace("'", '"')
        return json.loads(var1)

    except Exception:
        return 404
