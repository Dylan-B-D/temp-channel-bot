import asyncio
import discord
import os
import json
from discord.ext import tasks
from datetime import timedelta, datetime
from discord.ext import commands

# DATA SAVING
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

TEMP_CHANNELS_FILE = os.path.join(DATA_DIR, 'temp_channels.json')
CLEAR_TIMES_FILE = os.path.join(DATA_DIR, 'clear_times.json')

class TempChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = self.load_temp_channels()
        self.clear_times = self.load_clear_times()
        self.clean_old_messages.start()

    def load_temp_channels(self):
        if os.path.exists(TEMP_CHANNELS_FILE):
            with open(TEMP_CHANNELS_FILE, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_temp_channels(self):
        with open(TEMP_CHANNELS_FILE, 'w') as f:
            json.dump(self.temp_channels, f)

    def load_clear_times(self):
        if os.path.exists(CLEAR_TIMES_FILE):
            with open(CLEAR_TIMES_FILE, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_clear_times(self):
        with open(CLEAR_TIMES_FILE, 'w') as f:
            json.dump(self.clear_times, f)

    @commands.command()
    async def settempchannel(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.temp_channels:
            self.temp_channels[guild_id] = []
        self.temp_channels[guild_id].append(ctx.channel.id)
        self.save_temp_channels()
        embed = discord.Embed(
            title="Temp Channel Setup",
            description="This channel has been set as a temp channel!",
            color=discord.Color.green()  # You can choose a different color if you want
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def setcleartime(self, ctx, time_in_seconds: int):
        # Check if the command is used in a temp channel
        guild_id = str(ctx.guild.id)
        if guild_id not in self.temp_channels or ctx.channel.id not in self.temp_channels[guild_id]:
            return

        if guild_id not in self.clear_times:
            self.clear_times[guild_id] = {}
        
        self.clear_times[guild_id][str(ctx.channel.id)] = time_in_seconds
        self.save_clear_times()

        embed = discord.Embed(
            title="Clear Time Set",
            description=f"Messages in this channel will now be cleared after {time_in_seconds} minutes!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx):
        # Check if the command is used in a temp channel
        guild_id = str(ctx.guild.id)
        if guild_id not in self.temp_channels or ctx.channel.id not in self.temp_channels[guild_id]:
            await ctx.send("This command can only be used in a temp channel.")
            return

        # Ask for confirmation
        confirmation_msg = await ctx.send("Are you sure you want to clear all messages in this channel? Type `yes` to confirm or `no` to cancel.")
        
        def check(message):
            return message.author == ctx.author and message.content in ['yes', 'no']

        try:
            # Wait for a reply from the user
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            
            if msg.content == 'yes':
                await ctx.channel.purge()
                await ctx.send("Channel cleared!", delete_after=5)
            else:
                await ctx.send("Clearing cancelled.", delete_after=5)
        
        except asyncio.TimeoutError:
            await ctx.send("Clearing request timed out. Please try again.")

    @tasks.loop(seconds=20)  # Run every 20 seconds for debugging
    async def clean_old_messages(self):
        for guild_id, channel_ids in self.temp_channels.items():
            guild = self.bot.get_guild(int(guild_id))
            if not guild:
                continue
            for channel_id in channel_ids:
                channel = guild.get_channel(channel_id)
                if not channel:
                    continue
                
                clear_time = self.clear_times.get(guild_id, {}).get(str(channel_id), 5)
                time_limit = discord.utils.utcnow() - timedelta(minutes=clear_time)
                
                async for message in channel.history(limit=100):
                    if message.created_at < time_limit:
                        await message.delete()

    @clean_old_messages.before_loop
    async def before_clean_old_messages(self):
        await self.bot.wait_until_ready()