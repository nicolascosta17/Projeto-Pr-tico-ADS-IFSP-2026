arq = "artistas.txt"

def informacoesArtista(artista): # Nicolas
    cpf = input("Digite o CPF do Artista:  ")
    artista.append(cpf)

    nome = input("Digite o Nome do Artista: ")
    artista.append(nome)

    telefone = input("Digite o Telefone do Artista: ")
    artista.append(telefone)

    dataNascimento = input("Digite a data de nascimento do Artista (26/12/2007): ")
    artista.append(dataNascimento)

    nacionalidade = input("Digite a nacionalidade do Artista: ")
    artista.append(nacionalidade)

    estiloPrincipal = input("Digite o estilo principal do Artista (Classico, Renascimento e etc): ")
    artista.append(estiloPrincipal)

    redeSocial = input("Digite a o @ do Artista nas redes sociais (@artista - Instagram): ")
    artista.append(redeSocial)

    with open(arq, "a", encoding="utf-8") as arquivo:
        arquivo.write(";".join(artista) + "\n")

    return artista

def artistas(lista): # Nicolas
    pergunta = input("Quer adicionar um artista? (1-sim, 2-não): ")
    if pergunta == "1":
        while True:
            print("=============ADICIONAR O ARTISTA===========?")
            informacoesArtista(lista)

        if lista:
            for i in range(len(lista)):
                print(lista[i], end='; ')
                
        else:
            print("Lista vazia!")

    elif pergunta == "2":
        print("Lista vazia!")
        break
        
lista = []
artistas(lista)

