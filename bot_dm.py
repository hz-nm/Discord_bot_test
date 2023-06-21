# Setting up member roles as Admin
# https://support.discord.com/hc/en-us/articles/206029707-Setting-Up-Permissions-FAQ#:~:text=Click%20on%20the%20'Members'%20tab,you%20assigned%20to%20that%20role.


import os
import random
from discord import channel
from dotenv import load_dotenv
from datetime import datetime
import csv

import discord
from discord.ext import commands
from discord.ext import tasks

intents = discord.Intents.default()
intents.members = True

# intent = discord.Intents.all()

# PLEASE MAKE REQUIRED CHANGES OVER HERE...
MESSAGE = 'Put your message over here within these inverted commas!'

time_to_kick = 60

last_online = {}
latest_online = {}


# load the previous dictionaries here
if os.path.exists('last_online.csv'):
    with open('last_online.csv', 'r') as f:
        content = csv.reader(f)
        for row in content:
            k = row[0]
            last_online[k] = row[1]

if os.path.exists('latest_online.csv'):
    with open('latest_online.csv', 'r') as f:
        content = csv.reader(f)
        for row in content:
            k = row[0]
            latest_online[k] = row[1]


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

bot = commands.Bot(intents=intents, command_prefix='!')

###########
# 1 - Send message to new member when they join
# Automatically invoked
###########
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        'Hi {}, welcome to my Discord server!'.format(member.name)
    )

@bot.event
async def on_ready():
    print('{} has connected to Discord!'.format(bot.user.name))

    if not check_status_kick.is_running():
        check_status_kick.start()



###########
# 2 - Test Command
# Invoked when you send a message with the command "!test" to a channel within the server
###########
@bot.command(name='test')
async def test_message(ctx): 
    messages = [
        'Bot Testing 1'
    ]

    response = random.choice(messages)

    await ctx.send(response)        # send a random message

member_list = []

###########
# 3 - Mass Messaging Command
# Invoked when you send a message with the command "!dmm" to a channel within the server
###########
@bot.command(name='dmm')
@commands.has_role('Admin')
async def send(ctx):
    for member in ctx.guild.members:
        if member.name == 'OGMintB':
            pass
        else:
            member_list.append(member.name)
            await member.create_dm()
            # await member.send('Hi, this is a TEST DM')
            await member.send(MESSAGE)
    
    await ctx.send("Your request has been accomplished Dear King {}!".format(ctx.author.mention))


    print(member_list)

###########
# 4 - Link Removal Command
# Invoked automatically when someone sends a message to the channel containing a link except for ogminter
###########
@bot.event
async def on_message(message):
    if 'https://' in message.content:
        if message.author.name == 'ogminter':
            pass
        else:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Don't send links!")
    else:
        await bot.process_commands(message)
        

###########
# 5 - Kick Command
# Invoked when you send a message with the command "!status" to a channel within the server
# Ver - 2 --> This command will now run by itself every 12 hours. This can be changed by changing the below hours=12 to whatever interval wanted.
# can be rolled back to previous way of invocation via command !status if needed.
###########

# @bot.command(name='status')       # uncomment this for invoking kicking bot via command on server !status
# @commands.has_role('Admin')       # uncomment this for invoking kicking bot via command on server !status
@tasks.loop(hours=12)               # comment this for invoking this bot via command on server channel
async def check_status_kick(ctx):
    for member in ctx.guild.members:
        if member.name == 'OGMintB':
            continue
        if not last_online:
            last_online[member.name] = datetime.now().date()
            latest_online[member.name] = datetime.now().date()
        else:
            if member.name not in last_online.keys():
                last_online[member.name] = datetime.now().date()
                latest_online[member.name] = datetime.now().date()
        
    
    for member in ctx.guild.members:
        if member.name == 'OGMintB':
            continue
        # check status of member and if online, add a new date to the latest_online, last_online
        if member.status == discord.Status.online:
            latest_online[member.name] = datetime.now().date()
            last_online[member.name] = datetime.now().date()
        elif member.status == discord.Status.offline:
            latest_online[member.name] = datetime.now().date()
    
    # writing new things to csv files
    with open('last_online.csv', 'w') as f:
        for key in last_online.keys():
            f.write("{},{}\n".format(key, last_online[key]))
    
    with open('latest_online.csv', 'w') as f:
        for key in latest_online.keys():
            f.write("{},{}\n".format(key, latest_online[key]))

    for member in ctx.guild.members:
        if member.name == 'OGMintB':
            continue
        # check the difference between last online and latest online dates.
        offline_since = latest_online[member.name] - last_online[member.name]
        offline_since = offline_since.days
        # For debugging!
        # Comment the following line when deploying in production
        print('The user {} has been offline since {} days'.format(member.name, str(offline_since)))
        # if difference is larger than preset kick the member
        if offline_since > time_to_kick:
            reason = '{} has been inactive for more than {} days'.format(member.name, str(time_to_kick))
            await member.kick(reason=reason)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

    else:
        print(error)


bot.run(TOKEN)
