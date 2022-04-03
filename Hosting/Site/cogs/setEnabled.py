import hikari
import lightbulb
from lightbulb.ext import filament
from pymongo import MongoClient
import json

from functions.imageHostv2 import *


dbclient = MongoClient(getDbLink())

imageHost_GetGDB = dbclient.get_database('imageHost')
imageHostDB = imageHost_GetGDB.v2
plugin = lightbulb.Plugin("setenabled")

def getColor():
    return hikari.Color.from_hex_code("3498db")

@plugin.command
@lightbulb.option("value", "true or false", type=str, required=True) 
@filament.utils.prefix_slash_command("setenabled", "Enabled or disable your embeds.")
async def command(ctx: lightbulb.Context):
    if requestDataWithDiscordID(str(ctx.author.id)) == 404:
        await ctx.respond("Your info wasn't found in the database.")
        
    else:

        if(ctx.options.value == "true"):
            updates = {
                'embedDisabled': "False"
            }
            imageHostDB.update_one({"discordId": str(ctx.author.id)}, {'$set': updates})
            await ctx.respond(f"Okay, your embed has been enabled.")
        
        elif(ctx.options.value == "false"):
            updates = {
                'embedDisabled': "True"
            }
            imageHostDB.update_one({"discordId": str(ctx.author.id)}, {'$set': updates})
            await ctx.respond(f"Okay, your embed has been disabled.")

        else:
            await ctx.respond(f"You said something other than `true` or `false`.\nSet this to `true` to have embeds enabled.\nSet this to `false` to have embeds disabled.")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)