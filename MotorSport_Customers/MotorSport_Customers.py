import discord
import os
from discord.ext import commands
from redbot.core import commands
from redbot.core import Config
from redbot.core import utils
from redbot.core import checks
import asyncio

class MOTORSPORT_CUSTOMERS(commands.Cog):
    """Its all about Motorsport - Customer Systems"""

    def __init__(self, bot):
        self.bot = bot
        self.database = Config.get_conf(self, identifier=1)
        data = {"Name": "",
                "MemberID": "",
                "Orders": [],
                "VIP_Status": False,
                "Customer_Status": False,
                "Shopper_Status": True,
        }
        self.database.register_member(**data)

    @commands.command(pass_context=True)
    async def register(self, ctx, *, name: str):
        """Use to register an account with Motorsport
        Usage: !register <name>
        Example: !register Jasper Akerman"""

        author = ctx.author
        await self.database.member(author).Name.set(name)
        await self.database.member(author).MemberID.set(author.id)
        shopper_role = ctx.guild.get_role(482965019189968927)
        await author.add_roles(shopper_role)
        embed = discord.Embed(title="Motorsport Management", colour=discord.Colour(
            0xFF00FF), description="Dear {},\n\nThank you for registering a membership with us at Premium Deluxe Motorsport!".format(name))
        embed.set_thumbnail(
            url='https://i.imgur.com/xJyIgAQ.png')
        await ctx.send(embed=embed)
    
    @commands.command(pass_context=True)
    async def membership(self, ctx):
        author = ctx.author
        membershipinfo = await self.database.member(author).get_raw()
        if membershipinfo['Name'] != "":
            embed = discord.Embed(title="Motorsport Membership", colour=discord.Colour(0xFF00FF))
            embed.set_thumbnail(url='https://i.imgur.com/xJyIgAQ.png')
            embed.set_author(name=membershipinfo['Name'], icon_url=author.avatar_url)
            embed.add_field(name="Number of Purchased", value=len(membershipinfo['Orders']), inline=False)
            embed.add_field(name="VIP", value=membershipinfo['VIP_Status'], inline=True)
            embed.add_field(name="Customer", value=membershipinfo['Customer_Status'], inline=True)
            embed.add_field(name="Shopper", value=membershipinfo['Shopper_Status'], inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Please register with us first with !register or start ordering with !order")
    
    @commands.command(pass_context=True)
    async def unregister(self, ctx):
        author = ctx.author
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        try:
            await ctx.send("Are you sure you want to unregister? All data will be ereased. (Yes/No)")
            answer = await self.bot.wait_for('message', check=check, timeout=120)
            if answer.content.lower() == "yes":
                await self.database.member(author).clear()
                await ctx.send("You have unregistered your membership here.")
            else:
                await ctx.send("Nothing has been done.")
        except asyncio.TimeoutError:
                await ctx.send("You did not answer in time.")

    @commands.command(pass_context=True)
    async def myorders(self, ctx, user: discord.Member = None):
        if user is None:
            author = ctx.author
        else:
            author = user
        membershipinfo = await self.database.member(author).get_raw()
        shipping = ""
        collection = ""
        completed = ""
        try:
            if membershipinfo['Name'] != "":
                embed = discord.Embed(title="Motorsport Orders", colour=discord.Colour(0xFF00FF))
                embed.set_thumbnail(url='https://i.imgur.com/xJyIgAQ.png')
                embed.set_author(name=membershipinfo['Name'], icon_url=author.avatar_url)
                try:
                    for x in membershipinfo['Orders']:
                        if x['Status'] == "Shipping":
                            shipping = shipping + "- {} (Order ID: {})\n".format(x['Vehicle_Name'], x['Order_ID'])
                        if x['Status'] == "Collection":
                            collection = collection + "- {} (Order ID: {})\n".format(x['Vehicle_Name'], x['Order_ID'])
                        if x['Status'] == "Completed":
                            completed = completed + "- {} (Order ID: {})\n".format(x['Vehicle_Name'], x['Order_ID'])
                    shipping = utils.chat_formatting.pagify(shipping, delims="\n", page_length=1000)
                    collection = utils.chat_formatting.pagify(collection, delims="\n", page_length=1000)
                    completed = utils.chat_formatting.pagify(completed, delims="\n", page_length=1000)
                    for num, x in enumerate(shipping, 1):
                        x = "```diff\n" + x + "```"
                        embed.add_field(name="Shipping ({})".format(num), value=x, inline=False)
                    for num, x in enumerate(collection, 1):
                        x = "```diff\n" + x + "```"
                        embed.add_field(name="Collection ({})".format(num), value=x, inline=False)
                    for num, x in enumerate(completed, 1):
                        x = "```diff\n" + x + "```"
                        embed.add_field(name="Completed ({})".format(num), value=x, inline=True)
                    await ctx.send(embed=embed)
                except:
                    embed.add_field(name="", value="No history", inline=False)
            else:
                await ctx.send("Please register with us first with !register or start ordering with !order")
        except:
            pass
    
    @commands.command(pass_context=True)
    async def getmessage(self, ctx):
        author = ctx.author
        data = []
        final_data = []
        counter = 0
        themessage = ""
        channel = self.bot.get_channel(341936700366258177)
        message = await channel.history(limit=3000).flatten()
        for x in message:
            try:
                message_data = x.embeds[0].to_dict()
                for y in message_data['fields']:
                    if y['name'] == 'Discord':
                        data.append(y['value'])
            except:
                pass
        data = list(dict.fromkeys(data))
        for x in data:
            for y in message:
                try:
                    message_data = y.embeds[0].to_dict()
                    for c in message_data['fields']:
                        if c['name'] == 'Discord' and c['value'] == x:
                            counter = counter + 1
                except:
                    pass
            final_data.append({"Name": str(x), "Count": counter})
            counter = 0
        final_data = sorted(final_data, key=lambda k: k['Count'])
        for x in final_data:
            themessage = themessage + x['Name'] + ' ({})\n'.format(x['Count'])


        themessage = utils.chat_formatting.pagify(themessage, delims="\n", page_length=1000)
        for q in themessage:
            await ctx.send(q)

    @commands.command(pass_context=True)
    async def importorders(self, ctx):
        guild = ctx.guild
        channel = self.bot.get_channel(341936700366258177)
        message = await channel.history(limit=3000).flatten()
        counter = 0
        for x in message:
            try:
                message_data = x.embeds[0].to_dict()
                for y in message_data['fields']:
                    if y['name'] == 'Discord':
                        memberid = y['value']
                    if y['name'] == 'Vehicle Name':
                        car_name = y['value']
                    if y['name'] == 'Price':
                        price = y['value'].replace("$ ","").replace(',',"")
                        price = int(price)
                new_memberid = memberid.replace("<", "").replace(">", "").replace("@", "").replace("!", "")
                member = guild.get_member(int(new_memberid))
                async with self.database.member(member).Orders() as orders:
                    orders.append({"Order_ID": x.id, "Vehicle_Name": car_name, "Price": price, "Status": "Collection"})
                    counter = counter + 1
            except:
                pass
        await ctx.send("Imported {}".format(counter))

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def clearall_customer(self, ctx):
        await self.database.clear_all()
        await ctx.send("Cleared All")        

    
    @commands.command(pass_context=True)
    async def totalspent(self, ctx, user: discord.Member = None):
        if user is None:
            author = ctx.author
        else:
            author = user
        value = 0
        orders = await self.database.member(author).Orders()
        for x in orders:
            value = value + x['Price']
        await ctx.send("Total Spent: $" + str(value))


    @commands.command(pass_context=True)
    async def cancelorder(self, ctx, Order_ID: int):
        async with self.database.member(ctx.author).Orders() as orders:
            try:
                if Order_ID in orders[0].values():
                    order_channel = self.bot.get_channel(341936700366258177)
                    message = await order_channel.fetch_message(Order_ID)
                    message_data = message.embeds[0].to_dict()
                    message.embeds[0].set_author(name='~~' + message_data['author']['name'] + '~~' + ' **(Cancelled)**', icon_url=message_data['author']['icon_url'])
                    orders[:] = [d for d in orders if d.get('Order_ID') != Order_ID]
                    try:
                        await message.edit(embed=message.embeds[0])
                        await message.clear_reactions()
                    except discord.errors.Forbidden:
                        pass
                    await ctx.send("Order #{} has been cancelled".format(Order_ID))
                else:
                    await ctx.send("Order #{} not found".format(Order_ID))
            except IndexError:
                await ctx.send("You have not placed any order yet")

    @commands.command(pass_context=True, no_pm=True)
    @commands.has_permissions(manage_roles=True)
    async def givecustomer(self, ctx, user: discord.Member):

        """Use to give Customer to players"""
        author = ctx.message.author
        management = self.bot.get_channel(341936003029794826)
        customer_role = ctx.guild.get_role(343722834016862211)
        await user.add_roles(customer_role)
        embed = discord.Embed(title="Motorsport Management", colour=discord.Colour(
            0xFF00FF), description="Dear {},\n\nThank you for shopping at Premium Deluxe Motorsport, we would truly appreciate if you could spare some time to send us a picture of the vehicle you purchased with a small comment in our <#343722557381279745> channel.\n\nWe hope that your purchasing experience here was satisfactory, and a huge thanks to you for supporting Motorsports.\nHave a wonderful day & enjoy your new vehicle!".format(user.display_name))
        embed.set_thumbnail(
            url='https://i.imgur.com/xJyIgAQ.png')
        await self.database.member(user).Customer_Status.set(True)
        try:
            await user.send(embed=embed)
        except discord.errors.Forbidden:
            await management.send(content="**[Warning]** {} turned off his PM".format(user.mention))
        await management.send(content="{} uses command !givecustomer to give {} {} role".format(author.mention, user.mention, customer_role.mention))

    @commands.command(pass_context=True, no_pm=True)
    @commands.has_permissions(manage_roles=True)
    async def givevip(self, ctx, user: discord.Member):

        """Use to give VIP to players"""
        author = ctx.message.author
        management = self.bot.get_channel(341936003029794826)
        VIP_role = ctx.guild.get_role(345786815959007234)
        await user.add_roles(VIP_role)
        embed = discord.Embed(title="Motorsport Management", colour=discord.Colour(
            0xFF0000), description="Dear {},\n\nBecause of your continuous support here at Motorsports, we are pleased to inform you that you are now a VIP customer! View our <#345600420883988481> channel for more details, take note that you are now entitled to VIP discounts!\nHave a fantastic day & enjoy your new perks!".format(user.display_name))
        embed.set_thumbnail(
            url="http://cdn.quotesgram.com/img/41/24/1219260287-icon_vip.png")
        await self.database.member(user).VIP_Status.set(True)
        try:
            await user.send(embed=embed)
        except discord.errors.Forbidden:
            await management.send(content="**[Warning]** {} turned off his PM".format(user.mention))
        await management.send(content="{} uses command !givevip to give {} {} role".format(author.mention, user.mention, VIP_role.mention))
    
    @commands.command(pass_context=True, no_pm=True)
    @commands.has_permissions(manage_roles=True)
    async def done(self, ctx, user: discord.Member):

        """Use to notify about stock ready to player"""
        # management = discord.utils.get(server.channels, name='management',
        #                             type=discord.ChannelType.text)
        # customer_role = discord.utils.get(server.roles, name='VIP')
        # await user.add_roles(customer_role)
        embed = discord.Embed(title="Motorsport Notification", colour=discord.Colour(
            0xFF0000), description="Your brand new vehicle is ready for collection at Motorsports, the dealership located next to Mors Insurance.\nEnjoy! :smile:")
        embed.set_thumbnail(url="https://i.imgur.com/xJyIgAQ.png")
        embed.set_image(url="https://i.imgur.com/NssiDxp.png")
        try:
            await user.send(embed=embed)
        except discord.errors.Forbidden:
            await ctx.send("**[Warning]** {} turned off his PM".format(user.mention))
