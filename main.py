from random import randint, randrange

# TODO if using Github diff deployment on HeroKu uncomment the next line
import os
import discord
from discord.ext import commands

# Author: hyppytyynytyydytys#1010
# Created: 26 MAY 2020
# Last updated: 17 JULY 2022
# About: This is a version of Passel Bot that should ONLY be used as a private server bot.
#        Follow the instructions here on how to set up with heroku:
#
#        Passel Bot is a solution to the number of limited number of pins in a discord server.
#        It manages pins in 2 modes, Mode 1 and Mode 2. 
#
#        More information can be found on https://passelbot.wixsite.com/home
#        Passel Support Server: https://discord.gg/wmSsKCX
#
#        Mode 1: In mode 1, the most recent pinned message gets sent to a pins archive
#        channel of your choice. This means that the most recent pin wont be viewable in
#        the pins tab, but will be visible in the pins archive channel that you chose during setup
#
#        Mode 2: In mode 2, the oldest pinned message gets sent to a pins archive channel of
#        your choice. This means that the most recent pin will be viewable in the pins tab, and
#        the oldest pin will be unpinned and put into the pins archive channel
#
#        Furthermore: the p.sendall feature described later in the code allows the user to set
#        Passel so that all pinned messages get sent to the pins archive channel.

# TODO change command here if you want to use another command, replace p. with anything you want inside the single ('') quotes
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='p.',
                      status='Online',
                      case_insensitive=True,
                      intents=intents)
client.remove_command("help")

# TODO 
# sendall is set to 0 by default, change to 1 if you want
# the bot to send all pinned messages to the pins channel
sendall = 0

# TODO 
# replace the 0 with the pins channel ID for your sever
pins_channel = 867221698867757066

# When the bot is ready following sets the status of the bot
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# Command to check what the settings of the bot
@client.command(name='settings', pass_context=True)
async def settings(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        return

    await ctx.send("The mode you have setup is: " + str(mode))
    await ctx.send("Sendall is toggled to: " + str(sendall))
    await ctx.send("The pins channel for this server is: " + ctx.channel.guild.get_channel(pins_channel).mention)
    await ctx.send("done")


@client.command(name='pins', pass_context=True)
async def pins(ctx):
    channelPins = await ctx.message.channel.pins()
    print("user requested pin count for " + ctx.message.channel.name + ": " + str(len(channelPins)) + " pins")
    await ctx.send(ctx.message.channel.mention + " has " + str(len(channelPins)) + " pins.")

# The method that takes care of pin updates in a server
@client.event
async def on_guild_channel_pins_update(channel, last_pin):
    try:
        print(channel)
        print(last_pin)
        channelPins = await channel.pins()
      
        print("pins updated in " + channel.name + ": there are now " + str(len(channelPins)) + " pins.")

        last_pinned = channelPins[0]
        if len(channelPins) == 50:
            print("There are 50 pins, time to archive.")
            last_pinned = channelPins[len(channelPins) - 1]
            print(last_pinned)
            print("Building embed")
            
            # Get the member object to ensure we have role color data
            # author.color can be black if author is a User (not Member) or has no colored roles
            embed_color = last_pinned.author.color
            if embed_color == discord.Colour.default():
                # Try to fetch the member from the guild for accurate color
                try:
                    member = await last_pinned.guild.fetch_member(last_pinned.author.id)
                    embed_color = member.color if member.color != discord.Colour.default() else discord.Colour.blurple()
                except:
                    embed_color = discord.Colour.blurple()  # Fallback color

            embed_content = "\"" + last_pinned.content + "\""

            if randint(1, 512) == 7:
                embed_content = "# ✨\n" + embed_content + "\n# ✨"
                embed_color = discord.Colour(~embed_color.value & 0xFFFFFF)

            
            pinEmbed = discord.Embed(
                # title="Sent by " + last_pinned.author.name,
                description=embed_content,
                colour=embed_color
            )
            print(pinEmbed)
            # checks to see if pinned message has attachments
            print("checking for attachments")
            attachments = last_pinned.attachments
            if len(attachments) >= 1:
                print("attachment found")
                pinEmbed.set_image(url=attachments[0].url)
            print("adding jump link")
            pinEmbed.add_field(
                name="Jump", value=last_pinned.jump_url, inline=False)
            print("adding footer")
            pinEmbed.set_footer(
                text="sent in: " + last_pinned.channel.name + " - at: " + str(last_pinned.created_at))
            print("adding author")
            avatar_url = last_pinned.author.avatar.url if last_pinned.author.avatar else last_pinned.author.default_avatar.url
            pinEmbed.set_author(name='Sent by ' + last_pinned.author.name,
                url=avatar_url,
                icon_url=avatar_url)

            print("sending pin")
            await last_pinned.guild.get_channel(int(pins_channel)).send(embed=pinEmbed)

            # remove this message if you do not want the bot to send a message when you pin a message
            print("sending pin notification")
            await last_pinned.channel.send(
                "See oldest pinned message in " + channel.guild.get_channel(int(pins_channel)).mention)
            await last_pinned.unpin()
            print("pinned message: " + channelPins[0].jump_url)
            print("archived message: " + last_pinned.jump_url)
    except Exception as e: print(e)


# TODO Replace TOKEN with the token from discord developer portal 
#client.run('TOKEN')

# TODO If using GitHub diff deployment on HeroKu comment out the above line with '#' and remove '#' from the line below to uncomment it. 
client.run(os.environ.get('TOKEN'))
