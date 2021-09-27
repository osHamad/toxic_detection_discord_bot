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
    if user.id == user.guild.owner_id:
        if str(reaction.emoji) == "\u2705":
            print('stay')
        if str(reaction.emoji) == "\u274c":
            print('delete')




@client.command(name='feedback', help='Ask person for feedback')
async def roll(ctx):
    message = await ctx.send('Are you enjoying this bot? \n :thumbsup: :-1: ')

    thumb_up = '👍'
    thumb_down = '👎'

    await message.add_reaction(thumb_up)
    await message.add_reaction(thumb_down)

    def check(reaction, user):
        return user == ctx.author and str(
            reaction.emoji) in [thumb_up, thumb_down]

    member = ctx.author

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=10.0, check=check)

            if str(reaction.emoji) == thumb_up:
                await ctx.send('Thank you for your feedback')


            if str(reaction.emoji) == thumb_down:
                await ctx.send('Sorry you feel that way')


client.run(token)
