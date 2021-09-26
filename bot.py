import pickle
import discord
from discord.ext import commands

with open('token.txt', 'r') as token_file:
    token = (token_file.read())

loaded_model = pickle.load(open('xgb_model.sav', 'rb'))
loaded_vectorizer = pickle.load(open('vectorizer.sav', 'rb'))


client = commands.Bot(command_prefix='.')

# instant ban/mute
# democracy
# notify mods


# 3 strike system


@client.command(aliases=['id'])
async def get_bot_id(ctx):
    print('activated')
    await ctx.send(client.user.id)


@client.event
async def on_ready():
    print('bot is ready')


@client.event
async def on_message(message):
    msg = [message.content]
    vectorized = loaded_vectorizer.transform(msg)
    prediction = loaded_model.predict(vectorized)
    if prediction == [1] and message.author.id != client.user.id:
        if True:
            client_msg = await message.reply('<@' + str(message.guild.owner_id) + '>, It appears that toxic behaviour took '
                                                                            'place, do you want to take action?')
            await client_msg.add_reaction('\u2705')
            await client_msg.add_reaction('\u274c')


    await client.process_commands(message)


@client.event
async def on_reaction_add(reaction, user):
    if user != client.user:
        if str(reaction.emoji) == "\u2705":
            print('stay')
        if str(reaction.emoji) == "\u274c":
            print('delete')


client.run(token)
