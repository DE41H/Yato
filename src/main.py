import os
import random
import discord
from discord_components import *
from discord.ext import commands
from anime_downloader.sites import get_anime_class, _4anime

client = commands.Bot(command_prefix="~", case_insensitive=True, intents=discord.Intents.all())
client.remove_command("help")
colors = [discord.Color.blue(), discord.Color.dark_blue(), discord.Color.dark_red(), discord.Color.blurple(), discord.Color.dark_gold(), discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_magenta(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_teal(), discord.Color.dark_theme(), discord.Color.darker_grey(), discord.Color.gold(), discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.lighter_grey(), discord.Color.magenta(), discord.Color.orange(), discord.Color.purple(), discord.Color.red(), discord.Color.teal()]


@client.event
async def on_ready():
    print(client.user.name)
    DiscordComponents(client)
    await client.change_presence(activity=discord.Streaming(name="Noragami", url="https://www.twitch.tv/animevibesradio"), status=discord.Status.dnd)


@client.event
async def on_message(msg):
    if msg.author.bot:
        return
    if msg.content.lower() == "<@!850765752293392406>" or msg.content.lower() == "<@850765752293392406>":
        pass
    await client.process_commands(msg)


@client.command(pass_context=True, aliases=["help"])
async def commands(ctx):
    embed = discord.Embed(title="Help Menu Lol", color=random.choice(colors))
    await ctx.channel.send(embed=embed, components=[Button(style=ButtonStyle.red, label="Delete")])
    awaited = await client.wait_for("button_click", check=lambda i: i.component.label.startswith("Delete"))
    await awaited.message.delete()


@client.command(pass_context=True)
async def invite(ctx):
    embed = discord.Embed(color=random.choice(colors), description="[Click on this message or the button below to invite Yato](https://discord.com/api/oauth2/authorize?client_id=850765752293392406&permissions=8&scope=bot)")
    await ctx.channel.send(embed=embed, components=[Button(style=ButtonStyle.URL, url="https://discord.com/api/oauth2/authorize?client_id=850765752293392406&permissions=8&scope=bot", label="Invite Me"), Button(style=ButtonStyle.red, label="Delete")])
    awaited = await client.wait_for("button_click", check=lambda i: i.component.label.startswith("Delete"))
    await awaited.message.delete()


@client.command(pass_context=True)
async def anime(ctx, *, query: str):
    four_anime = get_anime_class("4anime.to")
    search = four_anime.search(query)
    if len(search) == 0:
        await ctx.reply(f"**{query.capitalize()} not found on 4anime.to**")
        return
    if len(search) == 1:
        for item in search:
            await ctx.channel.send(f"**{item.title}**",
                                   components=[Button(style=ButtonStyle.URL, url=item.url, label="Watch on 4anime.to")])
    elif len(search) > 1:
        embed = discord.Embed(description="**:biohazard: More than one search result found :biohazard:**",
                              color=random.choice(colors))
        embed.set_footer(text=f"Search results for {query.capitalize()}, requested by {ctx.author}")
        for item in search:
            episodes = _4anime.Anime4(item.url)
            embed.add_field(name=item.title, inline=False,
                            value=f"{len(episodes)} episodes, [Watch on 4anime.to]({item.url})")
        await ctx.channel.send(embed=embed, components=[Button(style=ButtonStyle.red, label="Delete")])
        awaited = await client.wait_for("button_click", check=lambda i: i.component.label.startswith("Delete"))
        await awaited.message.delete()


if __name__ == "__main__":
    client.run(os.getenv("TOKEN"))
