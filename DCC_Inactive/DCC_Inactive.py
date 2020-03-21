from discord.ext import tasks
from redbot.core import Config
import discord
import os
import asyncio
from discord.ext import commands
import json
from fuzzywuzzy import process
from redbot.core import commands
import time
import datetime
import difflib
class DCC_INACTIVE(commands.Cog):
    """Its all about Downtown Cab Co - Inactive System"""

    def __init__(self, bot):
        self.bot = bot
        self.database = Config.get_conf(self, identifier=1)
        data = {"Inactives": []}
        self.database.register_guild(**data)
        self.units = {"day": 86400, "week": 604800, "month": 2592000}
        self.check_inactives.start()
    
    def cog_unload(self):
        self.check_inactives.cancel()

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def inactive(self, ctx, quantity: int, time_unit: str, *, reason: str):
        """Generate Inactive Report

        The time unit must be: days, weeks, month
        For example:
        !inactive 3 days Holiday Time"""
        author = ctx.message.author
        time_unit = time_unit.lower()
        s = ""
        if time_unit.endswith("s"):
            time_unit = time_unit[:-1]
            s = "s"
        if not time_unit in self.units:
            await ctx.send("Invalid time unit. Choose days/weeks/month")
            return
        if quantity < 1:
            await ctx.send("Quantity must not be 0 or negative.")
            return
        if len(reason) > 1960:
            await ctx.send("The reason is too long.")
            return
        if author.nick is not None:
            name = author.nick
        else:
            name = author.name
        seconds = self.units[time_unit] * quantity
        future = int(time.time() + seconds)
        inactivity_info = discord.utils.get(ctx.guild.text_channels, name='inactivity-info')
        embed = discord.Embed(title="Downtown Cab Co. Absence Report", colour=discord.Colour(
            0xffff00), description="I wish to inform you that")
        embed.set_thumbnail(
            url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
        embed.set_author(name=name, icon_url=author.avatar_url)
        embed.set_footer(text="Posted by " + author.name + "#" + author.discriminator)
        embed.add_field(name="I will be absent for:", value="{} {}".format(
            str(quantity), time_unit + s), inline=False)
        embed.add_field(name="Reason:", value=reason)
        msg = await inactivity_info.send(embed=embed)
        await ctx.message.delete()
        async with self.database.guild(ctx.guild).Inactives() as inactives:
            inactives.append({"ID": author.id, "NAME": name, "FUTURE": future, "REASON": reason, "MSG": msg.id})
        # await self.database.guild(ctx.guild).Inactives.set(inactives)

    @commands.command(pass_context=True, aliases=["cinactive"])
    @commands.guild_only()
    async def cancelinactive(self, ctx):
        """Removes all your inactive reports"""
        author = ctx.message.author
        inactivity_info_channel = discord.utils.get(ctx.guild.text_channels, name='inactivity-info')
        to_remove = []
        async with self.database.guild(ctx.guild).Inactives() as inactives:
            for inactive in inactives:
                if inactive["ID"] == author.id:
                    to_remove.append(inactive)

            if not to_remove == []:
                for inactive in to_remove:
                    inactives.remove(inactive)
                # await self.database.guild(ctx.guild).Inactives.set(inactives)
                try:
                    themessage = await inactivity_info_channel.fetch_message(inactive["MSG"])
                    await themessage.delete()
                except discord.errors.HTTPException:
                    pass
                except (discord.errors.Forbidden, discord.errors.NotFound):
                    pass
                await ctx.send("All your inactivity reports have been removed.")
            else:
                await ctx.send("You don't have any inactivity reports.")

    @commands.command(pass_context=True, aliases=["rinactive"])
    @commands.guild_only()
    @commands.has_any_role("CEO", "COO", "Human Resources Director", "Human Resources Representative", "Team Leader", "Bot-Developer", "General Manager", "Manager", "Assistant Manager")
    async def removeinactive(self, ctx, report_id: str):
        """Remove a specific inactive reports"""
        # author = ctx.message.author
        inactivity_info_channel = discord.utils.get(ctx.guild.text_channels, name='inactivity-info') #Get Inactive-Info Channel
        to_remove = []
        async with self.database.guild(ctx.guild).Inactives() as inactives:
            for inactive in inactives:
                try:
                    if inactive["MSG"] == int(report_id):
                        to_remove.append(inactive)
                except KeyError:
                    pass

            if not to_remove == []:
                for inactive in to_remove:
                    inactives.remove(inactive)
                # await self.database.guild(ctx.guild).Inactives.set(inactives)
                try:
                    themessage = await inactivity_info_channel.fetch_message(inactive["MSG"])
                    await themessage.delete()
                except discord.errors.HTTPException:
                    pass
                except (discord.errors.Forbidden, discord.errors.NotFound):
                    pass
                await ctx.send("The inactive report #{} has been deleted".format(inactive["MSG"]))
            else:
                await ctx.send("Nothing to delete")

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_any_role("CEO", "COO", "Human Resources Director", "Human Resources Representative", "Team Leader", "Bot-Developer", "General Manager", "Manager", "Assistant Manager")
    async def inactivelist(self, ctx, *, name=None):
        """list all inactive reports"""
        server = ctx.message.guild
        number = 1
        pagenumber = 0
        namelist = ""
        allname = []
        if name is None:
            await ctx.send("__**All inactive Report List**__\n")
            inactives = await self.database.guild(ctx.guild).Inactives()
            for inactive in inactives:
                timeleft = inactive["FUTURE"] - int(time.time())
                member = server.get_member(inactive["ID"])
                if pagenumber < 5:
                    try:
                        top_role = member.top_role
                        namelist = namelist + "{}. **{}**,\n**Position:** {}\n**Time Left:** {}\n**Reason:** {}".format(str(number), inactive["NAME"], top_role.name, datetime.timedelta(seconds=timeleft), inactive["REASON"])
                        try:
                            namelist = namelist + "\n**Report ID:** {}\n\n".format(inactive["MSG"])
                        except KeyError:
                            namelist = namelist + "\n\n"
                        number = number + 1
                        pagenumber = pagenumber + 1
                    except:
                        pass
                else:
                    await ctx.send(namelist)
                    namelist = ""
                    pagenumber = 0
            if pagenumber > 0:
                await ctx.send(namelist)
        else:
            inactives = await self.database.guild(ctx.guild).Inactives()
            for inactive in inactives:
                allname.append(inactive["NAME"])
            allname_new = {n.lower(): n for n in allname}
            allname_matched = [allname_new[r] for r in difflib.get_close_matches(name.lower(), allname_new, 1, 0.6)]
            if str(allname_matched) != "[]":
                for inactive in inactives:
                    if inactive["NAME"] == allname_matched[0]:
                        timeleft = inactive["FUTURE"] - int(time.time())
                        member = server.get_member(inactive["ID"])
                        top_role = member.top_role
                        namelist = namelist + "{}. **{}**,\n**Position:** {}\n**Time Left:** {}\n**Reason:** {}".format(str(number), inactive["NAME"], top_role.name, datetime.timedelta(seconds=timeleft), inactive["REASON"])
                        try:
                            namelist = namelist + "\n**Report ID:** {}\n\n".format(inactive["MSG"])
                        except KeyError:
                            namelist = namelist + "\n\n"
                        number = number + 1
                await ctx.send("__**Inactive Report List**__\n" + namelist)
            else:
                await ctx.send("**Not Found**\n**Try to provide more details on your search**")

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def myinactive(self, ctx):
        """list your inactive reports"""
        server = ctx.message.guild
        number = 1
        namelist = ""
        inactives = await self.database.guild(ctx.guild).Inactives()
        for inactive in inactives:
            if inactive["ID"] == ctx.message.author.id:
                name = inactive["NAME"]
                timeleft = inactive["FUTURE"] - int(time.time())
                member = server.get_member(inactive["ID"])
                top_role = member.top_role
                namelist = namelist + "{}. **{}**,\n**Position:** {}\n**Time Left:** {}\n**Reason:** {}".format(str(number), inactive["NAME"], top_role.name, datetime.timedelta(seconds=timeleft), inactive["REASON"])
                try:
                    namelist = namelist + "\n**Report ID:** {}\n\n".format(inactive["MSG"])
                except KeyError:
                    namelist = namelist + "\n\n"
                number = number + 1
        if namelist is not "":
            await ctx.send("__**Inactive Report List for {}**__".format(name))
            await ctx.send(namelist)
        else:
            await ctx.send("**You do not have any inactive report**")
    
    @tasks.loop(seconds=300.0)
    async def check_inactives(self):
        print("Checking Inactives")
        getDCCserver = self.bot.get_guild(301659110104104962)
        management = discord.utils.get(getDCCserver.text_channels, name='management') #Get management channel
        to_remove = []
        async with self.database.guild(getDCCserver).Inactives() as inactives:
            for inactive in inactives:
                if inactive["FUTURE"] <= int(time.time()):
                    try:
                        embed = discord.Embed(colour=discord.Colour(0xff0000))

                        embed.set_thumbnail(url="http://www.freeiconspng.com/download/13396")
                        embed.set_author(name="{}".format(
                            inactive["NAME"]), icon_url="http://www.freeiconspng.com/download/13396")

                        embed.add_field(name="Downtown Cab Co. Annual leave Application",
                                        value="The annual leave application has been expired")

                        await management.send(embed=embed)
                        member = getDCCserver.get_member(inactive["ID"])
                        await member.send(embed=embed)
                    except (discord.errors.Forbidden, discord.errors.NotFound):
                        to_remove.append(inactive)
                    except discord.errors.HTTPException:
                        pass
                    else:
                        to_remove.append(inactive)
            for inactive in to_remove:
                inactives.remove(inactive)
        # if to_remove:
        #     await self.database.guild(getDCCserver).Inactives.set(inactives)
    
    @check_inactives.before_loop
    async def before_check_inactives(self):
        print('waiting...')
        await self.bot.wait_until_ready()