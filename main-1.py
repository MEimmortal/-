import os
import discord
import asyncio
import datetime
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.all()

#activity = discord.Streaming(name="YO!", url="https://www.twitch.tv/wallibear")
#activity = discord.Game(name=f"n!help in {len(client.guilds)}")
#activity = discord.Activity(name="with discord", type=5)
activity = discord.Game(game="Discord",name="with discord", type=5)

client = commands.Bot(command_prefix=["N!", "n!"], intents=intents, activity=activity, status=discord.Status.do_not_disturb)

prefix = "n!" or "N!"

@client.command()
async def pages(ctx):

  #  em = discord.Embed(title="Not available", description=f"Hello {ctx.author.name} you are in {ctx.author.guild.name} server!", colour=0x5865F2)
  #  em.add_field(name="Note", value="This command is not available right now!")
  #  em.set_thumbnail(url=f'{client.user.avatar_url}')
  #  em.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
  #  em.set_footer(text='© Nutcrack')
  #  em.timestamp = datetime.datetime.utcnow()

  #  await ctx.send(embed=em)

    contents = ["page 1","page 2", "page 3","page 4"]
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

@client.command()
async def userinfo(ctx, *, user: discord.Member=None):
    if isinstance(ctx.channel, discord.DMChannel):
      return
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
#    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
#    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)

@client.command()
async def info(ctx):
  async with ctx.typing():
    try:
      print(client.users)
#      await ctx.reply(f"{len(client.users)}")
    except:
      await ctx.reply(client.user)

@client.command()
async def serverinfo(ctx):

    role_count = len(ctx.guild.roles)
    list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
    staff_roles = ["Owner", "Head Dev", "Dev", "Head Admin", "Admins", "Moderators", "Community Helpers", "Members"]
        
    em = discord.Embed(timestamp=ctx.message.created_at, color=ctx.author.color)
    em.add_field(name='Name', value=f"{ctx.guild.name}", inline=False)
#    em.add_field(name='Owner', value=f"", inline=False)
    em.add_field(name='Verification Level', value=str(ctx.guild.verification_level), inline=False)
    em.add_field(name='Highest role', value=ctx.guild.roles[-2], inline=False)
    em.add_field(name='Contributers:', value="None")

    for r in staff_roles:
        role = discord.utils.get(ctx.guild.roles, name=r)
        if role:
            members = '\n'.join([member.name for member in role.members]) or "None"
            em.add_field(name=role.name, value=members)

    em.add_field(name='Number of roles', value=str(role_count), inline=False)
    em.add_field(name='Number Of Members', value=ctx.guild.member_count, inline=False)
    em.add_field(name='Bots:', value=(', '.join(list_of_bots)))
    em.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y at %H:%M:%S'), inline=False)
    em.set_thumbnail(url=ctx.guild.icon_url)
    em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    em.set_footer(text=client.user.name, icon_url=client.user.avatar_url)

    await ctx.send(embed=em)

@client.command()
async def k(ctx, member: discord.Member=None):
    if member:
        member = member
    elif member == None:
        member = ctx.author
    em = discord.Embed(color=discord.Color.green())
    em.set_thumbnail(url=f"{member.avatar_url_as(format=None, static_format='webp', size=1024)}")
    em.add_field(name="Member:", value=f"{member.mention}", inline=False)
    em.add_field(name="Member name", value=f"{member.name}", inline=False)
    em.add_field(name="Member id:", value=f"{member.id}", inline=False)
    em.add_field(name="Nickname:", value=f"{member.nick}", inline=False)
    em.add_field(name="Joined at:", value=f"{member.joined_at}", inline=False)
    roles = " ".join([role.mention for role in member.roles if role.name != "@everyone"])
    em.add_field(name="Roles:", value=f"{roles}", inline=False)
    em.set_footer(text="GG-GamerPub | auto-mod")

    await ctx.send(embed=em)

@client.command()
async def d(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
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
  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)

  await ctx.send(embed=embed)

@client.command()
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

@client.command()
async def yo(ctx):
  await ctx.reply(f"Yo {ctx.author.name} try out my new hacking command **'n!myip'**")

@client.event
async def on_ready():
  print(f"{client.user} in:")
  for guild in client.guilds:
    print(guild)
  
  print(
    f"-----\nLogged in as: {client.user.name} : {client.user.id}\n-----\nMy current prefix is: {client.command_prefix}\n-----\nInitialize Database\n-----",f"\n{client.user.name} in {len(client.guilds)} servers\n-----"
  )

keep_alive()
client.run(os.getenv("TOKEN"))