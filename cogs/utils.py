
import discord
from discord.ext import commands
from discord import Embed

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="List of commands and their usages:", color=discord.Color.blue())

        # settempchannel command details
        embed.add_field(name="!settempchannel", value="Sets the current channel as a temporary channel.", inline=False)

        # setcleartime command details
        embed.add_field(name="!setcleartime [minutes]", value="Sets the clear time for messages in the current temp channel. Value is in minutes.", inline=False)

        # info command details
        embed.add_field(name="!info", value="View temporary channels in the server and the clear time for these channels.", inline=False)

        # removetempchannel command details
        embed.add_field(name="!removetempchannel", value="Removes the current channel from being a temporary channel.", inline=False)

        await ctx.send(embed=embed)
