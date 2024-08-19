import os

# text_start = """
# 0: Soma 
# 1: Subtração 
# 2: Multiplicação 
# 3: Divisão 
# 4: Exponenciação 
# 5: Sair

# """

operacacoes = {
    "0": {
        "title": "0: Soma",
        "text": ">>> + escolhido", 
        "res": lambda x, y: f"{x} + {y} = {x + y}"
    },
    "1": {
        "title":"1: Subtração",
        "text": ">>> - escolhido", 
        "res": lambda x, y: f"{x} - {y} = {x - y}"
    },
}



while True:
    for operacao in operacacoes.values():
        print(operacao.get("title"))
    opcao_operacao = input("\n\nEscolha a operação que deseja realizar: ")

    if opcao_operacao == "5":
        break

    operacao = operacacoes.get(opcao_operacao)
    print(operacao.get("text"))

    numero_1 = int(input("Qual o primeiro valor? "))
    numero_2 = int(input("Qual o segundo valor? "))
    
    res = operacao.get("res")(numero_1, numero_2)
    

    print(res)
