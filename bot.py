import pickle
import discord
from discord.ext import commands

loaded_model = pickle.load(open('xgb_model.sav', 'rb'))
loaded_vectorizer = pickle.load(open('vectorizer.sav', 'rb'))

client = commands.Bot(command_prefix='.')
@client.event
async  def on_ready():
    print('bot is ready')

@client.event
async def on_message(message):
    msg = [message.content]
    vectorized = loaded_vectorizer.transform(msg)
    prediction = loaded_model.predict(vectorized)
    if prediction == [1]:
        print('toxic')

client.run('token')
