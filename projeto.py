import os


# ===== MENU E SUBMENUS - William Rosales =====

def main():  # William Rosales
    arqArtistas = "artistas.txt"
    arqObras = "obras.txt"
    arqColaboracoes = "colaboracoes.txt"

    artistas = carregarArtistas(arqArtistas)
    obras = carregarObras(arqObras)
    colaboracoes = carregarColaboracoes(arqColaboracoes)

    while True:
        print()
        print("===== MENU PRINCIPAL =====")
        print("1. Submenu de Artista")
        print("2. Submenu de Obra")
        print("3. Submenu de Colaboração")
        print("4. Submenu Relatórios")
        print("5. Sair")
        opcao = input("Opção: ")

        if opcao == "1":
            menuArtistas(artistas, arqArtistas)
        elif opcao == "2":
            menuObras(obras, arqObras)
        elif opcao == "3":
            menuColaboracoes(colaboracoes, artistas, obras, arqColaboracoes)
        elif opcao == "4":
            menuRelatorios(artistas, obras, colaboracoes)
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


def mostrarSubmenu(nome):  # William Rosales
    print()
    print("-----", nome, "-----")
    print("1. Listar todos")
    print("2. Listar um")
    print("3. Incluir")
    print("4. Alterar")
    print("5. Excluir")
    print("6. Voltar")


def menuArtistas(artistas, nomeArquivo):  # William Rosales
    while True:
        mostrarSubmenu("ARTISTAS")
        opcao = input("Opção: ")
        if opcao == "1":
            listarArtistas(artistas)
        elif opcao == "2":
            listarUmArtista(artistas)
        elif opcao == "3":
            incluirArtista(artistas, nomeArquivo)
        elif opcao == "4":
            alterarArtista(artistas, nomeArquivo)
        elif opcao == "5":
            excluirArtista(artistas, nomeArquivo)
        elif opcao == "6":
            break
        else:
            print("Opção inválida!")


def menuObras(obras, nomeArquivo):  # William Rosales
    while True:
        mostrarSubmenu("OBRAS")
        opcao = input("Opção: ")
        if opcao == "1":
            listarObras(obras)
        elif opcao == "2":
            listarUmaObra(obras)
        elif opcao == "3":
            incluirObra(obras, nomeArquivo)
        elif opcao == "4":
            alterarObra(obras, nomeArquivo)
        elif opcao == "5":
            excluirObra(obras, nomeArquivo)
        elif opcao == "6":
            break
        else:
            print("Opção inválida!")


def menuColaboracoes(colaboracoes, artistas, obras, nomeArquivo):  # William Rosales
    while True:
        mostrarSubmenu("COLABORAÇÕES")
        opcao = input("Opção: ")
        if opcao == "1":
            listarColaboracoes(colaboracoes)
        elif opcao == "2":
            listarUmaColaboracao(colaboracoes)
        elif opcao == "3":
            incluirColaboracao(colaboracoes, artistas, obras, nomeArquivo)
        elif opcao == "4":
            alterarColaboracao(colaboracoes, nomeArquivo)
        elif opcao == "5":
            excluirColaboracao(colaboracoes, nomeArquivo)
        elif opcao == "6":
            break
        else:
            print("Opção inválida!")


def menuRelatorios(artistas, obras, colaboracoes):  # William Rosales
    while True:
        print()
        print("----- RELATÓRIOS -----")
        print("1. Obras de um artista")
        print("2. Obras de um tipo")
        print("3. Colaborações entre duas datas")
        print("4. Voltar")
        opcao = input("Opção: ")
        if opcao == "1":
            relatorioObrasArtista(artistas, obras, colaboracoes)
        elif opcao == "2":
            relatorioObrasTipo(artistas, obras, colaboracoes)
        elif opcao == "3":
            relatorioColaboracoesPeriodo(artistas, obras, colaboracoes)
        elif opcao == "4":
            break
        else:
            print("Opção inválida!")


# ===== ARTISTAS, OBRAS, COLABORAÇÕES E RELATÓRIOS - Nicolas =====

def dataValida(data):  # Nicolas
    if len(data) != 10 or data[2] != "/" or data[5] != "/":
        return False
    partes = data.split("/")
    if not partes[0].isdigit() or not partes[1].isdigit() or not partes[2].isdigit():
        return False
    dia = int(partes[0])
    mes = int(partes[1])
    if dia < 1 or dia > 31 or mes < 1 or mes > 12:
        return False
    return True


def lerData(mensagem):  # Nicolas
    data = input(mensagem)
    while not dataValida(data):
        print("Data inválida! Use dd/mm/aaaa")
        data = input(mensagem)
    return data


def dataParaNumero(data):  # Nicolas
    return int(data[6:10] + data[3:5] + data[0:2])


def lerLista(nomeItem):  # Nicolas
    lista = []
    print("Digite os", nomeItem, "(aperte Enter vazio para parar):")
    item = input("> ")
    while item != "":
        lista.append(item)
        item = input("> ")
    return lista


def lerTipo():  # Nicolas
    tipos = ["3D", "Ilustração", "NFT", "Animação"]
    tipo = input("Tipo (3D, Ilustração, NFT, Animação): ")
    while tipo not in tipos:
        print("Tipo inválido!")
        tipo = input("Tipo (3D, Ilustração, NFT, Animação): ")
    return tipo


def carregarArtistas(nomeArquivo):  # Nicolas
    artistas = []
    if os.path.exists(nomeArquivo):
        arquivo = open(nomeArquivo, "r", encoding="utf-8")
        for linha in arquivo:
            dados = linha.strip().split(";")
            if len(dados) == 7:
                telefones = dados[2].split(",")
                redes = dados[6].split(",")
                artistas.append([dados[0], dados[1], telefones, dados[3], dados[4], dados[5], redes])
        arquivo.close()
    return artistas


def salvarArtistas(artistas, nomeArquivo):  # Nicolas
    arquivo = open(nomeArquivo, "w", encoding="utf-8")
    for a in artistas:
        telefones = ",".join(a[2])
        redes = ",".join(a[6])
        arquivo.write(a[0] + ";" + a[1] + ";" + telefones + ";" + a[3] + ";" + a[4] + ";" + a[5] + ";" + redes + "\n")
    arquivo.close()


def carregarObras(nomeArquivo):  # Nicolas
    obras = []
    if os.path.exists(nomeArquivo):
        arquivo = open(nomeArquivo, "r", encoding="utf-8")
        for linha in arquivo:
            dados = linha.strip().split(";")
            if len(dados) == 6:
                obras.append(dados)
        arquivo.close()
    return obras


def salvarObras(obras, nomeArquivo):  # Nicolas
    arquivo = open(nomeArquivo, "w", encoding="utf-8")
    for o in obras:
        arquivo.write(";".join(o) + "\n")
    arquivo.close()


def carregarColaboracoes(nomeArquivo):  # Nicolas
    colaboracoes = []
    if os.path.exists(nomeArquivo):
        arquivo = open(nomeArquivo, "r", encoding="utf-8")
        for linha in arquivo:
            dados = linha.strip().split(";")
            if len(dados) == 6:
                colaboracoes.append(dados)
        arquivo.close()
    return colaboracoes


def salvarColaboracoes(colaboracoes, nomeArquivo):  # Nicolas
    arquivo = open(nomeArquivo, "w", encoding="utf-8")
    for c in colaboracoes:
        arquivo.write(";".join(c) + "\n")
    arquivo.close()


def buscarArtista(artistas, cpf):  # Nicolas
    for i in range(len(artistas)):
        if artistas[i][0] == cpf:
            return i
    return -1


def buscarObra(obras, codigo):  # Nicolas
    for i in range(len(obras)):
        if obras[i][0] == codigo:
            return i
    return -1


def buscarColaboracao(colaboracoes, cpf, codigo):  # Nicolas
    for i in range(len(colaboracoes)):
        if colaboracoes[i][0] == cpf and colaboracoes[i][1] == codigo:
            return i
    return -1


def mostrarArtista(a):  # Nicolas
    print("CPF:", a[0])
    print("Nome:", a[1])
    print("Telefones:", ", ".join(a[2]))
    print("Data de nascimento:", a[3])
    print("Nacionalidade:", a[4])
    print("Estilo principal:", a[5])
    print("Redes sociais:", ", ".join(a[6]))


def listarArtistas(artistas):  # Nicolas
    if len(artistas) == 0:
        print("Nenhum artista cadastrado.")
    for a in artistas:
        print("--------------------")
        mostrarArtista(a)


def listarUmArtista(artistas):  # Nicolas
    cpf = input("CPF do artista: ")
    pos = buscarArtista(artistas, cpf)
    if pos == -1:
        print("Artista não encontrado!")
    else:
        mostrarArtista(artistas[pos])


def incluirArtista(artistas, nomeArquivo):  # Nicolas
    cpf = input("CPF: ")
    if buscarArtista(artistas, cpf) != -1:
        print("Já existe um artista com esse CPF!")
        return
    nome = input("Nome: ")
    telefones = lerLista("telefones")
    dataNascimento = lerData("Data de nascimento (dd/mm/aaaa): ")
    nacionalidade = input("Nacionalidade: ")
    estilo = input("Estilo principal: ")
    redes = lerLista("redes sociais")
    artistas.append([cpf, nome, telefones, dataNascimento, nacionalidade, estilo, redes])
    salvarArtistas(artistas, nomeArquivo)
    print("Artista cadastrado!")


def alterarArtista(artistas, nomeArquivo):  # Nicolas
    cpf = input("CPF do artista: ")
    pos = buscarArtista(artistas, cpf)
    if pos == -1:
        print("Artista não encontrado!")
        return
    a = artistas[pos]
    mostrarArtista(a)
    print("Digite os novos dados (Enter para manter):")
    novo = input("Nome: ")
    if novo != "":
        a[1] = novo
    if input("Alterar telefones? (s/n): ") == "s":
        a[2] = lerLista("telefones")
    novo = input("Data de nascimento: ")
    if novo != "" and dataValida(novo):
        a[3] = novo
    novo = input("Nacionalidade: ")
    if novo != "":
        a[4] = novo
    novo = input("Estilo principal: ")
    if novo != "":
        a[5] = novo
    if input("Alterar redes sociais? (s/n): ") == "s":
        a[6] = lerLista("redes sociais")
    salvarArtistas(artistas, nomeArquivo)
    print("Artista alterado!")


def excluirArtista(artistas, nomeArquivo):  # Nicolas
    cpf = input("CPF do artista: ")
    pos = buscarArtista(artistas, cpf)
    if pos == -1:
        print("Artista não encontrado!")
        return
    mostrarArtista(artistas[pos])
    resposta = input("Confirma a exclusão? (s/n): ")
    if resposta == "s":
        del artistas[pos]
        salvarArtistas(artistas, nomeArquivo)
        print("Artista excluído!")
    else:
        print("Exclusão cancelada.")


def mostrarObra(o):  # Nicolas
    print("Código:", o[0])
    print("Título:", o[1])
    print("Ano de criação:", o[2])
    print("Tipo:", o[3])
    print("Descrição:", o[4])
    print("Valor estimado: R$", o[5])


def listarObras(obras):  # Nicolas
    if len(obras) == 0:
        print("Nenhuma obra cadastrada.")
    for o in obras:
        print("--------------------")
        mostrarObra(o)


def listarUmaObra(obras):  # Nicolas
    codigo = input("Código da obra: ")
    pos = buscarObra(obras, codigo)
    if pos == -1:
        print("Obra não encontrada!")
    else:
        mostrarObra(obras[pos])


def incluirObra(obras, nomeArquivo):  # Nicolas
    codigo = input("Código: ")
    if buscarObra(obras, codigo) != -1:
        print("Já existe uma obra com esse código!")
        return
    titulo = input("Título: ")
    ano = input("Ano de criação: ")
    while not ano.isdigit():
        ano = input("Digite um ano válido: ")
    tipo = lerTipo()
    descricao = input("Descrição: ")
    valor = input("Valor estimado: ")
    obras.append([codigo, titulo, ano, tipo, descricao, valor])
    salvarObras(obras, nomeArquivo)
    print("Obra cadastrada!")


def alterarObra(obras, nomeArquivo):  # Nicolas
    codigo = input("Código da obra: ")
    pos = buscarObra(obras, codigo)
    if pos == -1:
        print("Obra não encontrada!")
        return
    o = obras[pos]
    mostrarObra(o)
    print("Digite os novos dados (Enter para manter):")
    novo = input("Título: ")
    if novo != "":
        o[1] = novo
    novo = input("Ano de criação: ")
    if novo.isdigit():
        o[2] = novo
    if input("Alterar tipo? (s/n): ") == "s":
        o[3] = lerTipo()
    novo = input("Descrição: ")
    if novo != "":
        o[4] = novo
    novo = input("Valor estimado: ")
    if novo != "":
        o[5] = novo
    salvarObras(obras, nomeArquivo)
    print("Obra alterada!")


def excluirObra(obras, nomeArquivo):  # Nicolas
    codigo = input("Código da obra: ")
    pos = buscarObra(obras, codigo)
    if pos == -1:
        print("Obra não encontrada!")
        return
    mostrarObra(obras[pos])
    resposta = input("Confirma a exclusão? (s/n): ")
    if resposta == "s":
        del obras[pos]
        salvarObras(obras, nomeArquivo)
        print("Obra excluída!")
    else:
        print("Exclusão cancelada.")


def mostrarColaboracao(c):  # Nicolas
    print("CPF do artista:", c[0])
    print("Código da obra:", c[1])
    print("Papel:", c[2])
    print("Percentual de contribuição:", c[3] + "%")
    print("Data de entrada:", c[4])
    print("Data de saída:", c[5])


def listarColaboracoes(colaboracoes):  # Nicolas
    if len(colaboracoes) == 0:
        print("Nenhuma colaboração cadastrada.")
    for c in colaboracoes:
        print("--------------------")
        mostrarColaboracao(c)


def listarUmaColaboracao(colaboracoes):  # Nicolas
    cpf = input("CPF do artista: ")
    codigo = input("Código da obra: ")
    pos = buscarColaboracao(colaboracoes, cpf, codigo)
    if pos == -1:
        print("Colaboração não encontrada!")
    else:
        mostrarColaboracao(colaboracoes[pos])


def incluirColaboracao(colaboracoes, artistas, obras, nomeArquivo):  # Nicolas
    cpf = input("CPF do artista: ")
    if buscarArtista(artistas, cpf) == -1:
        print("Artista não cadastrado!")
        return
    codigo = input("Código da obra: ")
    if buscarObra(obras, codigo) == -1:
        print("Obra não cadastrada!")
        return
    if buscarColaboracao(colaboracoes, cpf, codigo) != -1:
        print("Essa colaboração já existe!")
        return
    papel = input("Papel (Modelagem, Textura, Roteiro, Animação...): ")
    percentual = input("Percentual de contribuição: ")
    dataEntrada = lerData("Data de entrada (dd/mm/aaaa): ")
    dataSaida = lerData("Data de saída (dd/mm/aaaa): ")
    colaboracoes.append([cpf, codigo, papel, percentual, dataEntrada, dataSaida])
    salvarColaboracoes(colaboracoes, nomeArquivo)
    print("Colaboração cadastrada!")


def alterarColaboracao(colaboracoes, nomeArquivo):  # Nicolas
    cpf = input("CPF do artista: ")
    codigo = input("Código da obra: ")
    pos = buscarColaboracao(colaboracoes, cpf, codigo)
    if pos == -1:
        print("Colaboração não encontrada!")
        return
    c = colaboracoes[pos]
    mostrarColaboracao(c)
    print("Digite os novos dados (Enter para manter):")
    novo = input("Papel: ")
    if novo != "":
        c[2] = novo
    novo = input("Percentual de contribuição: ")
    if novo != "":
        c[3] = novo
    novo = input("Data de entrada: ")
    if novo != "" and dataValida(novo):
        c[4] = novo
    novo = input("Data de saída: ")
    if novo != "" and dataValida(novo):
        c[5] = novo
    salvarColaboracoes(colaboracoes, nomeArquivo)
    print("Colaboração alterada!")


def excluirColaboracao(colaboracoes, nomeArquivo):  # Nicolas
    cpf = input("CPF do artista: ")
    codigo = input("Código da obra: ")
    pos = buscarColaboracao(colaboracoes, cpf, codigo)
    if pos == -1:
        print("Colaboração não encontrada!")
        return
    mostrarColaboracao(colaboracoes[pos])
    resposta = input("Confirma a exclusão? (s/n): ")
    if resposta == "s":
        del colaboracoes[pos]
        salvarColaboracoes(colaboracoes, nomeArquivo)
        print("Colaboração excluída!")
    else:
        print("Exclusão cancelada.")


def salvarRelatorio(linhas, nomeArquivo):  # Nicolas
    arquivo = open(nomeArquivo, "w", encoding="utf-8")
    for linha in linhas:
        print(linha)
        arquivo.write(linha + "\n")
    arquivo.close()
    print("Relatório salvo em", nomeArquivo)


def relatorioObrasArtista(artistas, obras, colaboracoes):  # Nicolas
    cpf = input("CPF do artista: ")
    pos = buscarArtista(artistas, cpf)
    if pos == -1:
        print("Artista não encontrado!")
        return
    linhas = []
    linhas.append("Artista: " + artistas[pos][1])
    linhas.append("Redes sociais: " + ", ".join(artistas[pos][6]))
    linhas.append("Obras:")
    achou = False
    for c in colaboracoes:
        if c[0] == cpf:
            posObra = buscarObra(obras, c[1])
            if posObra != -1:
                o = obras[posObra]
                linhas.append("- " + o[0] + " | " + o[1] + " | " + o[2] + " | " + o[3] + " | " + o[4] + " | R$ " + o[5])
                achou = True
    if not achou:
        linhas.append("Nenhuma obra encontrada.")
    salvarRelatorio(linhas, "relatorio_a.txt")


def relatorioObrasTipo(artistas, obras, colaboracoes):  # Nicolas
    tipo = lerTipo()
    linhas = []
    linhas.append("Obras do tipo " + tipo + ":")
    achou = False
    for o in obras:
        if o[3] == tipo:
            nomes = []
            for c in colaboracoes:
                if c[1] == o[0]:
                    posArtista = buscarArtista(artistas, c[0])
                    if posArtista != -1:
                        nomes.append(artistas[posArtista][1])
            linhas.append("- " + o[0] + " | " + o[1] + " | " + o[2] + " | " + o[4] + " | R$ " + o[5])
            linhas.append("  Artista(s): " + ", ".join(nomes))
            achou = True
    if not achou:
        linhas.append("Nenhuma obra encontrada.")
    salvarRelatorio(linhas, "relatorio_b.txt")


def relatorioColaboracoesPeriodo(artistas, obras, colaboracoes):  # Nicolas
    dataX = lerData("Data inicial (dd/mm/aaaa): ")
    dataY = lerData("Data final (dd/mm/aaaa): ")
    inicio = dataParaNumero(dataX)
    fim = dataParaNumero(dataY)
    linhas = []
    linhas.append("Colaborações entre " + dataX + " e " + dataY + ":")
    achou = False
    for c in colaboracoes:
        entrada = dataParaNumero(c[4])
        if entrada >= inicio and entrada <= fim:
            nomeArtista = ""
            posArtista = buscarArtista(artistas, c[0])
            if posArtista != -1:
                nomeArtista = artistas[posArtista][1]
            tituloObra = ""
            posObra = buscarObra(obras, c[1])
            if posObra != -1:
                tituloObra = obras[posObra][1]
            linhas.append("- " + nomeArtista + " | " + tituloObra + " | " + c[2] + " | " + c[3] + "%")
            achou = True
    if not achou:
        linhas.append("Nenhuma colaboração encontrada.")
    salvarRelatorio(linhas, "relatorio_c.txt")


main()
