import os

import disnake as discord
import numpy
import requests
from PIL import Image
from colormap import rgb2hex
from disnake.ext import commands
from dotenv import load_dotenv

from utils.functions import *

if os.name != "nt":
    try:
        import uvloop
        uvloop.install()
    except ModuleNotFoundError:
        print("- WARNING: uvloop was not found, skipping")

client = commands.InteractionBot(command_prefix="e!", help_command=None, sync_commands=False)

os.chdir("/root/runner/pub/feg-bot")  # change this dir to run your own bot
load_dotenv()

@client.slash_command(name="help", description="Show my help documentation.")
async def _help(inter):
    e = discord.Embed(title="Commands", color=0x2f3136)
    for name, desc in sorted([[command.name, command.description] for command in client.slash_commands if
                              command.name != "help"]):
        e.add_field(name=f"/{name}", value=f"```fix\n{desc}\n```")
    await inter.response.send_message(embed=e)


@client.slash_command(name="invite", description="Invite me to your server!")
async def invite(inter):
    await inter.response.send_message(discord.utils.oauth_url(client.user.id, scopes=["applications.commands"]))


@client.slash_command(description="Show the current free game on Epic Games.")
async def current(inter):
    g = get_curr_free()
    if not g:
        e = discord.Embed(title="<a:x_tick:829701311850610708> No free games were found right now!",
                          color=discord.Colour.brand_red())
        return await inter.response.send_message(embed=e)
    fs = parser.parse(
        g["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["startDate"]).timestamp()
    fu = parser.parse(g["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"]).timestamp()
    g_image = Image.open(requests.get(g["keyImages"][find_dict(g["keyImages"], "type", "DieselStoreFrontWide")]["url"], stream=True).raw)
    avg = numpy.average(numpy.average(g_image, axis=0), axis=0)
    avg = int(rgb2hex(int(avg[0]), int(avg[1]), int(avg[2])).replace("#", "0x"), 16)
    e = discord.Embed(title=g["title"], description=g["description"],
                      url=f"https://www.epicgames.com/store/en-US/p/{g['productSlug']}", color=avg)
    e.add_field(name="Seller", value=g["seller"]["name"], inline=True)
    try:
        e.add_field(name="Publisher", value=g["customAttributes"][1]["value"], inline=True)
    except IndexError:
        e.add_field(name="Publisher", value="Unknown", inline=True)
    try:
        e.add_field(name="Developer", value=g["customAttributes"][2]["value"], inline=True)
    except IndexError:
        e.add_field(name="Developer", value="Unknown", inline=True)
    e.add_field(name="Original Price", value=g["price"]["totalPrice"]["fmtPrice"]["originalPrice"], inline=True)
    e.add_field(name="Free Since", value=f"<t:{int(fs)}:d>", inline=True)
    e.add_field(name="Free Until", value=f"<t:{int(fu)}:d>", inline=True)
    e.set_image(url=g["keyImages"][find_dict(g["keyImages"], "type", "DieselStoreFrontWide")]["url"])
    await inter.response.send_message(embed=e)


@client.slash_command(name="next", description="Show the upcoming free game on Epic Games.")
async def _next(inter):
    g = get_next_free()
    if not g:
        e = discord.Embed(title="<a:x_tick:829701311850610708> No free games were found right now!",
                          color=discord.Colour.brand_red())
        return await inter.response.send_message(embed=e)

    fs = parser.parse(
        g["promotions"]["upcomingPromotionalOffers"][0]["promotionalOffers"][0]["startDate"]).timestamp()
    fu = parser.parse(
        g["promotions"]["upcomingPromotionalOffers"][0]["promotionalOffers"][0]["endDate"]).timestamp()
    g_image = Image.open(requests.get(g["keyImages"][4]["url"], stream=True).raw)
    avg = numpy.average(numpy.average(g_image, axis=0), axis=0)
    avg = int(rgb2hex(int(avg[0]), int(avg[1]), int(avg[2])).replace("#", "0x"), 16)
    e = discord.Embed(title=g["title"], description=g["description"],
                      url=f"https://www.epicgames.com/store/en-US/p/{g['productSlug']}", color=avg)
    e.add_field(name="Seller", value=g["seller"]["name"], inline=True)
    try:
        e.add_field(name="Publisher", value=g["customAttributes"][1]["value"], inline=True)
    except IndexError:
        e.add_field(name="Publisher", value="Unknown", inline=True)
    try:
        e.add_field(name="Developer", value=g["customAttributes"][2]["value"], inline=True)
    except IndexError:
        e.add_field(name="Developer", value="Unknown", inline=True)
    e.add_field(name="Current Price", value=g["price"]["totalPrice"]["fmtPrice"]["originalPrice"], inline=True)
    e.add_field(name="Free After", value=f"<t:{int(fs)}:d>", inline=True)
    e.add_field(name="Free Until", value=f"<t:{int(fu)}:d>", inline=True)
    e.set_image(url=g["keyImages"][find_dict(g["keyImages"], "type", "DieselStoreFrontWide")]["url"])
    await inter.response.send_message(embed=e)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.InteractionTimedOut):
        print("- WARNING: Interaction timed out")


@client.event
async def on_ready():
    print("\n―――― Ready ――――")


if __name__ == "__main__":
    client.run(os.environ["TOKEN"], reconnect=True)
