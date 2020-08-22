# If somebody is actually looking at this the keyphrase me and my friends used was "weed" because we like spamming weed in the chat at 4:20 am or pm because we have little pea brains


import discord
import json
import asyncio

# Initializing bot and variables
client = discord.Client()
finalmessage = ""
weedercount = 0
weeder = ""


YOURTOKEN = "NzQxNTA1NjA0NTM0Nzk2MzQ4.Xy4i6A.w8bXySm0-6NO31H9JVOXgv0NJxE"
YOURGUILDSID = 691931904135397417
YOURID = 146026805365571585
YOURFILENAME = "whatever.json"

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
    if message.content.lower() == "!stopweed" and message.author.id == YOURID:
        with open(YOURFILENAME, "w") as j:
            j.write( json.dumps(m) )
            j.close()
        await message.channel.send("Weed counts saved :)")
        await client.close()

    # minusweed is used for testing, so i can easily remove a weed from myself
    if message.content.lower() == "!minusweed":
        m[str(message.author.id)]["xp"] -= 1
        await message.channel.send("weed subtracted")
        


    # !weed returns personal weed count
    elif message.content == "!weed":
        await message.channel.send(str(m[str(message.author.id)]["xp"]) + " weeds" )

    # !weederboard returns weed count of whole server
    elif message.content == "!weederboard":
        # Getting weeds of whole server and putting into one string, so it doesn't spam chat
        
        weedercount = 0

        for member in client.get_guild(YOURGUILDSID).members:
            if not str(str(member).rstrip("#1234567890")).lower().endswith("bot") and not str(str(member).rstrip("#1234567890")).lower().endswith("rythm"):
                finalmessage += (str(member).rstrip("#1234567890") + ": " + str(m[str(member.id)]["xp"]) +  " weeds \n")
                # Finding the member with highest count
                
                # Once you get around to making sorted leaderboard, use selection sort
                #   - iterates through and finds lowest element in the unsorted original array and places it into a sorted subarray
            
                if int(str(m[str(member.id)]["xp"])) > weedercount:
                    weedercount = int(str(m[str(member.id)]["xp"])) 
                    weeder = (str(member).rstrip("#1234567890"))
                    tie = False

                elif int(str(m[str(member.id)]["xp"])) == weedercount:
                    weeder += " and " + (str(member).rstrip("#1234567890"))
                    tie = True

        finalmessage += "\n"
        
        if tie:
            finalmessage += "The current weeders are "
        else:
            finalmessage += "The current weeder is "
        finalmessage += weeder

        finalmessage += " at "
        finalmessage += str(weedercount)
        finalmessage += " weeds"


        await message.channel.send(finalmessage)
        # Resetting finalmessage to empty so !weederboard doesn't keep adding onto itself the next time it is used
        finalmessage = ""

    # This is where it counts when people say "weed" in chat, and other variances of weed
    elif message.author != client.user and message.content.lower().startswith("wee"):
        # Check if they aren't on cooldown, then add 1 to their weedCount and set CD back to 5 minutes
        if m[str(message.author.id)]["messageCountdown"] <= 0:
            m[str(message.author.id)]["xp"] += 1
            m[str(message.author.id)]["messageCountdown"] = 360
            await message.channel.send("weed")
            # adding an autosave, hope it works
            with open(YOURFILENAME, "w") as j:
                j.write( json.dumps(m) )
                j.close()



    # Some fun little animal messages because I thought it was nice :)
    elif message.author != client.user and message.content.lower() == "!duck":
            await message.channel.send("quack")
    elif message.author != client.user and message.content.lower() == "!dog":
        await message.channel.send("bark!")
    elif message.author != client.user and message.content.lower() == "!cat":
        await message.channel.send("mewow")
    elif message.author != client.user and message.content.lower() == "!frog":
        await message.channel.send("ribbit")
    elif message.author != client.user and message.content.lower() == "!fwog":
        await message.channel.send("You matter.")


# Add new members to the json if they join the server
@client.event
async def on_member_join(member):
    m[str(member.id)] = {"xp" : 0, "messageCountdown" : 0}

client.run(YOURTOKEN)
