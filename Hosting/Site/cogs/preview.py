import hikari
import lightbulb
from lightbulb.ext import filament
from pymongo import MongoClient
import json
import random

from functions.imageHostv2 import *


dbclient = MongoClient(getDbLink())

imageHost_GetGDB = dbclient.get_database('imageHost')
imageHostDB = imageHost_GetGDB.v2
plugin = lightbulb.Plugin("preview")

domain = getDomain()

@plugin.command
@filament.utils.prefix_slash_command("preview", "Preview your embeds.")
async def command(ctx: lightbulb.Context):
    a = requestDataWithDiscordID(str(ctx.author.id))
    if a == 404:
        await ctx.respond("Your info wasn't found in the database.")
        
    else:

        await ctx.respond(f"https://{domain}/api/v2/preview/{a['userName']}#{random.randint(1000, 9999)}")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)