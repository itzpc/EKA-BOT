from discord.ext import commands
import discord
import asyncio
import traceback
import inspect
import textwrap
from contextlib import redirect_stdout
import io
import os
from typing import Union
from datetime import datetime, date
import time
from discord.ext import tasks
from application.constants.guild1947 import *
from application.constants.guildsupport import *
from application.constants.emoji import *
from application.cogs.utils.paginator import TextPages
from application.constants.config import DiscordConfig
from application.utlis.birthday import Birthday

class User(commands.Cog):
    """ EKA members will have all these fun """
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
    
    @commands.command(aliases=['Av','av','avatar','Avatar'])
    async def user_avatar(self, ctx, user:discord.User):
        """--> `eka av @mentionUser `"""
        if user.bot:
            return
        embed = discord.Embed(title = f"Avatar Requested of EKA Warrior : {user.name}",
            color = 0x98FB98
            )
        embed.set_image(url = user.avatar_url) 
        
        await self.bot.get_channel(id=Guild1947.EKA_BOT_CHANNEL_ID).send(embed=embed)
        await ctx.message.add_reaction(Emoji.GREEN_TICK)

    @commands.command(aliases=['Dm','dm','DM'])
    async def dm_user(self, ctx, user:discord.User,msg:str):
        """--> `eka dm @mentionUser message`"""
        if user.bot:
            return
        embed = discord.Embed(title = f"You have a message from : {ctx.message.author}",
            description = msg,
            color = 0x98FB98
            )
        embed.set_thumbnail(url=str(ctx.message.author.avatar_url))
        
        try:
            await user.send(embed=embed)
            Msg=await self.bot.get_channel(id=Guild1947.EKA_BOT_CHANNEL_ID).send(f"Hey {ctx.message.author}, Your message has been sent ```eka dm @mentionUser YourMessage``` to DM someone")
            await Msg.add_reaction(Emoji.GREEN_TICK)
        except:
            Msg=await self.bot.get_channel(id=Guild1947.EKA_BOT_CHANNEL_ID).send(f"Sorry {ctx.message.author}, The user has disabled DM. Your message could not be sent.```eka dm @mentionUser YourMessage``` to DM someone")
            await Msg.add_reaction(Emoji.X)
        await ctx.message.delete()

    @commands.command(aliases=['add_birthday','Add_birthday','Add_bday'])
    async def add_bday(self, ctx, message:str):
        """--> `eka add_bday dd-mm-yyyy `"""
        try:

            if message is None:
                await self.bot.get_channel(id=Guild1947.EKA_BOT_CHANNEL_ID).send("Oh ! You forget to give me a date in DD-MM-YYYY format")
                return
            
            msg = message.strip()
            dob = datetime.strptime(msg, "%d-%m-%Y")
            today = date.today()
            result = self.bot.db_utlis.update_member_table(ctx.message.author.id, ctx.message.author.joined_at, dob)
            if result is True:
                await ctx.message.add_reaction(Emoji.GREEN_TICK)
                if (dob.month == today.month) and (dob.day == today.day):
                    await Birthday(self.bot,self.bot.db_utlis,ctx.message.author).wish_birthday()
            elif result:
                await ctx.message.add_reaction(Emoji.WARNING)
                await self.bot.get_channel(id=Guild1947.EKA_BOT_CHANNEL_ID).send(f"Oh ! We have already recorded your DOB as {str(result)}, Try `eka update_bday DD-MM-YYYY` , If you want to update it.")
            else:
                await ctx.message.add_reaction(Emoji.X)

        except Exception as ex:
            await self.bot.get_channel(id=Guild1947.EKA_BOT_CHANNEL_ID).send(f"Oh ! Provide date in DD-MM-YYYY format only {ex}")

    @commands.command(aliases=['update_birthday','Update_birthday','Update_bday'])
    async def update_bday(self, ctx, message:str):
        """--> `eka update_bday dd-mm-yyyy `"""
        try:
            if message is None:
                await self.bot.get_channel(id=Guild1947.EKA_BOT_CHANNEL_ID).send("Oh ! You forget to give me a date in DD-MM-YYYY format")
                return
            msg = message.strip()
            dob = datetime.strptime(msg, "%d-%m-%Y")
            today= date.today()
            if self.bot.db_utlis.update_member_table(ctx.message.author.id, ctx.message.author.joined_at, dob,True):
                await ctx.message.add_reaction(Emoji.GREEN_TICK)
                if (dob.month == today.month) and (dob.day == today.day):
                    await Birthday(self.bot,self.bot.db_utlis,ctx.message.author).wish_birthday()

            else:
                await ctx.message.add_reaction(Emoji.X)

        except Exception as ex:
            await self.bot.get_channel(id=Guild1947.EKA_BOT_CHANNEL_ID).send(f"Oh ! Provide date in DD-MM-YYYY format only . `ERRORCODE : {ex}`")
        
    @commands.command(aliases=['list_birthday','List_birthday','List_bday'])
    async def list_bday(self, ctx):
        """--> `eka list_bday  `"""
        try:
            result=self.bot.db_utlis.fetch_bday()
            text = str()
            for row in result:
                userObj=self.bot.get_user(row.member_id)
                text += f"{userObj.name} - {row.dob} \n "
            p = TextPages(ctx, text=text ,max_size=500)
            await p.paginate()
        except Exception as Ex:
            logging.error("ERROR : user.py : list_bday : {}".format(Ex))
        

def setup(bot):
    bot.add_cog(User(bot))

