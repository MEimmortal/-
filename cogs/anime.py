import discord
import animec
import datetime
import random
import aiohttp
from io import BytesIO
from discord.utils import get
from discord.ext import commands

class Animec(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command()
  async def animec(self, ctx, *, search):
    async with ctx.typing():
      try:
        anime = animec.Anime(search)
      except:
        await ctx.reply(embed = discord.Embed(description = f"No Anime named '{search}' found.", color = discord.Color.red()))
        return
      em = discord.Embed(title=anime.title_english, url=anime.url, description=f"{anime.description}", color=0x5865F2)   
      em.add_field(name="Episodes", value=str(anime.episodes)) 
      em.add_field(name="Rating", value=str(anime.rating)) 
      em.add_field(name="Broadcast", value=str(anime.broadcast)) 
      em.add_field(name="Status", value=str(anime.status)) 
      em.add_field(name="Type", value=str(anime.type)) 
      em.add_field(name="NSFW status", value=anime.is_nsfw)
      em.set_thumbnail(url=anime.poster)
      await ctx.reply(embed=em)

  @commands.command()
  async def image(self, ctx, *, search):
    async with ctx.typing():
      try:
        char = animec.Charsearch(search)
        em = discord.Embed(title=char.title, url=char.url, color=0x5865F2)
        em.set_image(url=char.image_url)
        em.set_footer(text=", ".join(list(char.references.keys())[:2]))
        await ctx.reply(embed=em)
      except:
        await ctx.reply(embed = discord.Embed(description = f"No Anime character named '{search}' found.", color = discord.Color.red()))

  @commands.command()
  async def aninews(self, ctx, amount:int=3):
      news = animec.Aninews(amount)
      links = news.links
      titles = news.titles
      descriptions = news.description

      em = discord.Embed(title="Latest Anime News", color=0x5865F2, timestamp=datetime.datetime.utcnow())
      em.set_thumbnail(url=news.images[0])

      for i in range(amount):
        em.add_field(name=f"{i+1}) {titles[1]}", value = f"{descriptions[i][:200]}...\n[Read more]({links[i]})", inline=False)

      await ctx.reply(embed=em)

  @commands.command(aliases=['wave', 'ohaiyo'])
  async def hello(self, ctx):
        gifs = ['https://cdn.discordapp.com/attachments/102817255661772800/219512763607678976/large_1.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219512898563735552/large.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518948251664384/WgQWD.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518717426532352/tumblr_lnttzfSUM41qgcvsy.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519191290478592/tumblr_mf76erIF6s1qj96p1o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519729604231168/giphy_3.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519737971867649/63953d32c650703cded875ac601e765778ce90d0_hq.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519738781368321/17201a4342e901e5f1bc2a03ad487219c0434c22_hq.gif']
        msg = f':wave:\n'
        await ctx.send(msg+{random.choice(gifs)})

  @commands.command(aliases=['nepu', 'topnep'])
  async def nep(self, ctx):
        neps = ['https://cdn.discordapp.com/attachments/102817255661772800/219530759881359360/community_image_1421846157.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535598187184128/tumblr_nv25gtvX911ubsb68o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535698309545984/tumblr_mpub9tTuZl1rvrw2eo2_r1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535820430770176/dd9f3cc873f3e13fe098429388fc24242a545a21_hq.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535828773371904/tumblr_nl62nrrPar1u0bcbmo1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535828995538944/dUBNqIH.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535906942615553/b3886374588ec93849e1210449c4561fa699ff0d_hq.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536353841381376/tumblr_nl9wb2qMFD1u3qei8o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536345176080384/tumblr_njhahjh1DB1t0co30o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536356223877120/tumblr_njkq53Roep1t0co30o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536424121139210/tumblr_oalathnmFC1uskgfro1_400.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536451807739904/tumblr_nfg22lqmZ31rjwa86o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536686529380362/tumblr_o98bm76djb1vv3oz0o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219537181440475146/tumblr_mya4mdVhDv1rmk3cyo1_500.gif',
                'https://i.imgur.com/4xnJN9x.png',
                'https://i.imgur.com/bunWIWD.jpg']
        nepnep = ['topnep',
                  'Can\'t pep the nep',
                  'Flat is justice',
                  'nep nep nep nep nep nep nep nep nep nep nep',
                  'Nepgear > your waifu']
        await ctx.send(f"{random.choice(nepnep)}\n"+{random.choice(neps)})

  @commands.command(aliases=['headpat'])
  async def pat(self, ctx, member: discord.Member = None):
        gifs = ['https://gfycat.com/PoisedWindingCaecilian',
                'https://cdn.awwni.me/sou1.jpg',
                'https://i.imgur.com/Nzxa95W.gifv',
                'https://cdn.awwni.me/sk0x.png',
                'https://i.imgur.com/N0UIRkk.png',
                'https://cdn.awwni.me/r915.jpg',
                'https://i.imgur.com/VRViMGf.gifv',
                'https://i.imgur.com/73dNfOk.gifv',
                'https://i.imgur.com/UXAKjRc.jpg',
                'https://i.imgur.com/dzlDuNs.jpg',
                'https://i.imgur.com/hPR7SOt.gif',
                'https://i.imgur.com/IqGRUu4.gif',
                'https://68.media.tumblr.com/f95f14437809dfec8057b2bd525e6b4a/tumblr_omvkl2SzeK1ql0375o1_500.gif',
                'https://i.redd.it/0ffv8i3p1vrz.jpg',
                'http://i.imgur.com/3dzA6OU.png',
                'http://i.imgur.com/vkFKabZ.jpg',
                'https://i.imgur.com/Lb4p20s.jpg',
                'https://cdn.awwni.me/snot.jpg',
                'https://i.imgur.com/5yEOa6u.jpg',
                'https://i.redd.it/dc7oebkfsetz.jpg']

        if member == ctx.me:
            await ctx.send("You can't pat your self!")
        elif member is not None:
            msg = f"{ctx.author.mention} pat's {member.mention}\n"
            await ctx.send(msg+{random.choice(gifs)})

  @commands.command(aliases=['anilist'])
  async def anime(self, ctx, *, animeName: str):
        api = 'https://graphql.anilist.co'
        query = '''
        query ($name: String){
          Media(search: $name, type: ANIME) {
            id
            idMal
            description
            title {
              romaji
              english
            }
            coverImage {
              large
            }
            startDate {
              year
              month
              day
            }
            endDate {
              year
              month
              day
            }
            synonyms
            format
            status
            episodes
            duration
            nextAiringEpisode {
              episode
            }
            averageScore
            meanScore
            source
            genres
            tags {
              name
            }
            studios(isMain: true) {
              nodes {
                name
              }
            }
            siteUrl
          }
        }
        '''
        variables = {
            'name': animeName
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api, json={'query': query, 'variables': variables}, headers = self.client.userAgentHeaders) as r:
                if r.status == 200:
                    json = await r.json()
                    data = json['data']['Media']

                    embed = discord.Embed(color=ctx.author.top_role.colour)
                    embed.set_footer(text='API provided by AniList.co | ID: {}'.format(str(data['id'])))
                    embed.set_thumbnail(url=data['coverImage']['large'])
                    if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
                        embed.add_field(name='Titel', value=data['title']['romaji'], inline=False)
                    else:
                        embed.add_field(name='Titel', value='{} ({})'.format(data['title']['english'], data['title']['romaji']), inline=False)

                    #embed.add_field(name='Beschreibung', value=data['description'], inline=False)
                    if data['synonyms'] != []:
                        embed.add_field(name='Synonyme', value=', '.join(data['synonyms']), inline=True)

                    embed.add_field(name='Typ', value=data['format'].replace('_', ' ').title().replace('Tv', 'TV'), inline=True)
                    if data['episodes'] > 1:
                        embed.add_field(name='Folgen', value='{} à {} min'.format(data['episodes'], data['duration']), inline=True)
                    else:
                        embed.add_field(name='Dauer', value=str(data['duration']) + ' min', inline=True)

                    embed.add_field(name='Gestartet', value='{}.{}.{}'.format(data['startDate']['day'], data['startDate']['month'], data['startDate']['year']), inline=True)
                    if data['endDate']['day'] == None:
                        embed.add_field(name='Released Folgen', value=data['nextAiringEpisode']['episode'] - 1, inline=True)
                    elif data['episodes'] > 1:
                        embed.add_field(name='Beendet', value='{}.{}.{}'.format(data['endDate']['day'], data['endDate']['month'], data['endDate']['year']), inline=True)

                    embed.add_field(name='Status', value=data['status'].replace('_', ' ').title(), inline=True)

                    try:
                        embed.add_field(name='Haupt-Studio', value=data['studios']['nodes'][0]['name'], inline=True)
                    except IndexError:
                        pass
                    embed.add_field(name='Ø Score', value=data['averageScore'], inline=True)
                    embed.add_field(name='Genres', value=', '.join(data['genres']), inline=False)
                    tags = ''
                    for tag in data['tags']:
                        tags += tag['name'] + ', '
                    embed.add_field(name='Tags', value=tags[:-2], inline=False)
                    try:
                        embed.add_field(name='Adaptiert von', value=data['source'].replace('_', ' ').title(), inline=True)
                    except AttributeError:
                        pass

                    embed.add_field(name='AniList Link', value=data['siteUrl'], inline=False)
                    embed.add_field(name='MyAnimeList Link', value='https://myanimelist.net/anime/' + str(data['idMal']), inline=False)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(':x: Konnte keinen passenden Anime finden!')

  @commands.command()
  async def manga(self, ctx, *, mangaName: str):
        api = 'https://graphql.anilist.co'
        query = '''
        query ($name: String){
          Media(search: $name, type: MANGA) {
            id
            idMal
            description
            title {
              romaji
              english
            }
            coverImage {
              large
            }
            startDate {
              year
              month
              day
            }
            endDate {
              year
              month
              day
            }
            status
            chapters
            volumes
            averageScore
            meanScore
            genres
            tags {
              name
            }
            siteUrl
          }
        }
        '''
        variables = {
            'name': mangaName
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api, json={'query': query, 'variables': variables}, headers = self.client.userAgentHeaders) as r:
                if r.status == 200:
                    json = await r.json()
                    data = json['data']['Media']

                    embed = discord.Embed(color=ctx.author.top_role.colour)
                    embed.set_footer(text='API provided by AniList.co | ID: {}'.format(str(data['id'])))
                    embed.set_thumbnail(url=data['coverImage']['large'])
                    if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
                        embed.add_field(name='Titel', value=data['title']['romaji'], inline=False)
                    else:
                        embed.add_field(name='Titel', value='{} ({})'.format(data['title']['english'], data['title']['romaji']), inline=False)
                    #embed.add_field(name='Beschreibung', value=data['description'], inline=False)
                    if data['chapters'] != None:
                        # https://github.com/AniList/ApiV2-GraphQL-Docs/issues/47
                        embed.add_field(name='Kapitel', value=data['chapters'], inline=True)
                    if data['volumes'] != None:
                        embed.add_field(name='Bände', value=data['volumes'], inline=True)
                    embed.add_field(name='Gestartet', value='{}.{}.{}'.format(data['startDate']['day'], data['startDate']['month'], data['startDate']['year']), inline=True)
                    if data['endDate']['day'] != None:
                        embed.add_field(name='Beendet', value='{}.{}.{}'.format(data['endDate']['day'], data['endDate']['month'], data['endDate']['year']), inline=True)
                    embed.add_field(name='Status', value=data['status'].replace('_', ' ').title(), inline=True)
                    embed.add_field(name='Ø Score', value=data['averageScore'], inline=True)
                    embed.add_field(name='Genres', value=', '.join(data['genres']), inline=False)
                    tags = ''
                    for tag in data['tags']:
                        tags += tag['name'] + ', '
                    embed.add_field(name='Tags', value=tags[:-2], inline=False)
                    embed.add_field(name='AniList Link', value=data['siteUrl'], inline=False)
                    embed.add_field(name='MyAnimeList Link', value='https://myanimelist.net/anime/' + str(data['idMal']), inline=False)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(':x: Konnte keinen passenden Manga finden!')

def setup(client):
  client.add_cog(Animec(client))