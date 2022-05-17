import discord
from discord.ext import commands
import random

class Games(commands.Cog):
    
    def __init__(self, client):
        self.client = client # allows us to access client w/in our cog
    
    # Must always have this decorator here if want to create events within a cog
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')
    
    # Commands
    @commands.command()
    async def ping(self, ctx):
        '''Spoiler: Pong! & Shows client latency'''
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')
    
    
    @commands.command(aliases = ['8ball'])
    async def _8ball(self, ctx, *, question):
        '''Ask a question get a response'''
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    
def setup(client):
    client.add_cog(Games(client))
