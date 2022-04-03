import hikari
import lightbulb
from lightbulb.ext import filament
from pymongo import MongoClient
import json

from functions.imageHostv2 import *


dbclient = MongoClient(getDbLink())

imageHost_GetGDB = dbclient.get_database('imageHost')
imageHostDB = imageHost_GetGDB.v2
plugin = lightbulb.Plugin("setdescription")

@plugin.command
@lightbulb.option("description", "The description you would like.", type=str, required=True) 
@filament.utils.prefix_slash_command("setdescription", "Set the description of your embeds.")
async def command(ctx: lightbulb.Context):
    if requestDataWithDiscordID(str(ctx.author.id)) == 404:
        await ctx.respond("Your info wasn't found in the database.")

    else:
        description = ctx.options.description
        description = description.replace('"', "%1%")
        description = description.replace("'", "%2%")
        description = description.replace("’", "%2%")

        updates = {
            'embedDescription': description
        }
        imageHostDB.update_one({"discordId": str(ctx.author.id)}, {'$set': updates})
        await ctx.respond(f"Okay, your description has been changed to `{ctx.options.description}`.")

def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)