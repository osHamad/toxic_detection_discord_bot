import pickle
import discord
from discord.ext import commands
from bot_classes.bot_server import  Server
from bot_classes.flagged_messages import  Flagged

# initialize the server object
server = Server()

# grab token from token file
with open('token.txt', 'r') as token_file:
    token = (token_file.read())

# load the ML model for detecting toxic behaviour
loaded_model = pickle.load(open('xgb_model.sav', 'rb'))
loaded_vectorizer = pickle.load(open('vectorizer.sav', 'rb'))

# create the bot object and set prefix to '.'
client = commands.Bot(command_prefix='.')


# display the queue of the flagged messages and their senders
@client.command(aliases=['queue', 'q'])
async def flagged_queue(ctx):
    # flagged messages
    all_the = server.list_flags()
    embed = discord.Embed(title="Flagged Messages",
                          description="All unresolved flagged toxic behaviour",
                          color=0xFF5733)
    # create an embed field for every flagged message
    for i in all_the:
        embed.add_field(name=f'{str(i[0])}. {str(i[1])}', value=str(i[2]), inline=False)
    await ctx.send(embed=embed)


@client.command(aliases=['action', 'a'])
async def take_action(ctx, pos=0):
    # save flagged messages in the variable below
    blop = server.flagged

    # make sure that position inputted is in index
    try:
        person = blop[pos - 1]
        await ctx.send(f'this user will be banned: {person.sender} {person.number}')
    except IndexError:
        await ctx.send('out of range')


# print message when bot is up
@client.event
async def on_ready():
    print('bot is ready')


# toxic message detection
@client.event
async def on_message(message):
    # predict if the message is toxic or not using our ML model
    msg = [message.content]
    vectorized = loaded_vectorizer.transform(msg)
    prediction = loaded_model.predict(vectorized)

    # make sure that the sender is not the bot
    if prediction == [1] and message.author.id != client.user.id:
        # add message to the flagged list in server object
        server.add_flag(Flagged(message, server.get_flag_number()))
        # the 'if True' is for a future feature (setting the mod type)
        if True:
            await message.reply('<@' + str(message.guild.owner_id) + '> Toxic Behaviour Detected.')
            sender = message.author.id

            # adds strikes after each toxic message
            # the third strike will ban or mute the sender
            if sender in server.strikes:
                server.strikes[sender] += 1
                if server.strikes[sender] == 3:
                    print('three strikes, you are out')
            else:
                server.strikes[sender] = 1

    await client.process_commands(message)

client.run(token)
