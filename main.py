import os
import discord
import asyncio
import datetime
import random
import aiohttp
import json
import requests
import time
import io
import praw
from bs4 import BeautifulSoup
from discord.ext import commands
from keep_alive import keep_alive

activity = discord.Streaming(name="Follow MEimmortal007", url="https://www.twitch.tv/MEimmortal007")
#activity = discord.Game(name=f"n!help in {len(client.guilds)}")
#activity = discord.Activity(name="with discord", type=5)
#activity = discord.Game(game="Discord",name="with discord", type=5)

client = commands.Bot(command_prefix=["N!", "n!"], intents=discord.Intents.all(), activity=activity, status=discord.Status.do_not_disturb, help_command=None)

#client.remove_command("help")

prefix = "n!" or "N!"

owner = "<@!812912547937255434>"

async def get_help():
  em = discord.Embed(title="Help!", description=f"Help command for {client.user.name}!", color=0x5865F2)
  em.set_footer(text=f"Total commands [{len(client.commands)}]")
  em.timestamp = datetime.datetime.utcnow()
  for command in client.walk_commands():
    description = command.description
    if not description or description is None or description == "":
      description = 'No description was provided'
    em.add_field(name=f"`{prefix}{command.name}{command.signature if command.signature is not None else ''}`", value=description)
  return em

@client.event
async def on_message(message):
#  if owner.user.mentioned_in(message):
#    await message.guild.ban(message.author)
#    await message.author.send(f"> **First why did you ping <@!812912547937255434>?**\n> _I told you if you ping me you die!_\n> **Fuck you {message.author.mention}**\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you\n**Hahaha**\nFuck you")
  if message.content == "<@908917461489975307>":
    em = await get_help()
    await message.channel.send(embed=em)

  await client.process_commands(message)

@client.command(description = f"Help command for Nutcrack!")
async def help(ctx):
  em = await get_help()
  await ctx.send(embed=em)

@client.command(description = "Some random pages")
async def pages(ctx):

  #  em = discord.Embed(title="Not available", description=f"Hello {ctx.author.name} you are in {ctx.author.guild.name} server!", colour=0x5865F2)
  #  em.add_field(name="Note", value="This command is not available right now!")
  #  em.set_thumbnail(url=f'{client.user.avatar_url}')
  #  em.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
  #  em.set_footer(text='© Nutcrack')
  #  em.timestamp = datetime.datetime.utcnow()

  #  await ctx.send(embed=em)
    gifs = ['https://cdn.discordapp.com/attachments/102817255661772800/219512763607678976/large_1.gif',
    'https://cdn.discordapp.com/attachments/102817255661772800/219512898563735552/large.gif',
    'https://cdn.discordapp.com/attachments/102817255661772800/219518948251664384/WgQWD.gif',
    'https://cdn.discordapp.com/attachments/102817255661772800/219518717426532352/tumblr_lnttzfSUM41qgcvsy.gif',
    'https://cdn.discordapp.com/attachments/102817255661772800/219519191290478592/tumblr_mf76erIF6s1qj96p1o1_500.gif',
    'https://cdn.discordapp.com/attachments/102817255661772800/219519729604231168/giphy_3.gif',
    'https://cdn.discordapp.com/attachments/102817255661772800/219519737971867649/63953d32c650703cded875ac601e765778ce90d0_hq.gif',
    'https://cdn.discordapp.com/attachments/102817255661772800/219519738781368321/17201a4342e901e5f1bc2a03ad487219c0434c22_hq.gif']
  
    contents = ["\nHello!","\nHello its me again!","\nDidn't you already have enough\nI sware if you got to the next one...","https://media0.giphy.com/media/Ju7l5y9osyymQ/200.gif"]
    pages = 4
    cur_page = 1
    message = await ctx.send(f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            break

@client.command(description = "This command will yo you back")
async def yo(ctx, something=None):
  if not something:
    await ctx.reply(f"Yo {ctx.author.name}")
  else:
    print(something)
    await ctx.reply(f"Yo {ctx.author.name}")

@client.command(description="Owner's command (only)", hidden=True)
@commands.is_owner()
async def loop(ctx, l="**Hahaha**"):
  v = True
  while (v):
    await ctx.send(l)

@client.command(description = "Nuke channel or server (administrator)") 
@commands.has_permissions(administrator=True)
async def nuke(ctx, channel: discord.TextChannel = None):
    if channel == None: 
        await ctx.send("You did not mention a channel!")
        return

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    if nuke_channel is not None:
        new_channel = await nuke_channel.clone(reason="Has been Nuked!")
        await nuke_channel.delete()
        await new_channel.send("THIS CHANNEL HAS BEEN NUKED!")
        await ctx.send("Nuked the Channel sucessfully!")

    else:
        await ctx.send(f"No channel named {channel.name} was found!")

@client.command(aliases=['make_role'])
@commands.has_permissions(manage_roles=True)
async def create_role(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'Role `{name}` has been created')

@client.command()
async def ok(ctx):
  await ctx.reply(embed=discord.Embed(title="**KO!**"))

@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None, setting=None):
    if setting == '--server':
      for channel in ctx.guild.channels:
        await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked {channel.name} with --server", send_messages=False)
      await ctx.send("Locked down server")
    if channel is None:
      channel = ctx.message.channel
    await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked {channel.name}", send_messages=False)
    await ctx.send("Locked channel down")

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None, setting=None):
    if setting == '--server':
      for channel in ctx.guild.channels:
        await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} unlocked {channel.name} with --server", send_messages=True)
      await ctx.send(f"Unlocked {ctx.guild.name}")
    if channel is None:
      channel = ctx.message.channel
    await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} unlocked {channel.name}", send_messages=True)
    await ctx.send(f"unlocked {channel}")

@client.command()
async def serverowner(ctx):
  owner = ctx.guild.owner
  await ctx.reply(embed=discord.Embed(title=f"{ctx.guild.name} Owner", description=f"This server owner is ('{owner}')[Nick = '{owner.nick}']", inline=True))

@client.command()
async def serverinfo(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
#  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Server Information",
      description=description,
      color=discord.Color.blue()
    )
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
#  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)

  await ctx.send(embed=embed)

@client.command()
async def serverid(ctx):
  id = ctx.guild.id
  await ctx.reply(embed=discord.Embed(title=f"{ctx.guild.name} Id", description=f"The Server Id is ['{id}']", inline=True))

@client.command()
async def serveravatar(ctx):
  icon = str(ctx.guild.icon_url)  
  em = discord.Embed(title="Server avatar")
  em.set_thumbnail(url=icon)
  await ctx.replt(embed=em)

@client.command()
async def serverregion(ctx):
  region = ctx.guild.region
  await ctx.reply(embed=discord.Embed(title=f"{ctx.guild.name}Region", description=f"The Server region is ['{region}']", inline=True))

@client.command()
async def cockroach(ctx):
  await ctx.reply("https://tenor.com/view/roach-dancing-cockroach-dance-spinning-gif-17661669")

@client.command()
async def servers(ctx):
  await ctx.reply(embed=discord.Embed(title="**Servers**", description=f"{client.user.name} in **{len(client.guilds)} servers**!"))

@client.command()
async def hi(ctx):
  await ctx.send("᲼᲼")

@client.command(aliases=['nitro'])
async def freenitro(ctx):
  await ctx.reply("**Here Free Nitro!**\n||https://discord.gift/jrVPPaK7dB9HXawfPswz3uS9||\n**Lmao!**")

@client.command(pass_context=True, aliases=["announcement"])
@commands.has_permissions(manage_channels=True)
async def announce(ctx, channel : discord.TextChannel, *, message):

  if not channel:
    await ctx.reply("Failed Sending Announcement! ❌\nYou didn't mention a channel to send the announcement")
    return
  
  if not message:
    await ctx.reply("failed sending an Announcement! ❌")
    return

  msg = await ctx.channel.send(embed=discord.Embed(title=f"{ctx.author.mention} are you sure?"))
  await msg.add_reaction(u"\u2705")
  await msg.add_reaction(u"\U0001F6AB")

  try:
    reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in [u"\u2705", u"\U0001F6AB"], timeout=30.0)


  except asyncio.TimeoutError:
    await ctx.channel.send("Please don't ignore me!")
    return

  else:
    if reaction.emoji == u"\u2705":
      await channel.send(message)
      await ctx.reply(":white_check_mark: Announcement have been sent!")
      return
            
    else:
      await ctx.channel.send("Ok the announcement has been canceled!")
      return

@client.command(aliases=["giphy"],pass_context=True)
async def gif(ctx, *, search=""):
    try:
        author = ctx.message.author
        user_name = author.name
        session = aiohttp.ClientSession()
        print(search)
        if search == '':
            embed = discord.Embed(title=f"{user_name} Random GIF",
                                    description=f"", color=3447003)
            response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=PgVCpPdQHEIaeUcBrpNGXKcnuQS6AVS0')
            data = json.loads(await response.text())
            embed.set_image(url=data['data']['images']['original']['url'])
        else:
            embed = discord.Embed(title=f"{user_name} GIF : **{search}**  ",
                                    description=f"", color=3447003)
            search.replace(' ', '%20')
            response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=PgVCpPdQHEIaeUcBrpNGXKcnuQS6AVS0&limit=10')
            await session.close()
            data = json.loads(await response.text())
            gif_choice = random.randint(0, 9)
            embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])
        await session.close()
        await ctx.send(embed=embed)
    except:
        msg = f"{ctx.message.author.mention} GIF not found for **{search}**" 
        await ctx.send(msg)

@client.command()
async def roast(ctx, member : discord.Member = None):
  async with ctx.typing():

    roasts = ["At least my mom pretends to love me",
        "Bards will chant parables of your legendary stupidity for centuries, You",
        "Don't play hard to get when you are hard to want",
        "Don't you worry your pretty little head about it. The operative word being little. Not pretty.",
        "Get a damn life you uncultured cranberry fucknut.",
        "God wasted a good asshole when he put teeth in your mouth",
        "Goddamn did your parents dodge a bullet when they abandoned you.",
        "I bet your dick is an innie and your belly button an outtie.",
        "I can't even call you Fucking Ugly, because Nature has already beaten me to it.",
        "I cant wait to forget you.",
        "I curse the vagina that farted you out.",
        "I don't have the time, or the crayons to explain this to you.",
        "I FART IN YOUR GENERAL DIRECTION",
        "I fucking hate the way you laugh.",
        "I hope you win the lottery and lose your ticket.",
        "I once smelled a dog fart that had more cunning, personality, and charm than you.",
        "I shouldn't roast you, I can't imagine the pain you go through with that face!",
        "I want to call you a douche, but that would be unfair and unrealistic. Douches are often found near vaginas.",
        "I wonder if you'd be able to speak more clearly if your parents were second cousins instead of first.",
        "I would call you a cunt, but you lack the warmth or the depth.",
        "I would challenge you to a battle of wits, but it seems you come unarmed",
        "I would rather be friends with Ajit Pai than you.",
        "I'd love to stay and chat but I'd rather have type-2 diabetes",
        "I'm just surprised you haven't yet retired from being a butt pirate.",
        "I'm not mad. I'm just... disappointed.",
        "I've never met someone who's at once so thoughtless, selfish, and uncaring of other people's interests, while also having such lame and boring interests of his own. You don't have friends, because you shouldn't.",
        "I’m betting your keyboard is filthy as fuck now from all that Cheeto-dust finger typing, you goddamn weaboo shut in. ",
        "If 'unenthusiastic handjob' had a face, your profile picture would be it.",
        "If there was a single intelligent thought in your head it would have died from loneliness.",
        "If you were a potato you'd be a stupid potato.",
        "If you were an inanimate object, you'd be a participation trophy.",
        "If you where any stupider we'd have to water you",
        "If you're dad wasn't so much of a pussy, he'd have come out of the closet before he had you.",
        "It's a joke, not a dick. You don't have to take it so hard.",
        "Jesus Christ it looks like your face was on fire and someone tried to put it out with an ice pick",
        "May the fleas of ten thousand camels live happily upon your buttocks",
        "Maybe if you eat all that makeup you will be beautiful on the inside.",
        "Mr. Rogers would be disappointed in you.",
        "Next time, don't take a laxative before you type because you just took a steaming stinking dump right on the page. Now wipe that shit up and don't fuck it up like your life.",
        "Not even your dog loves you. He's just faking it.",
        "Once upon a time, Santa Clause was asked what he thought of your mom, your sister and your grandma, and thus his catchphrase was born.",
        "People don't even pity you.",
        "People like you are the reason God doesn't talk to us anymore",
        "Take my lowest priority and put yourself beneath it.",
        "The IQ test only goes down to zero but you make a really compelling case for negative numbers",
        "the only thing you're fucking is natural selection",
        "There are two ugly people in this chat, and you're both of them.",
        "There will never be enough middle fingers in this world for You",
        "They don't make a short enough bus in the Continental United States for a person like you.",
        "Those aren't acne scars, those are marks from the hanger.",
        "Twelve must be difficult for you. I don’t mean BEING twelve, I mean that being your IQ.",
        "We all dislike you, but not quite enough that we bother to think about you.",
        "Were you born a cunt, or is it something you have to recommit yourself to every morning?",
        "What's the difference between three dicks and a joke? You can't take a joke.",
        "When you die, people will struggle to think of nice things to say about you.",
        "Where'd ya get those pants? The toilet store?",
        "Why do you sound like you suck too many cocks?",
        "Why don’t you crawl back to whatever micro-organism cesspool you came from, and try not to breath any of our oxygen on the way there",
        "WHY SHOULD I LISTEN TO YOU ARE SO FAT THAT YOU CAN'T POO OR PEE YOU STINK LYRE YOU HAVE A CRUSH ON POO﻿",
        "You are a pizza burn on the roof of the world's mouth.",
        "You are a stupid.",
        "You are dumber than a block of wood and not nearly as useful",
        "You are like the end piece of bread in a loaf, everyone touches you but no one wants you",
        "You have a face made for radio",
        "You have more dick in your personality than you do in your pants",
        "You have the face of a bulldog licking piss off a stinging nettle.",
        "You know they say 90% of dust is dead human skin? That's what you are to me.",
        "You know, one of the many, many things that confuses me about you is that you remain unmurdered.",
        "You look like your father would be disappointed in you. If he stayed.",
        "You losing your virginity is like a summer squash growing in the middle of winter. Never happening.",
        "You may think people like being around you- but remember this: there is a difference between being liked and being tolerated.",
        "You might want to get a colonoscopy for all that butthurt",
        "You need to go up to your daddy, get on your knees and apologize to each and every brother and sister that didn't make it to your mother's egg before you",
        "You should put a condom on your head, because if you're going to act like a dick you better dress like one too.",
        "You stuck up, half-witted, scruffy looking nerf herder!",
        "You were birthed out your mothers ass because her cunt was too busy.",
        "You're an example of why animals eat their young.",
        "You're impossible to underestimate",
        "You're kinda like Rapunzel except instead of letting down your hair you let down everyone in your life",
        "You're like a penny on the floor of a public restroom - filthy, untouchable and practically worthless.",
        "You're like a square blade, all edge and no point.",
        "You're looking well for a man twice your age! Any word on the aneurism?",
        "You're not pretty enough to be this dumb",
        "You're objectively unattractive.",
        "You're so dense, light bends around you.",
        "You're so salty you would sink in the Dead Sea",
        "You're so stupid you couldn't pour piss out of a boot if the directions were written on the heel",
        "You're such a pussy that fucking you wouldnt be gay.",
        "You're ugly when you cry.",
        "Your birth certificate is an apology letter from the abortion clinic.",
        "Your memes are trash.",
        "Your mother may have told you that you could be anything you wanted, but a douchebag wasn't what she meant.",
        "Your mother was a hamster, and your father reeks of elderberries!",
        "Your penis is smaller than the payment a homeless orphan in Mongolia received for stitching my shoes."]

    try:
      if member == ctx.author:
        await ctx.reply("You can't roast yourself!")
        return
      if not member.bot:
        await ctx.reply(f"{random.choice(roasts)}")
      else:
        await ctx.reply(f"You can't roast {member} its a bot you moron!")
    except:
      await ctx.reply(f"You can't roast {member}")

@client.command()
async def addreaction(ctx, channel : discord.TextChannel=None, msgid : int=None, emoji=None):
  if not channel:
    await ctx.reply("You didn't mention a channel!")
    return
  if not msgid:
    await ctx.reply("You didn't add a message id!")
    return
  if not emoji:
    await ctx.reply(f"You didn't add a emoji to react to the message!\n{emoji} does this look emoji to you?")
  message = await channel.fetch_message(msgid)
  await message.add_reaction(emoji)

@client.command()
async def add(ctx, add1 : int=0, add2 : int=0, add3 : int=0, add4 : int=0):
  if add1 == 0:
    await ctx.reply("Add your first number first!")
    return
  if add2 == 0:
    await ctx.reply("Add you second number to add to the first number!")
    return
  try:
    res = add1+add2+add3+add4
    await ctx.reply(f"Answer is [{res}]")
  except:
    await ctx.reply("I am bad at math!")

@client.command()
async def multiply(ctx, mul1 : int=0, mul2 : int=0, mul3 : int=1, mul4 : int=1):
  if mul1 == 0:
    await ctx.reply("Add your first number first!")
    return
  if mul2 == 0:
    await ctx.reply("Add you second number to add to the first number!")
    return
  try:
    res = mul1*mul2*mul3*mul4
    await ctx.reply(f"Answer is [{res}]")
  except:
    await ctx.reply("I am bad at math!")

@client.command()
async def status(ctx, member : discord.Member=None):
  if not member:
    member = ctx.author
  embed = discord.Embed(title=f"{member.mention}'s Status")
  embed.add_field(name='Status Now', value=member.status)
  await ctx.send(embed=embed)

@client.command()
async def noice(ctx, member : discord.Member=None):
  if not member:
    member = ctx.author
  session = aiohttp.ClientSession()
  search = "noice"
  search.replace(' ', '%20')
  response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=PgVCpPdQHEIaeUcBrpNGXKcnuQS6AVS0&limit=10')
  await session.close()
  data = json.loads(await response.text())
  gif_choice = random.randint(0, 9)
  embed = discord.Embed(title=f"**{member.mention} Noice!**")
  embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])
  await ctx.reply(embed=embed)

@client.command(hidden=True)
@commands.is_owner()
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await client.fetch_user(user_id)
            await target.send(args)

            await ctx.channel.send("'" + args + "' sent to: " + target.name)

        except:
            await ctx.channel.send("Couldn't dm the given user.")
        

    else:
        await ctx.channel.send("You didn't provide a user's id and/or a message.")

@client.command()
async def q(ctx):
  msg = await ctx.channel.send(embed=discord.Embed(title=f"{ctx.author.mention} am I in your server?"))
  await msg.add_reaction(u"\u2705")
  await msg.add_reaction(u"\U0001F6AB")

  try:
        reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in [u"\u2705", u"\U0001F6AB"], timeout=30.0)


  except asyncio.TimeoutError:
        await ctx.channel.send("Ouch you ignored me.")

  else:
        if reaction.emoji == u"\u2705":
            await ctx.channel.send("Yaaaaa lets gooo..")

        else:
            await ctx.channel.send("Ouch, that hurts...\nAdd me right now!")    

#@client.command(hidden=True)
#async def hentai(ctx, *,type=""):
#        if ctx.message.channel.nsfw:
#            api_types = ['femdom', 'classic', 'ngif', 'erofeet', 'erok', 'les',
#                         'hololewd', 'lewdk', 'keta', 'feetg', 'nsfw_neko_gif', 'eroyuri',
#                         'tits', 'pussy_jpg', 'cum_jpg', 'pussy', 'lewdkemo', 'lewd', 'cum', 'spank',
#                         'smallboobs', 'Random_hentai_gif', 'nsfw_avatar', 'hug', 'gecg', 'boobs', 'pat',
#                         'feet', 'smug', 'kemonomimi', 'solog', 'holo', 'bj', 'woof', 'yuri', 'trap', 'anal',
#                         'blowjob', 'holoero', 'feed', 'gasm', 'hentai', 'futanari', 'ero', 'solo', 'pwankg', 'eron',
#                         'erokemo']
#            if type in api_types:
#                try:
#                    req = requests.get(f'https://nekos.life/api/v2/img/{type}')
#                    if req.status_code != 200:
#                        print("Unable to obtain image")
#                    apijson = json.loads(req.text)
#                    url = apijson["url"]
#
#                    message = await ctx.send("Wait")
#                    async with aiohttp.ClientSession() as session:
#                        async with session.get(url) as resp:
#                            data = io.BytesIO(await resp.read())
#                            #await ctx.send(
#                                #file=discord.File(data, f'SPOILER_HENTAI.{url.split("/")[-1].split(".")[-1]}'))
#                            #await message.delete()
#                            await ctx.send(data)
#                except:
#                    await ctx.send("Error")
#            else:
#                await ctx.send("Error")
#        else:
#            await ctx.send("This command only works in NSFW channels!")

@client.command()
async def get(ctx):
  i = requests.get('https://api.ipify.org').text
  await ctx.send("Here is my ip: " + i)

@client.command(hidden=True)
#@commands.is_owner()
async def hentai(ctx, *, search):
  #if not commands.is_owner(): 
    em = discord.Embed(title="Not available", description=f"Hello {ctx.author.name} you are in {ctx.author.guild.name} server!", colour=0x5865F2)
    em.add_field(name="Note", value="This command is not available right now!")
    em.set_thumbnail(url=f'{client.user.avatar_url}')
    em.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
    em.set_footer(text='© Nutcrack')
    em.timestamp = datetime.datetime.utcnow()

  #  return await ctx.send(embed=em)
  #else:
  #  return await ctx.send(embed=em)
#  if ctx.message.channel.nsfw:
    async with ctx.typing():
      if not search:
        await ctx.reply("Please enter hentai type to search!")
      try:
        await ctx.message.delete()
        req = requests.get(f"https://nekobot.xyz/api/image?type={search}").json()
        url = req['message']
        print(url)
        embed = discord.Embed(
          title= search,
          color = req['color']
        )
        embed.set_image(url=url)
        await ctx.send(f"{url}", delete_after=10)
        #await ctx.send(embed=embed)
      except:
        await ctx.send("Sorry I can't send NSFW right now!", delete_after=10)
#  else:
#    await ctx.send("This command only works in NSFW channels!")

@client.command(aliases=["Serverinvite", "si","joinlink","link"],pass_context=True)
async def serverinvite(ctx,*,message=""):
  invitelinknew = await ctx.channel.create_invite(destination = ctx.message.channel, xkcd = True)
  embed = discord.Embed(title=f"INVITE LINK TO JOIN THIS SERVER",
  description=f"Here is an instant invite to your server: {invitelinknew}", color=3447003)
  embed.set_image(url="https://i.imgur.com/u07ktga.png")
  await ctx.send(embed=embed)

@client.command()
#@commands.has_permissions(manage_messages=True) 
@commands.is_owner()
async def reply(ctx, channel : discord.TextChannel=None, id_ : int=None, *, reply_msg=None):
  if not channel:
    await ctx.reply("You need to add the channel to reply!")
    return
  if not id_:
    await ctx.reply("You need to add message id to reply!")
    return
  if not reply_msg:
    await ctx.reply("What do you want to reply?")
    return
  try:
    new_msg = await channel.fetch_message(id_)
    await ctx.message.delete()
    await new_msg.reply(f"{reply_msg}")
  except:
    await ctx.reply(f"The id  was entered incorrectly.\nYou can type `{prefix}help reply` if you are not sure what to do!")
    return

@client.command()
async def now(ctx):
  await ctx.send(time.time())
#  await ctx.send(f"<t:{time.time()}:R>")

@client.command()
async def embed(ctx, title=None, description=None, color=None):
  if not title:
    await ctx.reply("Please add a title to the embed and try again!")
    return

  if color is not None:
    try:
      color = await commands.ColorConverter().convert(color)
    except:
      color = None
  if color is None:
    color = discord.Color.default()
    # Generating an embed
  emb = discord.Embed(color=color)
  if title is not None:
    emb.title = title
  if description is not None:
    emb.description = description
    # Sending the output
  await ctx.send(embed=emb)

@client.command()
async def edit(ctx, msg_id: int=None, channel: discord.TextChannel=None, edit_msg: str=None):
  try:
    if not msg_id:
      await ctx.reply("Please put a message id to edit and try again!")
      return
    elif not channel:
      channel = ctx.channel
    elif not edit_msg:
      await ctx.reply( )
    msg = await channel.fetch_message(msg_id)
    await msg.edit(content=edit_msg)
  except:
    await ctx.send("Sorry, coudn't edit the message!")

@client.command()
async def k(ctx):
  return
  async with ctx.typing():
    reddit = praw.Reddit(client_id=os.environ['client_id'],
    client_secret=os.environ['client_secret'],
    user_agent='</BOT>')
    
    memes_submissions = reddit.subreddit('Bigtittedgirls').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
      submission = next(x for x in memes_submissions if not x.stickied)
      
      embed = discord.Embed(
        title = submission.title,
        color = 0x5865F2
      )
      embed.set_image(url=submission.url)
      embed.set_footer(text=f"{submission.subreddit}")
      embed.timestamp = datetime.datetime.utcnow()
      
      await ctx.send(embed=embed)

@client.command()
async def avatar(ctx, member : discord.Member=None):
  if not member:
    member = ctx.author
 
  em = discord.Embed(title=f"{member.name} avatar", description=f"Here is your avatar!", color=0x5865F2)
  em.set_image(url=member.avatar_url)
  em.set_footer(text=f'{member.guild.name}', icon_url=f'{member.guild.icon_url}')
  em.timestamp = datetime.datetime.utcnow()

  await ctx.reply(embed=em)

@client.event
async def on_ready():
  print(f"{client.user} in:")
  for guild in client.guilds:
    print(len(guild.members))
  i = requests.get('https://api.ipify.org').text
  print(
    f"-----\nLogged in as: {client.user.name} : {client.user.id}\n-----\nMy current prefix is: {client.command_prefix}\n-----\nTotal commands [{len(client.commands)}]\n-----\n{client.user.name} in {len(client.guilds)} servers\n-----\nMy ip: {i}"
  )
  #await client.change_presence(status=discord.Status.dnd, activity = discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers | 2467 users"))

#async def background_task():
#    await client.wait_until_ready()
#    counter = 0
#    channel = client.get_channel(919787906489528341) # Insert channel ID here
#    while not client.is_closed():
#        counter += 1
#        await channel.send(counter)
#        await asyncio.sleep(1)

#client.loop.create_task(background_task())
keep_alive()
client.run(os.getenv("TOKEN"))