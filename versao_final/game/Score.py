from game.DAOPlayer import DAOPlayer
from game.DAOPlayer import PlayerInfo


class Score:
    def __init__(self):
        self.__info = DAOPlayer('score.json')
    
    def salvar(self):
        self.__info.dump()
    
    def adiciona_score(self, nome, placar):
        if self.__info.get(nome) is None:
            self.__info.add(PlayerInfo(nome, placar))
        elif self.__info.get(nome) < placar:
            self.__info.remove(nome)
            self.__info.add(PlayerInfo(nome, placar))
    
    def listar_placar(self):
        listas = []
        [(listas.append((nome, placar))) for nome, placar in self.__info.get_all().items()]
        print(listas)
        score = []
        for i in range(1, len(listas)):
    
            key = listas[i]
    
            # Move elements of arr[0..i-1], that are
            # greater than key, to one position ahead
            # of their current position
            j = i-1
            print(key[1] , listas[j][1])
            while j >=0 and key[1] < listas[j][1] :
                    listas[j+1][1] = listas[j][1]
                    j -= 1
            listas[j+1] = key
        return listas

