import hikari
import lightbulb
from lightbulb.ext import filament
from pymongo import MongoClient
import json
import os

from functions.imageHostv2 import *


dbclient = MongoClient(getDbLink())

imageHost_GetGDB = dbclient.get_database('imageHost')
imageHostDB = imageHost_GetGDB.v2
plugin = lightbulb.Plugin("deleteall")

@plugin.command
@filament.utils.prefix_slash_command("deleteall", "Delete all your uploads.")
async def command(ctx: lightbulb.Context):
    a = requestDataWithDiscordID(str(ctx.author.id))
    if a == 404:
        await ctx.respond("Your info wasn't found in the database.")

    else:
        username = a["userName"]
        path = os.path.join(f"/home/Hosting/Site/web/UploadCache/{username}")
        os.popen(f"rm {path}/*")

        await ctx.respond(f"Okay, all your uploads have been deleted.")

def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)