import hikari
import lightbulb
from lightbulb.ext import filament
from pymongo import MongoClient
import json
import re

from functions.imageHostv2 import *


dbclient = MongoClient(getDbLink())

imageHost_GetGDB = dbclient.get_database('imageHost')
imageHostDB = imageHost_GetGDB.v2

plugin = lightbulb.Plugin("setcolor")

@plugin.command
@lightbulb.option("color", "The color you would like.", type=str, required=True)
@filament.utils.prefix_slash_command("setcolor", "Set the color of your embeds.")
async def command(ctx: lightbulb.Context):
    color = ctx.options.color.replace('#', '')
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', f"#{color}")
    if match:
        if requestDataWithDiscordID(str(ctx.author.id)) == 404:
            await ctx.respond("Your info wasn't found in the database.")

        else:
            updates = {
                'embedColor': color
            }
            imageHostDB.update_one({"discordId": str(ctx.author.id)}, {'$set': updates})
            await ctx.respond(f"Okay, your color has been changed to `#{color}`.")

    else:
        await ctx.respond("You've given me an invalid hex color.")
    
def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
