# @bot.command()
# # async def bus(ctx, *, xd):
# #     guild = ctx.guild
# #     temp_xd = " ".join(xd.lower().split()).replace(" ", "-")
# #     temp_xd2 = ""
# #
# #     for i in temp_xd:
# #         if i.isalnum() or i == "-":
# #             temp_xd2 += i
# #
# #     if get(guild.text_channels, name=temp_xd2):
# #         await ctx.send("There's already a text channel open for this question. (It may also be answered and is the "
# #                        "archived tab)")
# #     else:
# #         name = "Active Questions"
# #         category = get(guild.categories, name=name)
# #         await guild.create_text_channel(xd, category=category)
# #     print(xd)
# #     print(temp_xd2)

# ---------------------------------------------------------------------------------------------------------------------

# @bot.event
# async def on_message(message):
#     print(message.content)
#     if message.author == bot.user:
#         return
#     if message.content.startswith("/archive"):
#         guild = message.channel.guild
#         channel = message.channel
#         name = "Active Questions"
#         temp = get(guild.categories, name=name).channels

# ---------------------------------------------------------------------------------------------------------------------

# @slash.slash(name="answer",
#              description="answer a question that exist in the Questions text channel",
#              guild_ids=guild_ids,
#              options=[
#                  create_option(
#                      name="optone",
#                      description="This is the first option we have.",
#                      option_type=3,
#                      required=False,
#                      choices=[
#                          create_choice(
#                              name="ChoiceOne",
#                              value="DOGE!"
#                          ),
#                          create_choice(
#                              name="ChoiceTwo",
#                              value="NO DOGE"
#                          )
#                      ]
#                  )
#              ])

# ---------------------------------------------------------------------------------------------------------------------

# @bot.command()
# async def search(ctx, *, question):
#     # enter the id of the text channel you want to search
#     channel = bot.get_channel(questions_channel_ID)
#     messages = await channel.history(limit=None).flatten()
#     for msg in messages:
#         if question in msg.content:
#             await ctx.send(msg.jump_url)

# ---------------------------------------------------------------------------------------------------------------------

# @slash.slash(name="answer",
#              description="answer a question that exist in the Questions text channel",
#              guild_ids=guild_ids,
#              )
# async def answer(ctx, *, question):
#     guild = ctx.guild
#     channel = bot.get_channel(questions_channel_ID)
#     messages = await channel.history(limit=None).flatten()
#
#     temp = False
#     for msg in messages:
#         if question.lower() == msg.content.lower():
#             temp = True
#             name = "Active Questions"
#             category = get(guild.categories, name=name)
#             await guild.create_text_channel(question, category=category)
#             await msg.delete()
#
#             temp1 = " ".join(question.lower().split()).replace(" ", "-")
#             temp2 = ""
#             for i in temp1:
#                 if i.isalnum() or i == "-":
#                     temp2 += i
#             new_channel = get(guild.channels, name=temp2)
#             await new_channel.send("Answer your question here!")
#             new_messages = await new_channel.history(limit=None).flatten()
#             for new_msg in new_messages:
#                 if new_msg.content == "Answer your question here!":
#                     embed = discord.Embed(
#                         colour=discord.Colour.blue()
#                     )
#                     embed.add_field(name="Status:",
#                                     value='A text channel under "Active Question" has been created',
#                                     inline=False)
#                     embed.add_field(name="Link to channel: ",
#                                     value=new_msg.jump_url,
#                                     inline=False)
#                     await ctx.send(embed=embed)
#                     break
#             break
#     if temp is False:
#         await ctx.send("There is so such question for you to answer")