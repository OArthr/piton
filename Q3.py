num = []

i = 0
while True:
    i = int(input("Digite um numero(-1 para terminar): "))
    if i < 0:
        break
    num.append(i)

print("\nEntrada: ", num)

num2 = []
soma = 0

for n in num:
    if n > 10 and n%2 == 0:
        soma += n
        num2.append(n)

print("Saída: ", num2,
      "\nSoma: ", soma)