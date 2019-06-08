from discord.ext import commands
import discord
import asyncio
from copy import deepcopy
import asyncio
import traceback
import inspect
import textwrap
from contextlib import redirect_stdout
import io
import os
import copy
from typing import Union
# to expose to the eval command
import datetime
from collections import Counter

class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()

    @commands.command()
    @commands.is_owner()
    async def sudo(self, ctx, user: Union[discord.Member, discord.User], *, command: str):
        """Run a command as another user."""
        msg = copy.copy(ctx.message)
        msg.author = user
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg)
        await self.bot.invoke(new_ctx)
    @commands.Cog.listener()
    async def on_member_join(self,member):
        if member.guild.id == 561249245672374273:
            welcomechannel = self.bot.get_channel(569973273253904385)
            apply_eka = self.bot.get_channel(566609366770515989)
            about =self.bot.get_channel(567962887054950420)
            directory=os.getcwd()
            file = discord.File(os.path.join(directory+str('/')+"images/recruitment.jpg"),filename="recruitment.jpg")
            embed = discord.Embed(title="**__WELCOME TO EKA__**", colour=discord.Colour(0x673c27), url="https://link.clashofclans.com/?action=OpenClanProfile&tag=RJ9JYYQQ", description=f"Hello {member.mention}|{member.name}  \n\n:point_right:Elite Kerala Alliance. \n:point_right: MLCW - GWL & EWL -ELITE clan.\n:point_right: WCL, EWL, NDL WELTER\n\n  ", timestamp=datetime.datetime.utcfromtimestamp(1559028785))
            embed.set_thumbnail(url=str(member.avatar_url))
            embed.set_author(name="Elite Kerala Alliance ", url="https://link.clashofclans.com/?action=OpenClanProfile&tag=RJ9JYYQQ", icon_url="https://cdn.discordapp.com/attachments/562537063052738569/582847093434089472/eka.jpg")
            embed.set_footer(text="Team EKA |", icon_url="https://cdn.discordapp.com/attachments/562537063052738569/582847093434089472/eka.jpg")
            embed.add_field(name=f"Want to join With Us ?", value=f"React with :envelope_with_arrow: in {apply_eka.mention} \n\n\n\n")
            embed.add_field(name=f"Want to join get GUEST role ?", value=f":sos: React with EKA logo in {about.mention} \n\n")
            #embed.set_image(url="attachment://recruitment.jpg")
            await welcomechannel.send(file=file,embed = embed)
    @commands.Cog.listener()
    async def on_member_remove(member):
        if member.guild.id == 561249245672374273:
            welcomechannel = client.get_channel(562568072146321418)
            embed = discord.Embed(title = "You Lost a member",
            description = f"{member} left {member.guild.name} server!",
            color = 0x07999b
            )
            await welcomechannel.send(embed = embed)



def setup(bot):
    bot.add_cog(Owner(bot))
