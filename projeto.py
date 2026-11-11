import os
arq = "informacoes.txt"
ref_arq = open(arq, "w")

def informacoesArtista(): # Nicolas
    artista = []
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

def artistas(lista): # Nicolas
    condicao = True
    pergunta = input("Quer adicionar um artista? (1-sim, 2-não): ")
    if pergunta == "1":
        while condicao:
            print("=============ADICIONAR O ARTISTA===========?")
    elif pergunta == "2":
        condicao = False

artistas(informacoesArtista)