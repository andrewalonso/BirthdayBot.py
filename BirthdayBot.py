import discord, asyncio
import os
import random
import emoji
import json, datetime
from discord.ext import commands, tasks
from itertools import cycle

# A Birthday Bot to track all your friends birthdays so everyone can tell them Happy Birthday!
# Read README to understand how to use

client = commands.Bot(command_prefix = '.')

status = cycle(['Hello I am Birthday Bot!', 'MATHEMATICAL!', '*GameCube start up noise*', 'The sky\'s awake so I\'m awake'])

# First thing bot does when ran
@client.event
async def on_ready():
    change_status.start()
    happyBirthday.start()
    print('Bot is ready.')

# Background tasks updated every so often
@tasks.loop(seconds = 3600) # 1 hour
async def change_status():
    await client.change_presence(activity = discord.Game(next(status)))

# General Error Handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')


@client.command()
async def hi(ctx, member: discord.Member):
    '''Says hello to user mentioned'''
    await ctx.send(f'Why hello {member.mention}!')


# .add - adds birthday to list
@client.command()
#@commands.has_permissions(manage_messages = True) # Only people with manage messages can use
async def add(ctx, member: discord.Member, birthDate):
    '''
    Adds member and birthdate to bday list.
    Use: .add @MEMBER BIRTHDATE
    '''
    with open('bdays.json', 'r') as f:
        data = json.load(f)
    data[str(birthDate)] = member.name # Ex: "1-27": "DREWPER5ON"
    
    with open('bdays.json', 'w') as f:
        json.dump(data, f, indent = 4, sort_keys = True)
    

@client.command()
#@commands.has_permissions(manage_messages = True) # Only people with manage messages can use
async def delete(ctx, member: discord.Member, birthDate):
    '''
    Removes member and birthdate from bday list. 
    Use: .delete @MEMBER BIRTHDATE
    '''
    with open('bdays.json', 'r') as f:
        data = json.load(f)
    data[str(birthDate)] = member.name
    
    del (data[birthDate])
    
    with open('bdays.json', 'w') as f:
        json.dump(data, f, indent = 4, sort_keys = True)


@client.command(aliases = ['bdayList', 'birthdaylist','birthdays','list'])
async def birthdayList(ctx):
    '''List of all birthdays starting from Jan. to Dec.'''
    with open('bdays.json', 'r') as f:
        data = json.load(f)
    
    await ctx.send(json.dumps(data, indent = 4, sort_keys = True))


@client.command(aliases = ['birthdaysThisMonth','bdayThisMonth','bdaythismonth'])
async def birthdayThisMonth(ctx):
    '''All the birthdays this month.'''
    today = datetime.date.today() # Ex: datetime.date(2021, 1, 4)
    strMonth = (str(today.month)) # Ex: "1" for month of Dec.
    with open('bdays.json', 'r') as f:
        data = json.load(f)
    
    y = list(data.keys()) # Ex: ['1-27','date2','date3', ...]
    z = list(data.items()) # Ex: [('1-27', 'DREWPER5ON'), ('date2','user2'), ...]

    # t is set to the current month's date
    t = today.month
    for item in z:
        if str(t) in item[0][0]:
            await ctx.send(item)


@client.command(aliases = ['birthdaysNextMonth','bdayNextMonth','bdaynextmonth'])
async def birthdayNextMonth(ctx):
    '''Next month's birthdays.'''
    today = datetime.date.today() # Ex: datetime.date(2021, 1, 4)
    nextMonth = today.month + 1
    if nextMonth == 13:
        nextMonth = 1
    
    strNextMonth = (str(nextMonth)) # Ex: Dec. the 12th month would give '1'
    with open('bdays.json', 'r') as f:
        data = json.load(f)
    
    y = list(data.keys()) # Ex: ['1-27','date2','date3', ...]
    z = list(data.items()) # Ex: [('1-27', 'DREWPER5ON'), ('date2','user2'), ...]

    for item in z:
        if strNextMonth in item[0][0]:
            await ctx.send(item)


@tasks.loop()
async def happyBirthday():
    '''Sends a happy bday message and @'s all users.'''
    
    # ***IMPORTANT*** ADD CHANNEL(general) ID --------------------------------v
    # This is where the bot will wish Happy Birthday
    channel = client.get_channel('INSERT GENERAL CHAT ID HERE AND REMOVE QUOTES')
    
    while True:
        today = datetime.date.today() # Ex: datetime.date(2021, 1, 4)
        todaysDate = str(today.month) + '-' + str(today.day) # Example: '12-30'
        
        with open('bdays.json', 'r') as f:
            data = json.load(f)
        
        y = (list(data.keys())) # Ex: ['12-30']
        z = list(data.items()) # Ex: [('1-27', 'DREWPER5ON')]
        
        n = -1
        for birthDate in data:
            n = n + 1
            # If '12-30' == '12-30'
            if todaysDate == y[n]:
                startMessage = ["***Happy Birthday!!!***",
                                "***WOW INCREDIBLE*** IT'S YOUR BIRTHDAY",
                                "Happiest of the birthday's to you",
                                "Hey you, yeah you...Happy Birthday!"]
                
                endMessage = ["HAPPYYY BIRTHDAY TO YOUUUUUUU",
                              "Congratulations!!!",
                              "Hope you have an awesome day!"]
                
                quote = ['As you get older, three things happen: The first is your memory goes, and I can’t remember the other two. — Norman Wisdom',
                         'Today is the oldest you have been, and the youngest you will ever be. Make the most of it! – Nicky Gumbel',
                         'You know you’re getting old when the candles cost more than the cake. — Bob Hope',
                         'And in the end, it’s not the years in your life that count. It’s the life in your years. — Abraham Lincoln',
                         'Every birthday is a gift. Every day is a gift. — Aretha Franklin',
                         'Let them eat cake. — Marie Antoinette',
                         'You were born and with you endless possibilities, very few ever to be realized. It’s okay. Life was never about what you could do, but what you would do. — Richelle E. Goodrich',
                         'Live long and prosper. — Mr. Spock',
                         'Birthdays come but once a year, celebrate and be of good cheer. — Robert Rivers',
                         'I intend to live forever. So far, so good. — Steven Wright',
                         'May you live as long as you want and never want as long as you live. – Irish blessing',
                         'They say it’s your birthday. We’re gonna have a good time. I’m glad it’s your birthday. Happy birthday to you. – The Beatles',
                         'When a man has a birthday, he takes a day off. When a woman has a birthday, she takes at least three years off. – Joan Rivers',
                         'From our birthday, until we die, / Is but the winking of an eye. - William Butler Yeats',
                         'Have good, be fun. - Scott Slectha',
                         'Happy happy birthday! Happy birthday cake! Happy happy birthday! Pin the tail on the seahorse! Happy happy birthday! Happy birthday Squidward! \nSquidward: Its not my BIRTHDAY!']
                
                gif = ['https://tenor.com/view/happy-birthday-gifts-spongebob-patrick-star-squidward-gif-17295437',
                       'https://tenor.com/view/happy-birthday-fireworks-display-gif-22634411',
                       'https://tenor.com/view/happy-birthday-to-you-gif-24385804',
                       'https://tenor.com/view/happy-birthday-sing-happy-birthday-song-happy-birthday-to-you-happy-birthday-gif-gif-24530427',
                       'https://tenor.com/view/love-sis-gif-23719885',
                       'https://tenor.com/view/happy-birthday-gif-23099693',
                       'https://tenor.com/view/holiday-classics-elf-christmas-excited-happy-gif-15741376',
                       'https://tenor.com/view/happy-birthday-gif-25066162',
                       'https://tenor.com/view/happy-birthday-bon-anniversaire-birthday-cake-birthday-birthday-fiesta-gif-24411575',
                       'https://tenor.com/view/happy-birthday-wish-cake-happy-birthday-to-you-my-friend-celebrate-gif-15264814']
                
                await channel.send(f'@everyone {random.choice(startMessage)} {z[n][1]}!!! {random.choice(endMessage)}\n\nYour B-day quote: {random.choice(quote)}\n{random.choice(gif)}')
        
        await asyncio.sleep(86400)

    
# Load command - loads extension
@client.command()
#@commands.check(is_it_me)
async def load(ctx, extension):
    '''Loads extensions.'''
    client.load_extension(f'cogs.{extension}')
    
@client.command()
#@commands.check(is_it_me)
async def unload(ctx, extension):
    '''^'''
    client.unload_extension(f'cogs.{extension}')

# When bot turns on check if py file load it like a cog
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        # splices last three letters of .py file to load
        client.load_extension(f'cogs.{filename[:-3]}')


# Checks if its me 
# Important IF only you want to access the load/unload command
# To access uncomment code below and above *@commands.check(is_it_me)* & add ID
#def is_it_me(ctx):
#    return ctx.author.id == INSERT ID HERE


# Bot Token **IMPORTANT!** -------------------v
# To access, must create your own Bot in Discord Developer Portal
# and copy the token down below
client.run('INSERT BOT TOKEN HERE AND DONT REMOVE QUOTES')
