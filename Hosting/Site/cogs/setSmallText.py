import hikari
import lightbulb
from lightbulb.ext import filament
from pymongo import MongoClient
import json

from functions.imageHostv2 import *


dbclient = MongoClient(getDbLink())

imageHost_GetGDB = dbclient.get_database('imageHost')
imageHostDB = imageHost_GetGDB.v2
plugin = lightbulb.Plugin("setsmalltext")

@plugin.command
@lightbulb.option("text", "The description you would like.", type=str, required=True) 
@filament.utils.prefix_slash_command("setsmalltext", "Set the setsmalltext of your embeds.")
async def command(ctx: lightbulb.Context):
    if requestDataWithDiscordID(str(ctx.author.id)) == 404:
        await ctx.respond("Your info wasn't found in the database.")
        
    else:

        text = ctx.options.text
        text = text.replace('"', "%1%")
        text = text.replace("'", "%2%")
        text = text.replace("’", "%2%")

        updates = {
            'embedSmallText': text
        }
        imageHostDB.update_one({"discordId": str(ctx.author.id)}, {'$set': updates})
        await ctx.respond(f"Okay, your smalltext has been changed to `{ctx.options.text}`.")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)