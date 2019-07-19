import discord
import time
import asyncio
# first take on building a dicord bot in python

client = discord.Client()
token = open("token.txt", "r").read()
# token = 'NTAzMzgyOTQyMDE0MjQyODQ3.Dq1s0g.2yBg4hJKkAapK9fAagV7vSJydwk'
# https://discordapp.com/oauth2/authorize?client_id=503382942014242847&scope=bot&permissions=92160
def community_report(guild):
    online = 0
    idle = 0
    offline = 0

    for m in guild.members:
        if str(m.status) == "online":
            online += 1
        if str(m.status) == "offline":
            offline += 1
        else:
            idle += 1

    return online, idle, offline

async def user_metrics_background_task():
    await client.wait_until_ready()
    global my_server

    while not client.is_closed():
        try:
            online, idle, offline = community_report(my_server)
            with open("usermetrics.csv","a") as f:
                f.write(f"{int(time.time())},{online},{offline},{idle}/n")
            await asyncio.sleep(5)

        except Exception as e:
            print(str(e))
            await asyncio.sleep(5)

@client.event # event decorator
async def on_ready():
    global my_server
    my_server = client.get_guild(255233110071836672)
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):   # event that happens per any message.
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    if "member_count" == message.content.lower():
        await message.channel.send(f"```py\n{my_server.member_count}```")

    elif "logout()" == message.content.lower():
        await client.close()

    elif "server_report()" == message.content.lower():
        online, idle, offline = community_report(my_server)
        await message.channel.send(f"```Online: {online}.\nIdle/Busy/Dnd: {idle}.\nOffline: {offline}```")

client.loop.create_task(user_metrics_background_task())
client.run(token)
