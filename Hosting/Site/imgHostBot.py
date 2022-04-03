from typing import _get_type_hints_obj_allowed_types
import hikari
import lightbulb
import os

from functions.imageHostv2 import *

print(os.getcwd())

token = getBotToken()

bot = lightbulb.BotApp(token=token,
                       default_enabled_guilds=int(getID()), prefix="!",
                       intents=hikari.Intents.ALL_UNPRIVILEGED,
                       case_insensitive_prefix_commands=True)

bot.load_extensions_from("cogs", must_exist=True)


bot.run(status=hikari.Status("idle"),
        activity=hikari.Activity(type=hikari.ActivityType.STREAMING, name="Click for free Robux!",
                                 url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
