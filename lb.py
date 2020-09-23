class Leaderboard:
    def __init__(self, id):
        self.id = id
        self.runners = []
        self.game = ''
        self.loaded = False

    async def load():
        self.loaded = True
        pass # TODO
