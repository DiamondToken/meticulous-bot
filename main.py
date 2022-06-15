import discord
import aiohttp
import json
import os
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('token')

numbers_api = "http://numbersapi.com/{}"


def contains_digit(message):
    for num in message.content.split():
        if num.isdigit():
            return True

    return False

def get_next_num(message):
    for num in message.content.split():
        if num.isdigit():
            yield num


def form(message):
    ints = [s for s in message.content.split() if s.isdigit()]
    if len(ints) == 1:
        return ints[0]
    else:
        return ",".join(ints)


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        print(dir(self))
        print(self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if contains_digit(message):
            async with aiohttp.ClientSession() as session:
                async with session.get(numbers_api.format(form(message))) as r:
                    if r.status == 200:
                        out = await r.text()

                        if out.startswith("{"):
                            dic = json.loads(out)
                            dic = "\n".join(list(dic.values()))
                        else:
                            dic = out

                        await message.channel.send(dic)

        # if message.content == 'ping {}'.format(self.user):
        #     await message.channel.send('privet {}'.format(self.user))


client = MyClient()
client.run(token)
