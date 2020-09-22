import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as %s!' % self.user)

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))


client = MyClient()
client.run('NzU3NzcwMjg4NDk3ODE5Nzg4.X2lOkw.pD8rUrSXlENXMX54pL_sTbP2D_U')
