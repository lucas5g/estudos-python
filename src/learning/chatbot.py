import openai

client = openai.Client()


def geracao_texto(mensagens):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model="gpt-3.5-turbo-0125",
        temperature=0,
        max_tokens=1000,
        stream=True,
    )

    print("Assistant: ", end="")
    texto_completo = ""
    for stream in resposta:
        texto = stream.choices[0].delta.content
        if texto:
            print(texto, end="")
            texto_completo += texto
    print()
    mensagens.append({"role": "assistant", "content": texto_completo})

    return mensagens


if __name__ == "__main__":
    mensagens = []

    while True:
        input_usuario = input("User: ")
        if input_usuario == "q":
            break

        mensagens.append({"role": "user", "content": input_usuario})
        mensagens = geracao_texto(mensagens)
