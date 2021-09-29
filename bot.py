import pickle
import discord
from discord.ext import commands
from bot_classes.bot_server import  Server
from bot_classes.flagged_messages import  Flagged

server = Server()

with open('token.txt', 'r') as token_file:
    token = (token_file.read())

loaded_model = pickle.load(open('xgb_model.sav', 'rb'))
loaded_vectorizer = pickle.load(open('vectorizer.sav', 'rb'))


client = commands.Bot(command_prefix='.')

# instant ban/mute
# democracy
# notify mods


# 3 strike system


@client.command(aliases=['queue', 'q'])
async def flagged_queue(ctx):
    all_the = server.list_flags()
    embed = discord.Embed(title="Flagged Messages",
                          description="All unresolved flagged toxic behaviour",
                          color=0xFF5733)
    for i in all_the:
        embed.add_field(name=f'{str(i[0])}. {str(i[1])}', value=str(i[2]), inline=False)
    await ctx.send(embed=embed)


@client.command(aliases=['action', 'a'])
async def take_action(ctx, pos=0):
    blop = server.flagged
    if len(blop) > 0 and abs(pos) in range(len(blop)):
        person = blop[pos - 1]
        await ctx.send(f'this user will be banned: {person.sender} {person.number}')
    else:
        await ctx.send('out of range')


@client.event
async def on_ready():
    print('bot is ready')


@client.event
async def on_message(message):
    msg = [message.content]
    vectorized = loaded_vectorizer.transform(msg)
    prediction = loaded_model.predict(vectorized)
    if prediction == [1] and message.author.id != client.user.id:
        server.add_flag(Flagged(message, server.get_flag_number()))
        # for now working only on the notifying mods feature
        if True:
            await message.reply('<@' + str(message.guild.owner_id) + '> Toxic Behaviour Detected.')
            sender = message.author.id
            if sender in server.strikes:
                server.strikes[sender] += 1
                if server.strikes[sender] == 3:
                    print('three strikes, you are out')
            else:
                server.strikes[sender] = 1
            #client_msg = await message.reply('<@' + str(message.guild.owner_id) + 'Toxic Behaviour Detected.')
            # await client_msg.add_reaction('\u2705')
            # await client_msg.add_reaction('\u274c')
            # print(dir(message))


    await client.process_commands(message)


@client.event
async def on_reaction_add(reaction, user):
    if user.id == user.guild.owner_id:
        if str(reaction.emoji) == "\u2705":
            print('stay')
        if str(reaction.emoji) == "\u274c":
            print('delete')

client.run(token)
