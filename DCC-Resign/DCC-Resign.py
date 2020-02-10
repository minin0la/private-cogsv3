import discord
import os
from discord.ext import commands
from datetime import datetime
import asyncio


class DCC_RESIGN:
    """Its all about Downtown Cab Co - Resign System"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, no_pm=True)
    async def resign(self, ctx, *, themessage):

        """Use to write a resign letter. Please write a message after the command."""

        server = ctx.message.server
        author = ctx.message.author
        channel = discord.utils.get(server.channels, name='linda-office',
                                    type=discord.ChannelType.text)
        management = discord.utils.get(
            server.channels, name='management', type=discord.ChannelType.text)
        await self.bot.delete_message(ctx.message)
        date = datetime.now().strftime('%Y-%m-%d')
        embed = discord.Embed(title="To Downtown Cab Co. Management", colour=discord.Colour(
            0xFF0000), description="Dear Downtown Cab Co. Management,\n\nI would like to inform you that I am resigning from my position as {} for Downtown Cab Co., effective {}.\n\n{}\n\nSincerely,\n{}".format(author.top_role.mention, date, themessage, author.display_name))
        embed.set_thumbnail(
            url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
        await self.bot.send_message(channel, embed=embed)
        await self.bot.send_message(management, embed=embed)

def setup(bot):
    bot.add_cog(DCC_RESIGN(bot))