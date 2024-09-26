import random

i, soma, qtd, media, maior = 0, 0, 0, 0, 0

while soma <= 50:
    i = random.randrange(1, 11)
    soma += i
    maior = i if i > maior else maior
    qtd += 1
    print(i)

media = soma/qtd

print("Soma final: ",soma,
      "\nN° de números: ",qtd,
      "\nMédia: ",media,
      "\nMaior número: ",maior)
