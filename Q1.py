i = 0
while(i!=-1):
    i = int(input("Digite um numero inteiro(-1 para sair): "))
    if i%3==0 or i%5==0 or i%7==0:
        if i%3==0:
            print("Fizz",end='')
        if i%5==0:
            print("Buzz",end='')
        if i%7==0:
            print("Pop",end='')
    else:
        print(i)
    print('')
