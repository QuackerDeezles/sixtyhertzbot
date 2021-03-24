import discord
from discord.ext import commands
import os
import json

import asyncio
from mooncanedit import gdshopToken, gdshopGoldToken, list_desc, competition_info
from roleStuff import demonsROLE, gdrolesROLE, pointercrateROLE, competitionROLE, collabROLE, moderationsROLE, perksROLE, miscROLE, memberRolesROLE, leaderboardToppers
# import keep_alive
from discord_slash import SlashCommand, SlashContext
from itertools import cycle
# from flask import Flask
from discord_slash.utils import manage_commands

intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = commands.Bot(command_prefix="!", intents=intents)
GOLD_TOKEN_EMOJI = '<:goldtoken:805527920512204821>'
slash = SlashCommand(client,sync_commands=True)
verifiedEMOJI = "<a:verified:805929172451065879>"
redloading = '<a:red_loading:805930785919467521>'



guild_ids = [782651282128896020,757383943116030074] # Put your server ID in this array.


@slash.slash(name="ping", description="Returns the latency of the bot", guild_ids=guild_ids)
async def _ping(ctx): # Defines a new "context" (ctx) command called "ping."
    await ctx.respond()
    await ctx.send(f"Pong! ({int(client.latency*1000)}ms)")
@slash.slash(name="wealth", 
            description="Displays your current wealth balance in tokens.",
            options=[manage_commands.create_option(
                name = "member",
                description = "Person whose wealth you want to check",
                option_type = 6,
                required = False
              )],
            guild_ids=guild_ids)
async def _wealth(ctx, member = None): # Defines a new "context" (ctx) command called "ping."
    
    await ctx.respond()
    if not member:
      member = ctx.author
    with open('tokens.json', 'r') as f:
        users = json.load(f)
    await open_account(users, member)
    tokens = users[str(member.id)]['tokens']
    goldtokens = users[str(member.id)]['gold tokens']
    with open('tokens.json', 'w') as f:
        json.dump(users, f)
    desc = f":coin: **Tokens:** {tokens} \n{GOLD_TOKEN_EMOJI} **Gold Tokens:** {goldtokens}  "
    em = discord.Embed(title='Token Wealth',
                       description=desc,
                       color=discord.Color.green())
    em.set_author(name=member.name, icon_url=member.avatar_url)
    await ctx.send(embed=em)

@slash.slash(name="shop", 
            description="Shows the current token shop.",
            guild_ids=guild_ids)
async def _gdshop(ctx): # Defines a new "context" (ctx) command called "ping."
    
    await ctx.respond()
    embed = discord.Embed(title='60hz Gang Shop', color=discord.Color.purple())
    embed.add_field(name='Normal Shop', value=gdshopToken)
    embed.add_field(name='Special Shop (1 Gold Token Each)',
                    value=gdshopGoldToken)
    await ctx.send(embed=embed)

@client.command(aliases=['shop', '60hzshop'])
async def gdshop(ctx):
    embed = discord.Embed(title='60hz Gang Shop', color=discord.Color.purple())
    embed.add_field(name='Normal Shop', value=gdshopToken)
    embed.add_field(name='Special Shop (1 Gold Token Each)',
                    value=gdshopGoldToken)
    await ctx.send(embed=embed)

@client.command(aliases=['bal', 'balance'])
async def wealth(ctx, *, person: discord.Member = None):
    if not person:
        person = ctx.author
    with open('tokens.json', 'r') as f:
        users = json.load(f)
    await open_account(users, person)
    tokens = users[str(person.id)]['tokens']
    goldtokens = users[str(person.id)]['gold tokens']
    with open('tokens.json', 'w') as f:
        json.dump(users, f)
    desc = f":coin: **Tokens:** {tokens} \n{GOLD_TOKEN_EMOJI} **Gold Tokens:** {goldtokens}  "
    em = discord.Embed(title=f'Token Wealth',
                       description=desc,
                       color=discord.Color.green())
    em.set_author(name=person.name, icon_url=person.avatar_url)
    await ctx.send(embed=em)


@wealth.error
async def wealth_error(ctx, error):
    await ctx.send(error)

getHelpMenudesc = """
`!help` - This help command
`!gdshop` - Shows the current shop where you can buy items
`!wealth` - Your current wealth in tokens
``
"""



# Slash Commands

# options = [
#   {
#     "name" : "amount",
#     "description" : "The amount of tokens you want to give",
#     "required" : True,
#     "type" : 4
#   }
# ]




# @slash.slash(name = "give", description = "Gives tokens to a member", guild_ids = [757383943116030074], options = options)
# async def give(ctx : SlashContext, amount):
#   await ctx.send("I didn't give anything to anyone.")
@slash.slash(
  name="give",
  description="Allows you to give tokens to members. (Only Server Admins can use.)",
  options=[manage_commands.create_option(
    name = "receiver",
    description = "Person who you want to give tokens to",
    option_type = 6,
    required = True
  ),
  manage_commands.create_option(
    name = "amount",
    description = "The amount of tokens you want to give",
    option_type = 4,
    required = True,
  ),
  manage_commands.create_option(
    name = "token_type",
    description = "The type of token you want to give",
    option_type = 3,
    required = True,
    choices = [
      manage_commands.create_choice("Regular Tokens","Regular Tokens"),
      manage_commands.create_choice("Gold Tokens","Gold Tokens")
    ]
  )
  ,
  manage_commands.create_option(
    name = "reason",
    description = "The reason why you want to give these tokens",
    option_type = 3,
    required = True,
  )
  ]
  
  ,
  guild_ids=guild_ids
  #channel_ids = [805878707012108288,759974319799140412]
  )

async def _give(ctx,receiver,amount,token_type, reason):
  if ctx.author.guild_permissions.administrator:

    await ctx.respond()
    tokenlog = client.get_channel(805951549653778473)
    with open('tokens.json', 'r') as f:
        users = json.load(f)
    await open_account(users, receiver)
    if token_type.lower() == 'gold tokens':
      await change_tokens(users, receiver, amount, 'gold tokens')
      em = discord.Embed(
          title=f'{verifiedEMOJI} Successful Transfer',
          color=discord.Color.green())
      em.add_field(name='Giver', value=f'{ctx.author}', inline=False)
      em.add_field(name='Receiver', value=receiver, inline=False)
      em.add_field(name='Amount Given',
                    value=f'{amount} gold token(s)',
                    inline=False)
      em.add_field(name = 'Reason', value = f'{reason}',inline = False)
      await ctx.send(embed=em)
      await receiver.send(
          f"**{ctx.author.name}** has added **{amount} gold tokens** to your 60hz Competition Balance for {reason}"
      )
      await tokenlog.send(
          f"**{ctx.author.name}** has added **{amount} gold tokens** to **{receiver.name}**'s 60hz Competition Balance for {reason}"
    )
    else:
      await change_tokens(users, receiver, amount, 'tokens')
      em = discord.Embed(
          title=f'{verifiedEMOJI} Successful Transfer',
          color=discord.Color.green())
      em.add_field(name='Giver', value=f'{ctx.author}', inline=False)
      em.add_field(name='Receiver', value=receiver, inline=False)
      em.add_field(name='Amount Given',
                    value=f'{amount} token(s)',
                    inline=False)
      await ctx.send(embed=em)
      await receiver.send(
          f"**{ctx.author.name}** has added **{amount} tokens** to your 60hz Competition Balance for {reason}"
      )
      await tokenlog.send(
          f"**{ctx.author.name}** has added **{amount} regular tokens** to **{receiver.name}**'s 60hz Competition Balance for {reason}"
      )
    with open('tokens.json', 'w') as f:
      json.dump(users, f)
  else:
      await ctx.respond(eat = True)
      await ctx.send(content = "You do not have permission to use this command.", hidden=True)

@slash.slash(name = "whisper",
 description ="Test Command",
 options = [
   manage_commands.create_option(
    name = "message",
    description = "The message you want the bot to whisper",
    option_type = 3,
    required = True,
  )
 ])
async def _secret(ctx, message):
  await ctx.respond(eat=True)  # Again, this is optional, but still recommended to.
  await ctx.send(content = f"{message}", hidden=True)

@slash.slash(
  name="remove",
  description="Allows you to give remove tokens from members. (Only Server Admins can use.)",
  options=[manage_commands.create_option(
    name = "receiver",
    description = "Person who you want to give tokens to",
    option_type = 6,
    required = True
  ),
  manage_commands.create_option(
    name = "amount",
    description = "The amount of tokens you want to remove",
    option_type = 4,
    required = True,
  ),
  manage_commands.create_option(
    name = "token_type",
    description = "The type of token you want to remove",
    option_type = 3,
    required = True,
    choices = [
      manage_commands.create_choice("Regular Tokens","Regular Tokens"),
      manage_commands.create_choice("Gold Tokens","Gold Tokens")
    ]
  
  ),
  manage_commands.create_option(
    name = "reason",
    description = "The reason you want to remove tokens",
    option_type = 3,
    required = True
  )]
  ,
  guild_ids=guild_ids
  )
async def _remove(ctx,receiver,amount, token_type, reason):
  if ctx.author.guild_permissions.administrator:

    await ctx.respond()
    tokenlog = client.get_channel(805951549653778473)
    with open('tokens.json', 'r') as f:
        users = json.load(f)
    await open_account(users, receiver)
    if token_type.lower() == 'gold tokens':
      await change_tokens(users, receiver, amount * -1, 'gold tokens')
      em = discord.Embed(
          title=f'{verifiedEMOJI} Successful Transfer',
          color=discord.Color.green())
      em.add_field(name='Remover',
                    value=f'{ctx.author}',
                    inline=False)
      em.add_field(name='Member', value=receiver, inline=False)
      em.add_field(name='Amount Removed',
                    value=f'{amount} gold token(s)',
                    inline=False)
      await ctx.send(embed=em)
      await receiver.send(
          f"**{ctx.author.name}** has removed **{amount} gold tokens** from your 60hz Competition Balance for {reason}"
      )
      await tokenlog.send(
          f"**{ctx.author.name}** has removed **{amount} gold tokens** from **{receiver.name}**'s 60hz Competition Balance for {reason}"
      )
    
    else:
      await change_tokens(users, receiver, amount * -1, 'tokens')
      em = discord.Embed(
          title=f'{verifiedEMOJI} Successful Transfer',
          color=discord.Color.green())
      em.add_field(name='Giver', value=f'{ctx.author}', inline=False)
      em.add_field(name='Receiver', value=receiver, inline=False)
      em.add_field(name='Amount Removed',
                    value=f'{amount} token(s)',
                    inline=False)
      await ctx.send(embed=em)
      await receiver.send(
          f"**{ctx.author.name}** has removed **{amount} tokens** from your 60hz Competition Balance"
      )

      await tokenlog.send(
          f"**{ctx.author.name}** has removed **{amount} regular tokens** from **{receiver.name}**'s 60hz Competition Balance"
      )
    with open('tokens.json', 'w') as f:
      json.dump(users, f)
  else:
      await ctx.respond(eat = True)
      await ctx.send(content = "You do not have permission to use this command.", hidden=True)

@client.command(aliases=['donate', 'transfer', 'give'])
@commands.has_permissions(administrator=True)
async def giveTokens(ctx, receiver: discord.Member, *, grant: int):
    if str(ctx.guild.id) == '757383943116030074':
        #if grant > 200:
        #await ctx.send("You can't give that many tokens at once!")
        #else:
        tokenlog = client.get_channel(805951549653778473)
        with open('tokens.json', 'r') as f:
            users = json.load(f)
        await open_account(users, receiver)

        def check(m):
            return m.channel.id == ctx.channel.id and m.author.id == ctx.author.id

        await ctx.send(
            "Which token type do you want to give? (The receiver needs to have Dm's on to get the transaction receipt from the bot)"
        )
        try:

            tokenType = await client.wait_for("message",
                                              check=check,
                                              timeout=20)
            if tokenType.content.lower() == 'gold token':
                await change_tokens(users, receiver, grant, 'gold tokens')
                em = discord.Embed(
                    title=f'{verifiedEMOJI} Successful Transfer',
                    color=discord.Color.green())
                em.add_field(name='Giver', value=f'{ctx.author}', inline=False)
                em.add_field(name='Receiver', value=receiver, inline=False)
                em.add_field(name='Amount Given',
                             value=f'{grant} gold token(s)',
                             inline=False)
                await ctx.send(embed=em)
                await receiver.send(
                    f"**{ctx.author.name}** has added **{grant} gold tokens** to your 60hz Competition Balance"
                )
                await tokenlog.send(
                    f"**{ctx.author.name}** has added **{grant} gold tokens** to **{receiver.name}**'s 60hz Competition Balance"
                )
            elif (tokenType.content.lower()
                  == 'token') or (tokenType.content.lower()
                                  == 'regular token'):
                await change_tokens(users, receiver, grant, 'tokens')
                em = discord.Embed(
                    title=f'{verifiedEMOJI} Successful Transfer',
                    color=discord.Color.green())
                em.add_field(name='Giver', value=f'{ctx.author}', inline=False)
                em.add_field(name='Receiver', value=receiver, inline=False)
                em.add_field(name='Amount Given',
                             value=f'{grant} token(s)',
                             inline=False)
                await ctx.send(embed=em)
                await receiver.send(
                    f"**{ctx.author.name}** has added **{grant} tokens** to your 60hz Competition Balance"
                )
                await tokenlog.send(
                    f"**{ctx.author.name}** has added **{grant} regular tokens** to **{receiver.name}**'s 60hz Competition Balance"
                )
            else:
                await ctx.send(
                    "That isn't a valid option. Try again and say either `gold token` or `token`"
                )
            with open('tokens.json', 'w') as f:
                json.dump(users, f)
        except asyncio.TimeoutError:
            await ctx.send("You took too much time. Try again.")
    else:
        pass


@giveTokens.error
async def give_tokens_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "You are missing some arguments. Try doing: `!give <@Member> <amount>`"
        )
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "You do not have the required permissions to use this command.")
    else:
        await ctx.send(error)


@client.command()
async def vote(ctx):
    em = discord.Embed(
        title='Vote 60hz Gang!',
        description=
        '**Top.gg**\nhttps://top.gg/servers/757383943116030074/vote\n\n**Discord Server List**\nhttps://discordbotlist.com/servers/60hz-gang/upvote\n\n**Patreon Page**\nhttps://www.patreon.com/60hzgang',
        color=discord.Color.purple())
    em.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=em)


@client.command()
async def roleinfo(ctx, page=1):
    if page == 1:
        em = discord.Embed(
            title='Table of Contents',
            description=
            'Use `!roleinfo <page>` to find information about a specific category of roles \n\n**1** - Table of Contents (current page)\n**2** - Demons \n**3** - 60hz/Non-60hz \n**4** - Pointercrate \n**5** - Competitions \n**6** - Collabs \n**7** - Moderation (admin, trial admin, etc.) \n**8** - Perks (vip, server booster, donator, etc.) \n**9** - Misc (giveaway winner, content creator, etc.) \n**10** - Leaderboard Topper Roles\n**11** - Member Roles',
            color=discord.Color.blue())

        await ctx.send(embed=em)
    elif page == 2:

        em = discord.Embed(title='Demon Roles',
                           description=f'{demonsROLE}',
                           color=discord.Color.blue())

        await ctx.send(embed=em)
    elif page == 3:

        em = discord.Embed(title='GD/Self Roles',
                           description=f'{gdrolesROLE}',
                           color=discord.Color.red())

        await ctx.send(embed=em)
    elif page == 4:
        em = discord.Embed(title='Pointercrate Roles',
                           description=f'{pointercrateROLE}',
                           color=discord.Color.orange())
        await ctx.send(embed=em)
    elif page == 5:
        em = discord.Embed(title='Competition Roles',
                           description=f'{competitionROLE}',
                           color=discord.Color.green())
        await ctx.send(embed=em)
    elif page == 6:
        em = discord.Embed(title='Collaboration Roles',
                           description=f'{collabROLE}',
                           color=discord.Color.blue())
        await ctx.send(embed=em)
    elif page == 7:
        em = discord.Embed(title='Moderation Roles',
                           description=f'{moderationsROLE}',
                           color=discord.Color.blue())
        await ctx.send(embed=em)
    elif page == 8:
        em = discord.Embed(title='Perk Roles :smirk: ',
                           description=f'{perksROLE}',
                           color=discord.Color.blue())
        await ctx.send(embed=em)
    elif page == 9:
        em = discord.Embed(title='Misc Roles',
                           description=f'{miscROLE}',
                           color=discord.Color.blue())
        await ctx.send(embed=em)
    elif page == 10:
        em = discord.Embed(title='Leaderboard Topper Roles',
                           description=f'{leaderboardToppers}',
                           color=discord.Color.red())
        await ctx.send(embed=em)
    elif page == 11:
        em = discord.Embed(title='Member Roles',
                           description=f'{memberRolesROLE}',
                           color=discord.Color.blue())
        await ctx.send(embed=em)
    else:
        await ctx.send(
            "**Invalid Number/ Command Usage.** \nRemember to do `!roleinfo <page_number>`. You can only go up to 10 pages."
        )


@roleinfo.error
async def role_info_error(ctx, error):
    em = discord.Embed(title='There was an error',
                       description=f'{error}',
                       color=discord.Color.red())
    await ctx.send(embed=em)


@client.command(aliases=['lb'])
async def leaderboard(ctx, num=10):
    print('function loaded')
    #guild = ctx.guild
    if num <= 25:

        with open('tokens.json', 'r') as f:
            users = json.load(f)
        leaderboard = {}
        total = []
        userlist = list(users)
        addedPoint = cycle([0.1, 0.15, 0.2, 0,25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        for mem in userlist:
            name = int(mem)  # getting member.id in int form
            token = users[mem]['tokens']  # number of tokens someone has
            new_token = token + next(addedPoint)
            leaderboard[
                new_token] = name  # Allows someone to get name of person with x tokens
            total.append(new_token)  # adding token values of all users
        total = sorted(total, reverse=True)  # sorting tokens greatest to least
        em = discord.Embed(title='Tokens Leaderboard',
                           color=discord.Color.blue())
        idx = 1
        for data in total:
            if num <= 10:

                id_ = leaderboard[data]
                mem = client.get_user(id_)
                LVL = users[str(mem.id)]['gold tokens']
                name = mem.name
                em.add_field(
                    name=f"{idx}. {name}",
                    value=f"`{int(data)} Tokens` | *{LVL}*  Gold Tokens  ",
                    inline=False)
                if idx == num:
                    break
                else:
                    idx += 1
            else:
                id_ = leaderboard[data]
                mem = client.get_user(id_)
                LVL = users[str(mem.id)]['gold tokens']
                name = mem.name
                em.add_field(
                    name=f"{idx}. {name}",
                    value=f"`{int(data)} Tokens` | *{LVL}*  Gold Tokens  ",
                    inline=False)
                if idx == num:
                    break
                else:
                    idx += 1
        await ctx.send(embed=em)
    else:
        await ctx.send("That's too many people to display at once!")


@client.command()
async def remove(ctx, receiver: discord.Member, *, removed: int):
    if str(ctx.guild.id) == '757383943116030074':
        #if removed > 200:
        #await ctx.send("You can't remove that many tokens at once!")
        #else:
        tokenlog = client.get_channel(805951549653778473)
        with open('tokens.json', 'r') as f:
            users = json.load(f)
        await open_account(users, receiver)

        def check(m):
            return m.channel.id == ctx.channel.id and m.author.id == ctx.author.id

        await ctx.send(
            "Which token type do you want to remove? (The receiver needs to have Dm's on to get the transaction receipt from the bot)"
        )
        try:

            tokenType = await client.wait_for("message",
                                              check=check,
                                              timeout=20)
            if tokenType.content.lower() == 'gold token':
                await change_tokens(users, receiver, removed * -1,
                                    'gold tokens')
                em = discord.Embed(
                    title=f'{verifiedEMOJI} Successful Transfer',
                    color=discord.Color.green())
                em.add_field(name='Remover',
                             value=f'{ctx.author}',
                             inline=False)
                em.add_field(name='Member', value=receiver, inline=False)
                em.add_field(name='Amount Removed',
                             value=f'{removed} gold token(s)',
                             inline=False)
                await ctx.send(embed=em)
                await receiver.send(
                    f"**{ctx.author.name}** has removed **{removed} gold tokens** from your 60hz Competition Balance"
                )
                await tokenlog.send(
                    f"**{ctx.author.name}** has removed **{removed} gold tokens** from **{receiver.name}**'s 60hz Competition Balance"
                )

            elif (tokenType.content.lower()
                  == 'token') or (tokenType.content.lower()
                                  == 'regular token'):
                await change_tokens(users, receiver, removed * -1, 'tokens')
                em = discord.Embed(
                    title=f'{verifiedEMOJI} Successful Transfer',
                    color=discord.Color.green())
                em.add_field(name='Giver', value=f'{ctx.author}', inline=False)
                em.add_field(name='Receiver', value=receiver, inline=False)
                em.add_field(name='Amount Renoved',
                             value=f'{removed} token(s)',
                             inline=False)
                await ctx.send(embed=em)
                await receiver.send(
                    f"**{ctx.author.name}** has removed **{removed} tokens** from your 60hz Competition Balance"
                )

                await tokenlog.send(
                    f"**{ctx.author.name}** has removed **{removed} regular tokens** from **{receiver.name}**'s 60hz Competition Balance"
                )
            else:
                await ctx.send(
                    "That isn't a valid option. Try again and say either `gold token` or `token`"
                )
            with open('tokens.json', 'w') as f:
                json.dump(users, f)
        except asyncio.TimeoutError:
            await ctx.send("You took too much time. Try again.")
    else:
        pass


@client.command(aliases=['competitions'])
async def competition(ctx):
    em = discord.Embed(title='Current Competition',
                       description=competition_info,
                       color=discord.Color.purple())
    await ctx.send(embed=em)


@client.command(aliases=['list', 'link', 'lists'])
async def links(ctx):
    em = discord.Embed(title='List Links',
                       description=list_desc,
                       color=discord.Color.blue())
    await ctx.send(embed=em)


async def open_account(users, user):
    if str(user.id) not in users:
        users[str(user.id)] = {}
        users[str(user.id)]['tokens'] = 0
        users[str(user.id)]['gold tokens'] = 0


async def change_tokens(users, user, amount, typeToken):

    users[str(user.id)][typeToken] += amount
    pass


@client.command()
async def staff(ctx):
    listofmods = []
    listofDevs = []
    listofAdmins = []
    listofTA = []
    listofTM = []
    listofLM = []
    for member in ctx.guild.members:
        for role in member.roles:
            if role.name.lower() == 'trial admin':
                listofTA.append(member.name)
            elif role.name.lower() == 'trial mod':
                listofTM.append(member.name)
            elif role.name.lower() == 'server mod':
                listofmods.append(member.name)
            elif role.name.lower() == 'server admin':
                listofAdmins.append(member.name)
            elif role.name.lower() == 'developer':
                listofDevs.append(member.name)
            elif role.name.lower() == 'list manager':
                listofLM.append(member.name)
            
    mod = f"**Server Mod ({len(listofmods)})**\n"
    admin = f"**Server Admin ({len(listofAdmins)})**\n"
    trialadmin = f"**Trial Admin ({len(listofTA)})**\n"
    trialmod = f"**Trial Mod ({len(listofTM)})**\n"
    devs = f"**Developers ({len(listofDevs)})**\n"
    listMods = f"**List Managers ({len(listofLM)})**\n"
    serverowner = f"[**Server Owner**](https://www.youtube.com/channel/UCxW9ilAhTGuhLvzIhgmSvyw)"
    a, b, c, d, e,f,= 1, 1, 1, 1, 1,1
    for name in listofmods:
        mod += str(a) + ". " + name + '\n'
        a += 1

    for name in listofAdmins:
        admin += str(b) + ". " + name + '\n'
        b += 1

    for name in listofTA:
        trialadmin += str(c) + ". " + name + '\n'
        c += 1
    for name in listofTM:
        trialmod += str(d) + ". " + name + '\n'
        d += 1
    for name in listofDevs:
        devs += str(e) + ". " + name + '\n'
        e += 1
    for name in listofLM:
        listMods += str(f) + ". " + name + '\n'
        f += 1

    staffdesc = (serverowner + "\n1. [MoonFrost]((https://www.youtube.com/channel/UCxW9ilAhTGuhLvzIhgmSvyw))") + '\n\n' "2. **Server Co-Owner**\nQuackerDeezlesYT\n\n" + admin + '\n' + trialadmin + '\n' + listMods+ '\n' + mod + '\n' + trialmod + '\n' + devs
    em = discord.Embed(title='Current Staff',
                       description=staffdesc,
                       color=discord.Color.purple())
    #em.set_thumbnail(url = ctx.guild.icon_url)
    await ctx.send(embed=em)


@client.command()
async def boosters(ctx):
		listofBoo = []
		for member in ctx.guild.members:
			if member.premium_since:
				listofBoo.append(member.name)
			# for role in member.roles:
			# 		if role.name.lower() == 'server booster':
			# 				listofBoo.append(member.name)
		a = 1
		serverBoosters = f"<:boost:762396759871324190> **Server Boosters ({len(listofBoo)})**\n"
		for name in listofBoo:
			serverBoosters += str(a) + ". " + name + '\n'
			a += 1
		staffdesc = "<a:rainbow_boost:824117384297054225> Thank you to our server boosters!" + "\n\n" + serverBoosters
		em = discord.Embed(title='Current Boosters',
												description=staffdesc,
												color=discord.Color.purple())
		#em.set_thumbnail(url = ctx.guild.icon_url)
		await ctx.send(embed=em)
		
@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.streaming,
            name=f"Geometry Dash",
            url='https://www.youtube.com/watch?v=c9na_ojJRuI'))
    


@client.event
async def on_message(msg):
    if (str(msg.channel.id) == '805926378960191528') or (str(
            msg.channel.id) == '783022626523971654'):
        if ("#suggestion" in msg.content) or ("#sg" in msg.content):
            # like = discord.utils.get(client.guild.emojis, name = '<:like:805931149033472020>')
            # dislike = discord.utils.get(client.guild.emojis, name = '<:dislike:805931172436901899>')
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
            pass
    await client.process_commands(msg)


@client.command(aliases=['collabSS', 'collabss', 'add'])
async def collabsuggest(ctx, *, suggestion):
    with open('collabs.json', 'r') as f:
        suggesters = json.load(f)
    suggesters.append(suggestion)
    with open('collabs.json', 'w') as f:
        json.dump(suggesters, f)
    await ctx.send(f"{verifiedEMOJI} Collab Suggestion Added!")

    pass


@client.command()
async def suggestions(ctx):
    with open('collabs.json', 'r') as f:
        suggesters = json.load(f)
    em = discord.Embed(title='Collab Suggestions', color=discord.Color.blue())
    x = 1
    for suggestion in suggesters:
        em.add_field(name=f'Suggestion {x}', value=suggestion)
        x += 1
    await ctx.send(embed=em)


@client.command(aliases=['clearsuggestion'])
@commands.has_permissions(kick_members=True)
async def removesuggestion(ctx, *, num: int):
    with open('collabs.json', 'r') as f:
        suggesters = json.load(f)
    try:
        eee = num - 1
        sug = suggesters[eee]
        suggesters.pop(eee)

        with open('collabs.json', 'w') as f:
            json.dump(suggesters, f)
        await ctx.send(
            f'Collab Suggestion **{num}** Removed \n__**Suggestion Removed**__\n{sug}'
        )
    except:
        await ctx.send(
            "I could not remove suggestion. Make sure to pick a valid integer."
        )
    pass


@removesuggestion.error
async def remove_suggestion_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "You do not have the required permissions to use this command.")
    else:
        raise error


@client.command()
async def rules(ctx, *, page: int = None):
    ruledesc = ''
    rulereason = ''
    not_desc = 'Use `!rules <number>` to find each rule\n\n**1.**  No Spamming\n**2.** Use Channels Correctly\n**3.** No Asking for Mod\n**4.** No Racism or other similar things\n**5.** Only Ping with a Valid Reason\n**6.** Be respectful to each other (this includes no bullying, hate speech, harassment, etc.)\n**7.** Respect decisions made by the staff (unless it violates one of the rules)\n**8.** Try to keep politics/controversial topics out of the chat. \n**9.** Don\'t try to start any arguments here. \n**10.** If you have completed an Extreme Demon or a List Demon, it will not officially be believed unless there is video proof (and list points if it\'s a list demon)'
    if not page:
        em = discord.Embed(title='60hz Gang Rules',
                           description=not_desc,
                           color=discord.Color.green())
        await ctx.send(embed=em)
    else:

        if page == 1:
            ruledesc = 'No Spamming'
            rulereason = 'Spamming clogs up channels and is quite annoying.'
        elif page == 2:
            ruledesc = 'Use Channels Correctly'
            rulereason = 'Different channels are meant for different reasons, so all content should go in their appropriate location.'
        elif page == 3:
            ruledesc = 'No Asking for Mod'
            rulereason = 'This is kind of obvious. Everyone wants mod, but everyone can\'t get it. Being a moderator means having a big responsibility of the server. If you want to actually become a mod, you can DM MoonFrost and ask for the staff applications. We may not allow any submissions if mods are not necessary.'
        elif page == 4:
            ruledesc = 'No Racism or other similar things'
            rulereason = 'Racism can be offensive to some people (obviously), so it is strictly prohibited'
        elif page == 5:
            ruledesc = 'Only Ping with a Valid Reason'
            rulereason = 'Excessively pinging people for no reason at all can be annoying for the people getting pinged.'
        elif page == 6:
            ruledesc = 'Be respectful to each other (this includes no bullying, hate speech, harassment, etc.)'
            rulereason = 'Like Rule 4, bullying and hate speech can depress people and can make people feel offended.'
        elif page == 7:
            ruledesc = 'Respect decisions made by the staff (unless it violates one of the rules)'
            rulereason = 'Staff have higher authority over normal members because usually they would know the correct thing to do in certain situations, even if it impacts you.'
        elif page == 8:
            ruledesc = 'Try to keep politics/controversial topics out of the chat.'
            rulereason = 'Politics and controversial topics can spark arguments pretty quickly and we want to limit the amount of fights that happen in the server.'
        elif page == 9:
            ruledesc = 'Don\'t try to start any arguments here.'
            rulereason = 'Arguments can create tension in the server, so we try our best to prohibit that from happening. If it gets too out of hand, the staff will take action.'
        elif page == 10:
            ruledesc = 'If you have completed an Extreme Demon or a List Demon, it will not officially be believed unless there is video proof (and list points if it\'s a list demon)'
            rulereason = 'Extreme Demons and Lists Demons are quite hard to complete which is why they will need some proof that you actually did it. Remember to never cheat!'

        em = discord.Embed(
            title=f'Rule {page} | {ruledesc}',
            description=f'\n\n__**Why is this a rule?**__\n\n{rulereason}',
            color=discord.Color.green())
        await ctx.send(embed=em)


@client.command()
async def server(ctx):
    em = discord.Embed(title='Official Bot Server',
                       description='https://discord.gg/JMnEK3gZcZ',
                       color=discord.Color.orange())
                      
    await ctx.send(embed=em)

async def get_names(members):
  new_str = ""
  for b in range(len(members)):
    get_member = members[b]
    if( b == len(members) - 1):
      new_str += get_member.name
    else:

      new_str += get_member.name + ", "
  return new_str

@client.event
async def on_message_delete(msg):
  if msg.mentions:
    if msg.mentions[0].bot:
      pass
    else:
			# hello
      membername = msg.mentions[0].name
      listed = await get_names(msg.mentions)
      new_desc = f"**Author** \n{msg.author}\n\n**Member(s) Pinged**\n{listed}\n\n**Message**\n{msg.clean_content}"
      em = discord.Embed(title = 'Ghost Ping', description = new_desc, color = discord.Color.blue())
      await msg.channel.send(embed = em)
  else:
    pass



client.run(os.getenv("TOKEN"))