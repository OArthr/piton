import random
class player:
    def __init__(self,saude,alegria,fome,energia,dinheiro):
        self.saude = saude
        self.alegria = alegria
        self.fome = fome
        self.energia = energia
        self.dinheiro = dinheiro
        self.maxSaude = 100
        self.maxAlegria = 100
        self.maxFome = 100
        self.maxEnergia = 100
    
    def comer(self,dif):
        self.fome -= self.fome//2 + 2
        self.energia += (self.maxEnergia-self.energia)/4
        self.alegria += (self.maxAlegria-self.alegria)/8
        self.dinheiro -= dif + 1
        self.saude += (self.maxSaude-self.saude)/4
        
    def dormir(self,dif):
        self.fome += 1
        self.energia += (self.maxEnergia-self.energia)/2
        self.alegria += (self.maxAlegria-self.alegria)/8
        self.saude += (self.maxSaude-self.saude)/4
        
    def jogar(self,dif):
        self.alegria += (self.maxAlegria-self.alegria)/2
        self.energia += (self.maxEnergia-self.energia)/8
        self.fome += 1
        self.dinheiro -= dif
        
    def trabalhar(self,dif):
        self.fome += 2
        self.energia -= self.energia/4 + dif
        self.alegria -= self.alegria/4 + dif
        self.saude -= self.saude/4 + dif
        self.dinheiro += 10

dif = int(input('Escolha uma dificuldade:(<0)\n'))
dia = 0
pl = player(100/dif,100/dif,100-100/dif,100/dif,100/dif)
while pl.saude>0 and pl.alegria>0 and pl.fome<100 and pl.energia>0 and pl.dinheiro>0:
    dif = random.randint(1,10+dia)
    print(f'Saude: {pl.saude}%| Alegria: {pl.alegria}%| Fome: {pl.fome}%| Energia: {pl.energia}%| Dinheiro: R$ {pl.dinheiro}\nDificuldade do dia: {dif}\n')
    esc = int(input('Escolha uma ação:\n1-comer\n2-dormir\n3-jogar\n4-trabalhar\n'))
    match esc:
        case 1:
            pl.comer(dif)
        case 2:
            pl.dormir(dif)
        case 3:
            pl.jogar(dif)
        case 4:
            pl.trabalhar(dif)
    dia += 1
    
