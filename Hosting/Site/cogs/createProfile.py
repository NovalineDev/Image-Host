import hikari
import lightbulb
from lightbulb.ext import filament
from pymongo import MongoClient
import json
import random
import string
import os

from functions.imageHostv2 import *


dbclient = MongoClient(getDbLink())

imageHost_GetGDB = dbclient.get_database('imageHost')
imageHostDB = imageHost_GetGDB.v2


plugin = lightbulb.Plugin("createProfile")

@plugin.command
@lightbulb.option("username", "The username the user would like to have.", type=str, required=True)
@lightbulb.option("user", "The user you'd like to make a profile for.", type=hikari.Member, required=True)
@filament.utils.prefix_slash_command("createprofile", "Creates a profile for a user.")
async def command(ctx: lightbulb.Context):
    user = ctx.options.user
    if str(ctx.author.id) not in getOwnerID():
        await ctx.respond("You are not a bot admin.")

    else:
        if requestDataWithDiscordID(str(user.id)) != 404:
            await ctx.respond("That person already has a profile.")
        elif requestDataWithUserName(ctx.options.username)  != 404:
            await ctx.respond("A profile with that username already exists.")

        else:
            ins = {
                "id": str(1 + int(imageHostDB.count_documents({}))),
                "discordId": str(user.id),
                "userName": str(ctx.options.username),
                "privateKey": str(''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(35))),
                "embedDisabled": "False",
                "embedColor": "0e1659",
                "embedSmallText": "use %1%/setsmalltext%1% to change this",
                "embedTitle": "use %1%/settitle%1% to change this",
                "embedDescription": "use %1%/setdescription%1% to change this",
            }

            path = os.path.join(f"/home/Hosting/Site/web/UploadCache/{ctx.options.username}")
            os.popen(f"mkdir {path}")

            imageHostDB.insert_one(ins)
            await ctx.respond(f"Okay, a profile has been made for {user.mention} as {ctx.options.username}!")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)