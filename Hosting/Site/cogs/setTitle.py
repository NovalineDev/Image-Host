import hikari
import lightbulb
from lightbulb.ext import filament
from pymongo import MongoClient
import json

from functions.imageHostv2 import *


dbclient = MongoClient(getDbLink())

imageHost_GetGDB = dbclient.get_database('imageHost')
imageHostDB = imageHost_GetGDB.v2
plugin = lightbulb.Plugin("settitle")

@plugin.command
@lightbulb.option("title", "The title you would like.", type=str, required=True) 
@filament.utils.prefix_slash_command("settitle", "Set the title of your embeds.")
async def command(ctx: lightbulb.Context):
    if requestDataWithDiscordID(str(ctx.author.id)) == 404:
        await ctx.respond("Your info wasn't found in the database.")

    else:
        title = ctx.options.title
        title = title.replace('"', "%1%")
        title = title.replace("'", "%2%")
        title = title.replace("’", "%2%")

        updates = {
            'embedTitle': title
        }
        imageHostDB.update_one({"discordId": str(ctx.author.id)}, {'$set': updates})
        await ctx.respond(f"Okay, your title has been changed to `{ctx.options.title}`.")

def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)