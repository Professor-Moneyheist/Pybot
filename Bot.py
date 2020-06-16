import discord
from discord.ext import commands
from itertools import cycle
from discord.ext import tasks



client = commands.Bot(command_prefix = "!")
status = cycle(['Roblox', 'Fortnite'])

client.remove_command('help')

@tasks.loop(seconds = 10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)
    print("Bot is ready")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(" ``Invalid command used``")

@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, Member : discord.Member, *, reason = None ):
    await Member.kick(reason=reason)
    await ctx.send(" `` Kicked an insect from this server ``")

@kick.error
async def on_kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(" ``Usage: !kick @user reason``")
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You are not allowed to kick people")


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason = None ):

    await member.ban(reason=reason)
    await ctx.send(" `` Banned an musquito which spreads disease`` ")


@ban.error
async def on_ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(" ``Usage: !ban @user reason``")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You are not allowed to ban people")

@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator =member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(" `` Unbanned someone `` ")
            return

@unban.error
async def on_unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(" ``Usage: !unban name#tag ``")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You are not allowed to unban people")


@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)

@clear.error
async def on_clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(" ``Usage: !clear amount``")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You are not allowed to clear messages")


@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("Please specify a member")
        return
    role = discord.utils.get(ctx.guild.roles, name="muted")
    await member.add_roles(role)
    await ctx.send(" `` Muted an insect `` ")


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You are not allowed to mute people")


@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("Please specify a member")
        return
    role = discord.utils.get(ctx.guild.roles, name="muted")
    await member.remove_roles(role)
    await ctx.send("``unmuted someone``")


@mute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You are not allowed to unmute people")

@client.command(pass_context=True)
async def help(ctx):
  author = ctx.message.author
  embed = discord.Embed(title="Help - MODERATION", color=0xFFA500)
  embed.add_field(name= "prefix", value= "use '!' before commands", inline = False)
  embed.add_field(name="!ban", value="usage : !ban @user reason", inline=False)
  embed.add_field(name="!kick", value="usage : !kick @user reason", inline=False)
  embed.add_field(name="!unban", value="usage : !unban user#xxxx", inline=False)
  embed.add_field(name="!mute", value="usage : !mute @user", inline=False)
  embed.add_field(name="!unmute", value="usage : !unmute @user", inline=False)
  embed.add_field(name="!clear", value="usage : !clear <no of messages to be cleared>", inline=False)
  await ctx.send(author, embed=embed)
   
client.run(TOKEN)
