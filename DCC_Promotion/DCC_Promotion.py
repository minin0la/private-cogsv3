from discord.ext import tasks
from redbot.core import Config
import discord
import os
import asyncio
from discord.ext import commands
import json
from fuzzywuzzy import process
from redbot.core import commands
from datetime import datetime


class DCC_PROMOTION(commands.Cog):
    """Its all about Downtown Cab Co - Promotion System"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    @commands.guild_only()
    @commands.has_any_role("CEO", "COO", "Bot-Developer", 'General Manager', 'Manager', 'Assistant Manager', 'CPO')
    async def promote(self, ctx, user: discord.Member, *, role_name: discord.Role):

        """Used to promote players"""
        author = ctx.author
        channel = self.bot.get_channel(367383714810036225) #Get linda-office channel
        bot_coders_channel = self.bot.get_channel(332558212429512704) #Get Bot-Coder channel
        old_role = user.top_role
        await ctx.message.delete()
        await user.add_roles(role_name)
        embed = discord.Embed(title="Downtown Cab Co. Management", colour=discord.Colour(
            0x7CFC00), description="Congratulations {},\n\nWe would like to inform you that you have been promoted from **{}** to **{}**\n\nKeep up the good work!".format(user.display_name, old_role.name, role_name.name))
        embed.set_thumbnail(
            url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
        await channel.send(embed=embed)
        try:
            await user.send(embed=embed)
        except discord.errors.Forbidden:
            await ctx.send("**[Warning]** {} turned off his PM".format(user.mention))
        await bot_coders_channel.send(content="{} uses command .promote to promote {} to rank {}".format(author.mention, user.mention, role_name.mention))

    @commands.command(pass_context=True, no_pm=True)
    @commands.guild_only()
    @commands.has_any_role("CEO", "COO", "Bot-Developer", 'General Manager', 'Manager', 'Assistant Manager', 'CPO')
    async def demote(self, ctx, user: discord.Member, *, role_name: discord.Role):

        """Used to demote players"""

        author = ctx.message.author
        channel = self.bot.get_channel(367383714810036225) #Get linda-office channel
        bot_coders_channel = self.bot.get_channel(332558212429512704) #Get Bot-Coder channel
        old_role = user.top_role
        await ctx.message.delete()
        await user.add_roles(role_name)
        while user.top_role != role_name:
            try:
                await user.remove_roles(user.top_role)
            except discord.Forbidden:
                await ctx.send("I don't have permissions to demote {}!".format(user.mention))
        date = datetime.now().strftime('%Y-%m-%d')
        embed = discord.Embed(title="Downtown Cab Co. Management", colour=discord.Colour(
            0xFF0000), description="Dear {},\n\nThe Management has reviewed your case and based on the information and testimonials available, henceforth effective from {}, you are demoted from **{}** to **{}**.\n\nIf you have any question, contact the management.".format(user.display_name, date, old_role.name, role_name.name))
        embed.set_thumbnail(
            url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
        await channel.send(embed=embed)
        try:
            await user.send(embed=embed)
        except discord.errors.Forbidden:
            await ctx.send("**[Warning]** {} turned off his PM".format(user.mention))
        await bot_coders_channel.send(content="{} uses command .demote to demote {} to rank {}".format(author.mention, user.mention, role_name.mention))

    @commands.command(pass_context=True, no_pm=True)
    @commands.guild_only()
    @commands.has_any_role("CEO", "COO", "Bot-Developer", 'General Manager', 'Manager', 'Assistant Manager', 'CPO')
    async def dismiss(self, ctx, user: discord.Member):

        """Used to dismiss players"""

        server = ctx.guild
        author = ctx.message.author
        channel = self.bot.get_channel(367383714810036225) #Get linda-office channel
        management = self.bot.get_channel(665362150440566807) #Get management channel
        visitor = ctx.guild.get_role(317392264571650058)
        await ctx.message.delete()
        while user.top_role != server.default_role:
            try:
                await user.remove_roles(user.top_role)
            except discord.Forbidden:
                await ctx.send("I don't have permissions to dismiss {}!".format(user.mention))
        await user.add_roles(visitor)
        date = datetime.now().strftime('%Y-%m-%d')
        embed = discord.Embed(title="Downtown Cab Co. Management", colour=discord.Colour(
            0xFF0000), description="Dear {},\n\nThe Management has reviewed your case and based on the information and testimonials available, henceforth effective from {}, you are terminated from DownTown Cab Co.\n\nIf you have any question, contact the management.".format(user.display_name, date))
        embed.set_thumbnail(
            url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
        await channel.send(embed=embed)
        try:
            await user.send(embed=embed)
        except discord.errors.Forbidden:
            await ctx.send("**[Warning]** {} turned off his PM".format(user.mention))
        await management.send(content="{} uses command .dismiss to dismiss {}".format(author.mention, user.mention))
    
    @commands.command(pass_context=True, no_pm=True)
    @commands.guild_only()
    @commands.has_any_role("CEO", "COO", "Bot-Developer", 'General Manager', 'Manager', 'Assistant Manager', 'CPO')
    async def suspend(self, ctx, user: discord.Member):

        """Used to suspend players"""

        server = ctx.message.guild
        author = ctx.message.author
        channel = self.bot.get_channel(367383714810036225) #Get linda-office channel
        management = self.bot.get_channel(665362150440566807) #Get management channel
        suspendrole = ctx.guild.get_role(605499324293447692) # Get Suspended Role
        await ctx.message.delete()
        while user.top_role != server.default_role:
            try:
                await user.remove_roles(user.top_role)
            except discord.Forbidden:
                await ctx.send("I don't have permissions to suspend {}!".format(user.mention))
        await user.add_roles(suspendrole)
        date = datetime.now().strftime('%Y-%m-%d')
        embed = discord.Embed(title="Downtown Cab Co. Management", colour=discord.Colour(
            0xFF0000), description="Dear {},\n\nThe Management has reviewed your case and based on the information and testimonials available, henceforth effective from {}, you are suspended until further notice.".format(user.display_name, date))
        embed.set_thumbnail(
            url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
        await channel.send(embed=embed)
        try:
            await user.send(embed=embed)
        except discord.errors.Forbidden:
            await ctx.send("**[Warning]** {} turned off his PM".format(user.mention))
        await management.send(content="{} uses command .suspend to suspend {}".format(author.mention, user.mention))

    @commands.command(pass_context=True, no_pm=True)
    @commands.guild_only()
    @commands.has_any_role("CEO", "COO", "Bot-Developer", 'General Manager', 'Manager', 'Assistant Manager', 'CPO')
    async def accept(self, ctx, user: discord.Member, *, role_name: discord.Role):

        """Used to accept players"""

        author = ctx.message.author
        channel = self.bot.get_channel(367383714810036225) #Get linda-office channel
        management = self.bot.get_channel(665362150440566807) #Get management channel
        interview = ctx.guild.get_role(353065275303788544)
        if role_name.name == "Trainee" or role_name.name == "Probationary Trainee":
            if any(r.name == 'Interviewee' for r in user.roles):
                await user.remove_roles(interview)
                await asyncio.sleep(1)
                await user.add_roles(role_name)
                embed = discord.Embed(title="Downtown Cab Co. Management", colour=discord.Colour(0x7CFC00), description="Dear {},\n\nCongratulation, you have been accepted into the team as {}. Read #faq-help and #announcements, if you have any questions feel free to ask. Good luck!".format(user.display_name, role_name.name))
                if user.avatar_url == "":
                    embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/k6AHx31fu7EiktzboQbX1BeOJ096MlVMKnXJawwYuF0/https/discordapp.com/api/guilds/301659110104104962/icons/71e58fd9b9c6a83b20f17b9eb8a671f8.jpg")
                else:
                    embed.set_thumbnail(url=user.avatar_url)
                await channel.send(content="@everyone {}".format(user.mention), embed=embed)
                try:
                    await user.send(embed=embed)
                except discord.errors.Forbidden:
                    await ctx.send("**[Warning]** {} turned off his PM".format(user.mention))
                await management.send(content="{} uses command .accept to accept {} to the team with {} Roles".format(author.mention, user.mention, role_name.mention))
            else:
                await ctx.send("""They must have the "Interview" Role""")
        else:
            await ctx.send("""You cannot accept them in {}. You can only accept them in `Trainee` or `Probationary Trainee`""".format(role_name.name))