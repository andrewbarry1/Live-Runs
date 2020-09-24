import aiohttp

async def load_runner_name(id):
    async with aiohttp.ClientSession() as session:
        user_url = 'https://www.speedrun.com/api/v1/users/%s' % id
        async with session.get(user_url) as r:
            if r.status == 200:
                j = await r.json()
                return j['data']['names']['international']
            else:
                return ''


class Leaderboard:
    def __init__(self, id):
        self.id = id
        self.runners = []
        self.game = ''
        self.loaded = False

    async def load():
        async with aiohttp.ClientSession() as session:
            runs_url = 'https://www.speedrun.com/api/v1/runs?game=%s&status=verified' % self.id
            async with session.get(runs_url) as r:
                if r.status == 200:
                    j = await r.json()
                    runner_ids = [player['id'] for player in j['data'][0]['players']]
                    self.runners = map(load_runner_name, runner_ids)
                    self.loaded = True
                    
