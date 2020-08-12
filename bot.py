# If somebody is actually looking at this the keyphrase me and my friends used was "weed" because we like spamming weed in the chat at 4:20 am or pm because we have little pea brains


import discord
import json
import asyncio


# Initializing bot and variables
client = discord.Client()
finalmessage = ""

YOURTOKEN = # Your token
YOURGUILDSID = # Your server ID
YOURID = # Your user ID
YOURFILENAME = # Whatever file name you want

#initializing empty json file
m = {}


# Event of running python scripts to setup bot
@client.event
async def on_ready():
    # get the json ready
    global m

    # open and read whatever.json
    with open(YOURFILENAME, "r") as j:
        m = json.load(j)
        j.close()

    # Initializing initial counts to zero
    if len(m) == 0:
        m = {}
        for member in client.get_guild(YOURGUILDSID).members:
            m[str(member.id)] = {"xp" : 0, "messageCountdown" : 0}

    # show bot is working :)
    print("ready")

    # Cooldown timer so it doesn't get spammed
    while True:
        try:
            for member in client.get_guild(YOURGUILDSID).members:
                m[str(member.id)]["messageCountdown"] -= 1
        except:
            pass
        await asyncio.sleep(1)


# Checking messages for event triggers
@client.event
async def on_message(message):
    # Getting variables
    global m
    global finalmessage

    # Used to pause counters if you need to edit the script
    if message.content == "!stop" and message.author.id == YOURID:
        with open(YOURFILENAME, "w") as j:
            j.write( json.dumps(m) )
            j.close()
        await client.close()

    # !weed returns personal weed count
    elif message.content == "!weed":
        await message.channel.send(str(m[str(message.author.id)]["xp"]) + " weeds" )

    # !weederboard returns weed count of whole server
    elif message.content == "!weederboard":
        # Getting weeds of whole server and putting into one string, so it doesn't spam chat
        for member in client.get_guild(YOURGUILDSID).members:
            finalmessage += (str(member).rstrip("#") + ": " + str(m[str(member.id)]["xp"]) +  " weeds \n")
        await message.channel.send(finalmessage)
        # Resetting finalmessage to empty so !weederboard doesn't keep adding onto itself the next time it is used
        finalmessage = ""

    # This is where it counts when people say "weed" in chat, and other variances of weed
    elif message.author != client.user and message.content.lower().startswith("wee"):
        # Check if they aren't on cooldown, then add 1 to their weedCount and set CD back to 5 minutes
        if m[str(message.author.id)]["messageCountdown"] <= 0:
            m[str(message.author.id)]["xp"] += 1
            m[str(message.author.id)]["messageCountdown"] = 360

    # Some fun little animal messages because I thought it was nice :)
    elif message.author != client.user and message.content.lower() == "!duck":
            await message.channel.send("quack")
    elif message.author != client.user and message.content.lower() == "!dog":
        await message.channel.send("bark!")
    elif message.author != client.user and message.content.lower() == "!cat":
        await message.channel.send("mewow")
    elif message.author != client.user and message.content.lower() == "!frog":
        await message.channel.send("ribbit")

# Add new members to the json if they join the server
@client.event
async def on_member_join(member):
    m[str(member.id)] = {"xp" : 0, "messageCountdown" : 0}

client.run(YOURTOKEN)