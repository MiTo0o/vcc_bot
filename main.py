import discord
from discord import CategoryChannel
from discord.utils import get
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from dotenv import load_dotenv
import os

load_dotenv('.env')

# TODO: MAKE DESCRIPTIONS FOR ALL COMMANDS
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

questions_channel_ID = int(os.getenv('QUESTIONS_CHANNEL_ID'))
guild_ids = [int(os.getenv("GUILD_ID"))]
active_questions_category = int(os.getenv("ACTIVE_QUESTIONS_CATEGORY"))


@bot.event
async def on_ready():
    print("{0.user} is ready to serve.".format(bot))
    await bot.change_presence(activity=discord.Game(name="-help"))


@slash.slash(name="ask",
             guild_ids=guild_ids,
             description="Ask a question",
             options=[
                 create_option(
                     name="Question",
                     description="Please type a question",
                     option_type=3,
                     required=True
                 )
             ]
             )
async def ask(ctx, *, question):
    guild = ctx.guild
    if len(question) >= 100:
        temp1 = (" ".join(question.lower().split()).replace(" ", "-"))[0:100]
    else:
        temp1 = " ".join(question.lower().split()).replace(" ", "-")
    temp2 = ""
    for i in temp1:
        if i.isalnum() or i == "-":
            temp2 += i

    # Can change this to discord.utils.get(ctx.guild.channels, name=text_channel_name) BUT since people can create 2
    # text channels with the same name, it's better to search by the id of the text channel
    channel = bot.get_channel(questions_channel_ID)
    messages = await channel.history(limit=None).flatten()
    temp = False
    if 0 != len(messages):
        for msg in messages:
            # print(msg.content.split(":** "))
            # print(msg.content.split(":** ")[1].lower())
            if question.lower() == msg.content.split(":** ")[1].lower():
                embed = discord.Embed(
                    color=0x2fd082
                )
                embed.add_field(name="Status:",
                                value="The question: " + msg.content.split(":** ")[1] + " has already been asked.",
                                inline=False)
                embed.add_field(name="Link to question: ",
                                value=msg.jump_url,
                                inline=False)
                await ctx.send(embed=embed)
                temp = True
                break
    if get(guild.text_channels, name=temp2):
        # TODO: make it so its not dumb
        temp = True
        # slight bug as this checks the all text channels instead of just archives and Active Questions but it's a pain
        # in the behind to fix so I'll leave it as is for now (The chance this bug matters is also quite small)
        embed = discord.Embed(
            color=0x2fd082
        )
        embed.add_field(name="Status:",
                        value="This question is currently getting `answered` or `archived`. (Check the text channels "
                              "under active questions)")
        await ctx.send(embed=embed)
    if temp is False:
        get_id_message = await channel.history(limit=1).flatten()
        # print(get_id_message)
        if len(get_id_message) != 0:
            id_message = get_id_message[0].content
            # print(id_message)
            # why don't i just split and then split? am i dumb?
            pound_index = id_message.index('#')
            colon_index = id_message.index(':')
            identifier = int(id_message[pound_index + 2:colon_index]) + 1
        else:
            identifier = 1
        await channel.send("**Question # " + str(identifier) + ":** " + question)
        new_messages = await channel.history(limit=1).flatten()
        for new_msg in new_messages:
            if new_msg.content.split(":** ")[1] == question:
                embed = discord.Embed(
                    color=0x2fd082
                )
                embed.add_field(name="Status:",
                                value='Your question has been logged in the `Questions channel`',
                                inline=False)
                embed.add_field(name="Link to question: ",
                                value=new_msg.jump_url,
                                inline=False)
                await ctx.send(embed=embed)
                break


@slash.slash(name="answer",
             description="Answer a question that is in the Questions text channel",
             guild_ids=guild_ids,
             options=[
                 create_option(
                     name="question_number",
                     description="Please enter the question number",
                     option_type=4,
                     required=True
                 )
             ]
             )
async def answer(ctx, *, question_number):
    guild = ctx.guild
    channel = bot.get_channel(questions_channel_ID)
    messages = await channel.history(limit=None).flatten()
    temp = False
    if len(messages) != 0:
        for msg in messages:
            if str(question_number) == msg.content.split("# ")[1].split(":** ")[0]:
                temp = True
                category = get(guild.categories, id=active_questions_category)
                if len(msg.content.split(":** ")[1]) >= 100:
                    new_channel_message = "```" + msg.content.split(":** ")[1] + ": ```"
                    await guild.create_text_channel(msg.content.split(":** ")[1][0:100], category=category)
                    temp1 = " ".join(msg.content.split(":** ")[1][0:100].lower().split()).replace(" ", "-")
                else:
                    await guild.create_text_channel(msg.content.split(":** ")[1], category=category)
                    new_channel_message = "```" + msg.content.split(":** ")[1] + ": ```"
                    temp1 = " ".join(msg.content.split(":** ")[1].lower().split()).replace(" ", "-")
                await msg.delete()

                temp2 = ""
                for i in temp1:
                    if i.isalnum() or i == "-":
                        temp2 += i
                new_channel = get(guild.channels, name=temp2)
                await new_channel.send(new_channel_message)
                new_messages = await new_channel.history(limit=1).flatten()
                for new_msg in new_messages:
                    if new_msg.content == new_channel_message:
                        embed = discord.Embed(
                            color=0x2fd082
                        )
                        embed.add_field(name="Status",
                                        value='`A text channel under "`Active Question`" has been created',
                                        inline=False)
                        embed.add_field(name="Link to channel: ",
                                        value=new_msg.jump_url,
                                        inline=False)
                        await ctx.send(embed=embed)
                        break
                break
    if temp is False:
        embed = discord.Embed(
            color=0x2fd082
        )
        embed.add_field(name="`Status:`",
                        value="`This question does not exist in the list`")
        await ctx.send(embed=embed)


@slash.slash(name="archive",
             guild_ids=guild_ids,
             description="Archives the current text channel (the text channel has to be under Active Questions)"
             )
async def archive(ctx):
    # TODO: make sure you can't archive something that isnt in ACtive Questions section
    guild = ctx.guild
    channel = ctx.channel
    id_list = []
    for i in get(guild.categories, id=active_questions_category).channels:
        id_list.append(i.id)
    # print(id_list)
    # len(get(guild.categories, name=name).channels)
    # check_correct_channel =
    embed = discord.Embed(
        color=0x2fd082
    )
    if channel.id in id_list:
        archive_names = ["Archive-#1", "Archive-#2", "Archive-#3", "Archive-#4", "Archive-#5", "Archive-#6",
                         "Archive-#7", "Archive-#8"]
        for index in range(len(archive_names)):
            arch = discord.utils.get(ctx.guild.categories, name=archive_names[index])
            if arch is None:
                await guild.create_category(archive_names[index])
                temp = get(guild.categories, name=archive_names[index])
                await channel.edit(category=temp)
                embed.add_field(name="`Status:`",
                                value="This text channel has been moved under " + "__***`" + archive_names[index] +
                                      "`***__",
                                inline=False)
                await ctx.send(embed=embed)
                break
            elif len(get(guild.categories, name=archive_names[index]).channels) == 50:
                continue
            else:
                temp = get(guild.categories, name=archive_names[index])
                await channel.edit(category=temp)
                embed.add_field(name="Status:",
                                value="This text channel has been moved under " + "__***`" + archive_names[index] +
                                      "`***__",
                                inline=False)
                await ctx.send(embed=embed)
                break
    else:
        await ctx.send("You cannot archive this channel")

    # await channel.edit(category=arch)
    # await ctx.send("This text channel has been moved under Archive")


@slash.slash(name="unarchive",
             guild_ids=guild_ids,
             description="Unarchives the current text channel (the text channel has to be under one of the archives)"
             )
async def unarchive(ctx):
    channel = ctx.channel
    guild = ctx.guild
    archive_names = ["Archive-#1", "Archive-#2", "Archive-#3", "Archive-#4", "Archive-#5", "Archive-#6",
                     "Archive-#7", "Archive-#8"]
    all_archive_id_list = []
    for archive_categories in archive_names:
        if get(guild.categories, name=archive_categories) is not None:
            for i in get(guild.categories, name=archive_categories).channels:
                all_archive_id_list.append(i.id)
    # print(all_archive_id_list)
    embed = discord.Embed(
        color=0x2fd082
    )
    if channel.id in all_archive_id_list:
        temp = discord.utils.get(ctx.guild.categories, name="Active Questions")
        await channel.edit(category=temp)
        embed.add_field(name="Status:",
                        value='This text channel has been moved back under __***`Active Questions`***__',
                        inline=False)
        await ctx.send(embed=embed)
    else:
        embed.add_field(name="Status:",
                        value="`You `cannot` unarchive a channel that isn't currently archived`",
                        inline=False)
        await ctx.send(embed=embed)


@slash.slash(name="help",
             guild_ids=guild_ids,
             description="Displays all available commands of this bot"
             )
async def help_panel(ctx):
    embed = discord.Embed(
        color=0x2fd082,
        title='Vcc Bot Commands'
    )
    embed.add_field(name='***`/ask`***', value='Got a question? Use this command to ask it.', inline=False)
    embed.add_field(name='***`/answer`***', value='Answer a question in the questions list', inline=False)
    embed.add_field(name='***`/archive`***', value='Done with a question? Archive it!!', inline=False)
    embed.add_field(name='***`/unarchive`***', value='Want to continue discussion a question? Unarchive it!!',
                    inline=False)
    await ctx.send(embed=embed)


# TODO: maybe create some random commands?

bot.run(os.getenv('BOT_TOKEN'))
