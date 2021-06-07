import discord
from discord.ext import commands
import os
import json
import datetime
import asyncio


from mooncanedit import gdshopToken, gdshopGoldToken, list_desc, competition_info
from roleStuff import demonsROLE, gdrolesROLE, pointercrateROLE, competitionROLE, collabROLE, moderationsROLE, perksROLE, miscROLE, memberRolesROLE, leaderboardToppers, pingsROLE
# import keep_alive
from discord_slash import SlashCommand, SlashContext
from itertools import cycle
# from flask import Flask
from discord_slash.utils import manage_commands
from pymongo import MongoClient
intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = commands.Bot(command_prefix="!", intents=intents)
GOLD_TOKEN_EMOJI = '<:goldtoken:805527920512204821>'
slash = SlashCommand(client,sync_commands=True)
verifiedEMOJI = "<a:verified:805929172451065879>"
redloading = '<a:red_loading:805930785919467521>'


guild_ids = [782651282128896020,757383943116030074] # Put your server ID in this array.

url = os.getenv("MONGO")
url2 = ""
cluster = MongoClient(url)
db = cluster['discord']
tokens = db['tokens']
warns = db['warns']


@slash.slash(name="ping", description="Returns the latency of the bot", guild_ids=guild_ids)
async def _ping(ctx): # Defines a new "context" (ctx) command called "ping."
    #await ctx.respond()
    await ctx.send(f"Pong! ({int(client.latency*1000)}ms)")

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
	name = "rule",
	description ="View the rules of the server",
 	options = [
   manage_commands.create_option(
    name = "rule",
    description = "The specific rule option you want to pick",
    option_type = 3,
    required = True,
		choices = [
			manage_commands.create_choice("1", "No Spamming"),
			manage_commands.create_choice("2", "Use Channels Correctly"),
			manage_commands.create_choice("3","No Asking for Mod"),
			manage_commands.create_choice("4","No Racism or other similar things"),
			manage_commands.create_choice("5","Only Ping with a Valid Reason"),
			manage_commands.create_choice("6","Be respectful to each other."),
			manage_commands.create_choice("7","No NSFW is tolerated whatsoever."),
			manage_commands.create_choice("8","Respect decisions made by the staff."),
			manage_commands.create_choice("9","Try to keep politics/controversial topics out of the chat."),
			manage_commands.create_choice("10","Don\'t try to start any arguments here."),
			manage_commands.create_choice("11","Extreme Demons and List Demons need video evidence")
		]
  )
 ],
 guild_ids = guild_ids)
async def _rules(ctx, rule):
		ruledesc = ''
		rulereason = ''

		if rule == "1":
				ruledesc = 'No Spamming'
				rulereason = 'Spamming clogs up channels and is quite annoying.'
		elif rule == "2":
				ruledesc = 'Use Channels Correctly'
				rulereason = 'Different channels are meant for different reasons, so all content should go in their appropriate location.'
		elif rule == "3":
				ruledesc = 'No Asking for Mod'
				rulereason = 'This is kind of obvious. Everyone wants mod, but everyone can\'t get it. Being a moderator means having a big responsibility of the server. If you want to actually become a mod, you can DM MoonFrost and ask for the staff applications. We may not allow any submissions if mods are not necessary.'
		elif rule == "4":
				ruledesc = 'No Racism or other similar things'
				rulereason = 'Racism can be offensive to some people (obviously), so it is strictly prohibited'
		elif rule == "5":
				ruledesc = 'Only Ping with a Valid Reason'
				rulereason = 'Excessively pinging people for no reason at all can be annoying for the people getting pinged.'
		elif rule == "6":
				ruledesc = 'Be respectful to each other'
				rulereason = 'This includes no bullying, hate speech, harassment, etc.) Like Rule 4, bullying and hate speech can depress people and can make people feel offended.'
		elif rule == "7":
				ruledesc = 'No NSFW is tolerated whatsoever.'
				rulereason = 'We want to keep 60hz Gang as SFW as possible to make the members feel comfortable whenever they enter the server.'
		elif rule == "8":
				ruledesc = 'Respect decisions made by the staff '
				rulereason = 'Staff have higher authority over normal members because usually they would know the correct thing to do in certain situations, even if it impacts you. This rule applies all the time unless it violates a rule.'
		elif rule == "9":
				ruledesc = 'Try to keep politics/controversial topics out of the chat.'
				rulereason = 'Politics and controversial topics can spark arguments pretty quickly and we want to limit the amount of fights that happen in the server.'
		elif rule == "10":
				ruledesc = 'Don\'t try to start any arguments here.'
				rulereason = 'Arguments can create tension in the server, so we try our best to prohibit that from happening. If it gets too out of hand, the staff will take action.'
		elif rule == "11":
				ruledesc = 'If you have completed an Extreme Demon or a List Demon, it will not officially be believed unless there is video proof (and list points if it\'s a list demon)'
				rulereason = 'Extreme Demons and Lists Demons are quite hard to complete which is why they will need some proof that you actually did it. Remember to never cheat!'
			
		em = discord.Embed(
				title=f'Rule {rule} | {ruledesc}',
				description=f'\n\n__**Why is this a rule?**__\n\n{rulereason}',
				color=discord.Color.green())
		#await ctx.respond()
		await ctx.send(embed=em)

@slash.slash(
	name = "role",
	description ="View the roles of the server",
 	options = [
   	manage_commands.create_option(
    	name = "role",
    	description = "The specific role category you want to pick",
    	option_type = 3,
    	required = True,
			choices = [
				manage_commands.create_choice("1","GD/Self Roles"),
				manage_commands.create_choice("2","Staff Roles"),
				manage_commands.create_choice("3","Perk Roles"),
				manage_commands.create_choice("4","Ping Roles")
				
			]
  )
 	],
 	guild_ids = guild_ids)
async def _role(ctx, role):
		page = role
		page = int(role)
		if page == 1:
				em = discord.Embed(
						title='Table of Contents',
						description=
						'Use `!roleinfo <page>` to find information about a specific category of roles \n\n**1** - Table of Contents (current page)\n**2** - GD/Self Roles \n**3** - Moderation (admin, trial admin, etc.) \n**4** - Perks (vip, server booster, donator, etc.) \n*58** - Ping roles',
						color=discord.Color.blue())
				await ctx.send(embed=em)
		elif page == 2:
				em = discord.Embed(title='GD/Self Roles', description=f'Get these roles in <#797897371866234910> by reacting!\n{gdrolesROLE}', color=discord.Color.red())
				await ctx.send(embed=em)
		elif page == 3:
				em = discord.Embed(title='Moderation Roles',
													description=f'{moderationsROLE}',
													color=discord.Color.blue())
				await ctx.send(embed=em)
		elif page == 4:
				em = discord.Embed(title='Perk Roles :smirk: ',
													description=f'{perksROLE}',
													color=discord.Color.blue())
				await ctx.send(embed=em)
		elif page == 5:
				em = discord.Embed(title = "Ping Roles",
													description = f"{pingsROLE}",
													color = discord.Color.blue())
				await ctx.send(embed = em)


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
						'Use `!roleinfo <page>` to find information about a specific category of roles \n\n**1** - Table of Contents (current page)\n**2** - GD/Self Roles \n**3** - Moderation (admin, trial admin, etc.) \n**4** - Perks (vip, server booster, donator, etc.) \n**5** - Ping roles',
						color=discord.Color.blue())
				await ctx.send(embed=em)
		elif page == 2:
				em = discord.Embed(title='GD/Self Roles',
													description=f'Get these roles in <#797897371866234910> by reacting!\n{gdrolesROLE}',
													color=discord.Color.red())
				await ctx.send(embed=em)
		elif page == 3:
				em = discord.Embed(title='Moderation Roles',
													description=f'{moderationsROLE}',
													color=discord.Color.blue())
				await ctx.send(embed=em)
		elif page == 4:
				em = discord.Embed(title='Perk Roles :smirk: ',
													description=f'{perksROLE}',
													color=discord.Color.blue())
				await ctx.send(embed=em)
		elif page == 5:
				em = discord.Embed(title = "Ping Roles",
													description = f"{pingsROLE}",
													color = discord.Color.blue())
				await ctx.send(embed = em)
		else:
				await ctx.send(
						"**Invalid Number/ Command Usage.** \nRemember to do `!roleinfo <page_number>`. You can only go up to 5 pages."
				)


@roleinfo.error
async def role_info_error(ctx, error):
    em = discord.Embed(title='There was an error',
                       description=f'{error}',
                       color=discord.Color.red())
    await ctx.send(embed=em)


@client.command()
async def staff(ctx):
    listofmods = []
    listofDevs = []
    listofAdmins = []
    listofTA = []
    listofTM = []
    for member in ctx.guild.members:
        for role in member.roles:
            if role.name.lower() == 'trainee duck watchman':
                listofTA.append(member.name)
            elif role.name.lower() == 'trianee headman ducks':
                listofTM.append(member.name)
            elif role.name.lower() == 'headman ducks':
                listofmods.append(member.name)
            elif role.name.lower() == 'supreme duck watchman':
                listofAdmins.append(member.name)
            elif role.name.lower() == 'dev ducks':
                listofDevs.append(member.name)
            
    mod = f"**Server Mod ({len(listofmods)})**\n"
    admin = f"**Server Admin ({len(listofAdmins)})**\n"
    trialadmin = f"**Trial Admin ({len(listofTA)})**\n"
    trialmod = f"**Trial Mod ({len(listofTM)})**\n"
    devs = f"**Developers ({len(listofDevs)})**\n"
    serverowner = f"[**Server Owner**](https://www.youtube.com/channel/UC6PKOburRMFSjwTCQcL4wbQ)"
    a, b, c, d, e,= 1, 1, 1, 1, 1
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

    staffdesc = (serverowner + "\n[nowaR]((https://www.youtube.com/channel/UCpnLOdwciYkZfdGzDvbrE7w))") + '\n\n' + admin + '\n' + trialadmin + '\n' + mod + '\n' + trialmod + '\n' + devs
    em = discord.Embed(title='Current Staff',
                       description=staffdesc,
                       color=discord.Color.purple())
    #em.set_thumbnail(url = ctx.guild.icon_url)
    em.set_footer(text="Quacker is not listed as he is founder, not the real owner.")
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
		serverBoosters = f"<:sparkleboost:825156918519398410> **Server Boosters ({len(listofBoo)})**\n"
		for name in listofBoo:
			serverBoosters += str(a) + ". " + name + '\n'
			a += 1
		staffdesc = "<a:rainbow_boost:824117384297054225>  Thank you to our server boosters!" + "\n\n" + serverBoosters
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
            url='https://www.youtube.com/watch?v=FxC7vJ5gsBw'))

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
async def add_warns(member,reason):
  data = warns.find_one({"_id" : member.id})
  if not data:
    warnData = [
      {"reason" : reason,
      "time" : datetime.datetime.now().strftime("%B %d, %Y  %I: %M %p UTC") }
    ]
    warns.insert_one({"_id" : member.id, "warns" : warnData})
  else:
    warnDataList = data["warns"]
    warnDataList.append({"reason" : reason, "time" : datetime.datetime.now().strftime("%B %d, %Y  %I: %M %p UTC")})
    warns.update_one({"_id" : member.id}, {"$set" : {"warns": warnDataList}})
  # json_files[str(member.guild.id)][str(member.id)]["warns"].append({"reason" : reason, "time" : datetime.datetime.now().strftime("%B %d, %Y  %I: %M %p UTC")})


async def setup_warns(member,json_files):
  if not str(member.guild.id) in json_files:
    print("True 1")
    json_files[str(member.guild.id)] = {}
  if not str(member.id) in json_files[str(member.guild.id)]:

    json_files[str(member.guild.id)][str(member.id)] = {}
  if not "warns" in json_files[str(member.guild.id)][str(member.id)]:

    json_files[str(member.guild.id)][str(member.id)]["warns"] = []

@client.command()
@commands.has_permissions(manage_messages = True)
async def warn(ctx,member : discord.Member = None, *, reason = None):
  if not reason:
    reason = "None"
  if not member:
    return await ctx.send("Invalid Command Usage. Remember to do ```%warn <member> (optional reason```")
  
  em = discord.Embed(title = "Member Warn", color = discord.Color.blue())
  em.add_field(name = "__Member Warned__", value = f"\n**Name:** {member}\n**ID:** {member.id}", inline = True)
  em.add_field(name = "__Moderator__", value = f"\n**Name:** {ctx.author}\n**ID:** {ctx.author.id}", inline = True)
  em.add_field(name = "__Reason__", value = f"{reason}", inline = False)
  

  await add_warns(member,reason)
  em.timestamp = ctx.message.created_at
  memData = warns.find_one({"_id" : member.id})
  numWarns = len(memData["warns"])
  await ctx.send(embed = em)
  await member.send(f"You were warned in **{ctx.guild.name}**. You now have {numWarns} warns.")
  
@client.command()
@commands.has_permissions(manage_messages = True)
async def clearwarns(ctx,member : discord.Member = None):
  if not member:
    return await ctx.send("Invalid Command Usage. Remember to do ```%clearwarns <@member>```")
  
  memberType = warns.find_one({"_id" : member.id})
  if not memberType:
    return await ctx.send("This user doesn't have any warns")
  warnAmount = memberType["warns"]
  warnAmount.clear()
  warns.update_one({"_id" : member.id}, {"$set" : {"warns" : warnAmount}})
  await ctx.send(f"All the warns for **{member}** were cleared! ")
  await member.send(f"All of your warns were cleared in **{ctx.guild.name}**")

@client.command()
@commands.has_permissions(manage_messages = True)
async def deletewarn(ctx,member : discord.Member = None, warn_number : int = None):
  if not member or not warn_number:
    return await ctx.send("Invalid Command Usage. Remember to do ```%delete_warn <@member> <number>```")
  findData = warns.find_one({"_id" : member.id})
  if not findData:
    return await ctx.send("This member doesn't have any warns!")
  warnAmount = findData["warns"]
  warnAmount.pop(warn_number - 1)
  
  warns.update_one({"_id" : member.id}, {"$set" : {"warns" : warnAmount}})
  await ctx.send(f"Warn {warn_number} was cleared for **{member}**")
  memData = warns.find_one({"_id" : member.id})
  numWarns = len(memData["warns"])
  await member.send(f"Warn {warn_number} was cleared in **{ctx.guild.name}**. You now have **{numWarns} warns**.")


async def get_warn_info(member):
  memberData = warns.find_one({"_id" : member.id})
  if not memberData:
    return None
  
  list_of_warns = memberData["warns"]
  warn_list = ""
  reason_list = ""
  dates = ""
  x = 1
  for warn in list_of_warns:
    reason_list += warn["reason"] + "\n"
    warn_list += f"Warn {x} \n"
    dates += warn["time"] + "\n"
    x += 1
    print("worked")

  print("done")
  return [warn_list,reason_list, dates]



@client.command(aliases = ['warns'])
async def infractions(ctx, member : discord.Member = None):
  if not member:
    member = ctx.author
  
  
  info_list = await get_warn_info(member)
  if (not info_list) or (info_list[1] == ""):
    reasons = "No warns!"
    dates = "None"
  else:
    reasons = info_list[1]
    dates = info_list[2]

    
  em = discord.Embed(title = f"Infractions for {member.name}", color = discord.Color.blue())
  #em.add_field(name ="Warns",value=f"{warns}",inline =True)
  em.add_field(name = "Reasons", value = reasons, inline = True)
  em.add_field(name = "Time", value = dates, inline = True)
  em.set_author(name = member, icon_url = member.avatar_url)
  em.timestamp = ctx.message.created_at
  em.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
  await ctx.send(embed = em)


@client.command(aliases = ['rule'])
async def rules(ctx, *, page: int = None):
		ruledesc = ''
		rulereason = ''
		not_desc = 'Use `!rules <number>` to find each rule\n\n**1.**  No Spamming\n**2.** Use Channels Correctly\n**3.** No Asking for Mod\n**4.** No Racism or other similar things\n**5.** Only Ping with a Valid Reason\n**6.** Be respectful to each other (this includes no bullying, hate speech, harassment, etc.)\n**7.** No NSFW is tolerated whatsoever.\n**8.** Respect decisions made by the staff (unless it violates one of the rules)\n**9.** Try to keep politics/controversial topics out of the chat. \n**10.** Don\'t try to start any arguments here. \n**11.** If you have completed an Extreme Demon or a List Demon, it will not officially be believed unless there is video proof (and list points if it\'s a list demon)'
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
						ruledesc = 'No NSFW is tolerated whatsoever.'
						rulereason = 'We want to keep 60hz Gang as SFW as possible to make the members feel comfortable whenever they enter the server.'
				elif page == 8:
						ruledesc = 'Respect decisions made by the staff (unless it violates one of the rules)'
						rulereason = 'Staff have higher authority over normal members because usually they would know the correct thing to do in certain situations, even if it impacts you.'
				elif page == 9:
						ruledesc = 'Try to keep politics/controversial topics out of the chat.'
						rulereason = 'Politics and controversial topics can spark arguments pretty quickly and we want to limit the amount of fights that happen in the server.'
				elif page == 10:
						ruledesc = 'Don\'t try to start any arguments here.'
						rulereason = 'Arguments can create tension in the server, so we try our best to prohibit that from happening. If it gets too out of hand, the staff will take action.'
				elif page == 11:
						ruledesc = 'If you have completed an Extreme Demon or a List Demon, it will not officially be believed unless there is video proof (and list points if it\'s a list demon)'
						rulereason = 'Extreme Demons and Lists Demons are quite hard to complete which is why they will need some proof that you actually did it. Remember to never cheat!'
				elif page == 12:
						ruledesc = 'No DM advertising'
						rulereason = 'DM Advertising is annoying. If you want to advertise, there\'s an advertising channel where you can post your content if you are above level 5.'
				elif page >= 13:
					return await ctx.send("There are only 11 rules!")
				
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