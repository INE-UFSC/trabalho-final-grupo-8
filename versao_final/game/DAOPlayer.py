from game.DAO import DAO
from game.PlayerInfo import PlayerInfo


class DAOPlayer(DAO):
    def add(self, player: PlayerInfo):
        self.cache[player.nome] = player.placar

    def get(self, key):
        return self.cache.get(key)

    def remove(self, key):
        del self.cache[key]
        
