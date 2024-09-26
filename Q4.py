produtos = ['maçã','banana','abacaxi','laranja']
preços = [3.0,2.5,5.0,4.0]

prod = ''
qtd = 0
carrinho = []
naoDisp = 0
print("Produtos: ",produtos,"\nPreços: ",preços)

while True:
    prod = input("Digite o nome de um produto('fim' para terminar): ")
    if prod == "fim":
        break
    while prod not in produtos:
        print("Produto não disponível: ", prod)
        naoDisp += 1
        prod = input("Digite o nome de um produto: ")

    print("Digite a quantidade de",prod,"para comprar: ",end='')
    qtd = int(input())
    while qtd < 0:
        print("Quantidade inválida!\n"
              "Digite a quantidade de", prod, "para comprar: ", end='')
        qtd = int(input())

    carrinho.append([prod,qtd])

print("\nLista de compras: ",carrinho)
if naoDisp > 0:
    print(naoDisp,"Produto não disponível.\n" if naoDisp == 1 else "Produtos não disponíveis.\n")

total = 0
for i in range(len(carrinho)):
    prodPreço = preços[produtos.index(carrinho[i][0])]
    totalPreço = carrinho[i][1] * prodPreço
    print(carrinho[i][0],":",carrinho[i][1],"*",prodPreço,"=", totalPreço,end='')
    if carrinho[i][1] > 5:
        totalPreço -= totalPreço / 10
        print("- 10% =", totalPreço, end='')
    total += totalPreço
    print('')

print("Total: ", total)