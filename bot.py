import discord
import json
from lb import Leaderboard

class MyClient(discord.Client):

    def __init__(self, lbs, channel_name):
        super().__init__()
        self.lbs = [Leaderboard(id) for id in lbs]
        self.channel = None
        self.channel_name = channel_name
        self.reload_lbs()


    async def reload_lbs(self):
        for lb in self.lbs:
            await lb.load()

            
    async def on_ready(self):
        print('Logged in as %s!' % self.user)
        if self.channel is None:
            all_channels = [c for c in self.get_all_channels() if c.name == self.channel_name and c is discord.TextChannel]
            if len(all_channels) > 0: # TODO multiple server support...
                self.channel = all_channels[0]
        

    async def on_member_update(self, before, after):
        print('on_member_update called')
        if len(after.activities) == 0:
            return
        activity = after.activities[0]
        if activity and activity is discord.Streaming:
            streamer = activity.url[activity.url.rfind('/')+1:]
            playing = activity.game
            print('%s is playing %s' % (streamer, playing))
            is_runner, game_whitelisted = False
            for lb in self.lbs: # TODO better data structure to avoid this loop...
                if lb.game == playing:
                    game_whitelisted = True
                elif streamer in self.runners:
                    is_runner = True
            if is_runner and game_whitelisted and self.channel:
                await self.channel.send('Runner %s is playing %s' % (streamer, playing))
                    

with open('config.json', 'r') as config_f:
    config = json.loads(config_f.read())



client = MyClient(config['leaderboards'], config['announce_channel'])
client.run(config['discord_token'])
