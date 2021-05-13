class PlayerInfo:
    def __init__(self, nome: str, placar: int):
        self.__nome = nome
        self.__placar = placar

    @property
    def placar(self):
        return self.__placar
    
    @placar.setter
    def placar(self, placar):
        self.__placar= placar

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome
        
    def __str__(self):
        return f'Nome: {self.__nome}, Score: {self.__placar}'



        