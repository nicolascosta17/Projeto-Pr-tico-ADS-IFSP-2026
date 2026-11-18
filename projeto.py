'''
Projeto Prático APR1 - Tema 15
Sistema de curadoria de artes digital e colaborações

Estruturas de dados (listas de listas):
    artista     = [cpf, nome, [telefones], data_nascimento, nacionalidade,
                   estilo_principal, [redes_sociais]]
    obra        = [codigo, titulo, ano_criacao, tipo, descricao, valor_estimado]
    colaboracao = [cpf_artista, codigo_obra, papel, percentual,
                   data_entrada, data_saida]

Arquivos texto (um registro por linha, campos separados por ";" e
itens de atributos no plural separados por ","):
    artistas.txt, obras.txt, colaboracoes.txt
Relatórios gerados:
    relatorio_obras_artista.txt, relatorio_obras_tipo.txt,
    relatorio_colaboracoes_periodo.txt
'''

import os


# ===================== FUNÇÃO PRINCIPAL =====================

def main():
    '''
    Responsável por carregar os dados dos arquivos e exibir o menu principal.
    '''
    arquivo_artistas = "artistas.txt"
    arquivo_obras = "obras.txt"
    arquivo_colaboracoes = "colaboracoes.txt"

    artistas = carregar_artistas(arquivo_artistas)
    obras = carregar_obras(arquivo_obras)
    colaboracoes = carregar_colaboracoes(arquivo_colaboracoes)

    opcao = ""
    while opcao != "5":
        print("\n========== CURADORIA DE ARTE DIGITAL ==========")
        print("1. Submenu de Artista")
        print("2. Submenu de Obra")
        print("3. Submenu de Colaboração")
        print("4. Submenu Relatórios")
        print("5. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            submenu_artistas(artistas, colaboracoes, arquivo_artistas)
        elif opcao == "2":
            submenu_obras(obras, colaboracoes, arquivo_obras)
        elif opcao == "3":
            submenu_colaboracoes(colaboracoes, artistas, obras, arquivo_colaboracoes)
        elif opcao == "4":
            submenu_relatorios(artistas, obras, colaboracoes)
        elif opcao == "5":
            print("Programa encerrado. Até logo!")
        else:
            print("Opção inválida!")


# ===================== FUNÇÕES DE VALIDAÇÃO E LEITURA =====================

def existe_arquivo(nome):
    '''
    Retorna True se o arquivo existir e False caso contrário.
    '''
    if os.path.exists(nome):
        return True
    else:
        return False


def real_valido(texto):
    '''
    Verifica se a string pode ser convertida para número real
    (aceita vírgula ou ponto como separador decimal).
    '''
    texto = texto.replace(",", ".")
    if texto == "" or texto.count(".") > 1 or texto == ".":
        return False
    sem_ponto = texto.replace(".", "")
    return sem_ponto.isdigit()


def ano_bissexto(ano):
    '''
    Retorna True se o ano for bissexto.
    '''
    return (ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0


def dias_no_mes(mes, ano):
    '''
    Retorna a quantidade de dias de um mês em um determinado ano.
    '''
    if mes == 2:
        if ano_bissexto(ano):
            return 29
        return 28
    if mes == 4 or mes == 6 or mes == 9 or mes == 11:
        return 30
    return 31


def data_valida(data):
    '''
    Verifica se a data está no formato dd/mm/aaaa e se é uma data existente.
    '''
    if len(data) != 10 or data[2] != "/" or data[5] != "/":
        return False
    partes = data.split("/")
    if not (partes[0].isdigit() and partes[1].isdigit() and partes[2].isdigit()):
        return False
    dia = int(partes[0])
    mes = int(partes[1])
    ano = int(partes[2])
    if mes < 1 or mes > 12 or ano < 1:
        return False
    if dia < 1 or dia > dias_no_mes(mes, ano):
        return False
    return True


def data_para_numero(data):
    '''
    Converte a data dd/mm/aaaa no número aaaammdd, permitindo comparar datas.
    '''
    return int(data[6:10] + data[3:5] + data[0:2])


def limpar_cpf(cpf):
    '''
    Remove pontos, traços e espaços do CPF.
    '''
    return cpf.replace(".", "").replace("-", "").replace(" ", "")


def valor_valido(valor, tipo):
    '''
    Verifica se o valor digitado é válido de acordo com o tipo:
    texto, cpf, inteiro, real, percentual, data ou data_opcional.
    '''
    if tipo == "texto":
        return valor != "" and ";" not in valor
    elif tipo == "cpf":
        cpf = limpar_cpf(valor)
        return cpf.isdigit() and len(cpf) == 11
    elif tipo == "inteiro":
        return valor.isdigit()
    elif tipo == "real":
        return real_valido(valor)
    elif tipo == "percentual":
        if not real_valido(valor):
            return False
        numero = float(valor.replace(",", "."))
        return numero > 0 and numero <= 100
    elif tipo == "data":
        return data_valida(valor)
    elif tipo == "data_opcional":
        return valor == "" or data_valida(valor)
    return False


def mensagem_erro(tipo):
    '''
    Retorna a mensagem de erro adequada para cada tipo de valor.
    '''
    if tipo == "texto":
        return "Valor inválido! Não pode ser vazio nem conter ';'."
    elif tipo == "cpf":
        return "CPF inválido! Digite os 11 números do CPF."
    elif tipo == "inteiro":
        return "Valor inválido! Digite um número inteiro positivo."
    elif tipo == "real":
        return "Valor inválido! Digite um número (ex: 1500.50)."
    elif tipo == "percentual":
        return "Percentual inválido! Digite um número maior que 0 e até 100."
    else:
        return "Data inválida! Use o formato dd/mm/aaaa."


def converter_valor(valor, tipo):
    '''
    Converte a string digitada para o tipo correto.
    '''
    if tipo == "cpf":
        return limpar_cpf(valor)
    elif tipo == "inteiro":
        return int(valor)
    elif tipo == "real" or tipo == "percentual":
        return float(valor.replace(",", "."))
    return valor


def ler_valor(mensagem, tipo):
    '''
    Lê um valor do usuário até que ele seja válido e o retorna convertido.
    '''
    valor = input(mensagem).strip()
    while not valor_valido(valor, tipo):
        print(mensagem_erro(tipo))
        valor = input(mensagem).strip()
    return converter_valor(valor, tipo)


def ler_alteracao(rotulo, valor_atual, tipo):
    '''
    Lê o novo valor de um atributo. Se o usuário apertar Enter,
    o valor atual é mantido.
    '''
    mensagem = f"{rotulo} [{valor_atual}] (Enter mantém): "
    valor = input(mensagem).strip()
    while valor != "" and not valor_valido(valor, tipo):
        print(mensagem_erro(tipo))
        valor = input(mensagem).strip()
    if valor == "":
        return valor_atual
    return converter_valor(valor, tipo)


def ler_lista_itens(nome_item):
    '''
    Lê uma quantidade indefinida de itens (telefones, redes sociais...)
    e retorna uma lista com eles. Pelo menos um item deve ser informado.
    '''
    itens = []
    print(f"Digite os(as) {nome_item} um por vez (Enter vazio para terminar):")
    item = input(f"  {nome_item} {len(itens) + 1}: ").strip()
    while item != "" or len(itens) == 0:
        if item == "":
            print("  Informe pelo menos um item!")
        elif ";" in item or "," in item:
            print("  O item não pode conter ';' ou ','.")
        elif item in itens:
            print("  Item já informado!")
        else:
            itens.append(item)
        item = input(f"  {nome_item} {len(itens) + 1}: ").strip()
    return itens


def ler_tipo_obra():
    '''
    Mostra os tipos de obra disponíveis e retorna o tipo escolhido.
    '''
    tipos = ["3D", "Ilustração", "NFT", "Animação"]
    print("Tipos de obra:")
    for i in range(len(tipos)):
        print(f"  {i + 1}. {tipos[i]}")
    opcao = input("Escolha o tipo: ").strip()
    while not (opcao.isdigit() and int(opcao) >= 1 and int(opcao) <= len(tipos)):
        print("Opção inválida!")
        opcao = input("Escolha o tipo: ").strip()
    return tipos[int(opcao) - 1]


def confirmar(mensagem):
    '''
    Pede uma confirmação (s/n) ao usuário e retorna True se a resposta for sim.
    '''
    resposta = input(mensagem + " (s/n): ").strip().lower()
    while resposta != "s" and resposta != "n":
        resposta = input("Digite 's' para sim ou 'n' para não: ").strip().lower()
    return resposta == "s"


def juntar_itens(lista, separador):
    '''
    Junta os itens de uma lista em uma única string, usando o separador.
    '''
    texto = ""
    for i in range(len(lista)):
        if i > 0:
            texto = texto + separador
        texto = texto + str(lista[i])
    return texto


def separar_itens(texto):
    '''
    Separa uma string com itens separados por "," em uma lista.
    '''
    if texto == "":
        return []
    return texto.split(",")


# ===================== FUNÇÕES DE BUSCA =====================

def buscar_artista(artistas, cpf):
    '''
    Retorna a posição do artista com o CPF informado ou -1 se não existir.
    '''
    for i in range(len(artistas)):
        if artistas[i][0] == cpf:
            return i
    return -1


def buscar_obra(obras, codigo):
    '''
    Retorna a posição da obra com o código informado ou -1 se não existir.
    '''
    for i in range(len(obras)):
        if obras[i][0].upper() == codigo.upper():
            return i
    return -1


def buscar_colaboracao(colaboracoes, cpf, codigo):
    '''
    Retorna a posição da colaboração (CPF + código da obra) ou -1.
    '''
    for i in range(len(colaboracoes)):
        if colaboracoes[i][0] == cpf and colaboracoes[i][1].upper() == codigo.upper():
            return i
    return -1


def nome_do_artista(artistas, cpf):
    '''
    Retorna o nome do artista a partir do CPF.
    '''
    posicao = buscar_artista(artistas, cpf)
    if posicao == -1:
        return "(artista não encontrado)"
    return artistas[posicao][1]


def titulo_da_obra(obras, codigo):
    '''
    Retorna o título da obra a partir do código.
    '''
    posicao = buscar_obra(obras, codigo)
    if posicao == -1:
        return "(obra não encontrada)"
    return obras[posicao][1]


def possui_colaboracao(colaboracoes, valor, campo):
    '''
    Verifica se existe colaboração com o CPF (campo 0) ou código de obra
    (campo 1) informado. Usada para não excluir registros em uso.
    '''
    for colaboracao in colaboracoes:
        if colaboracao[campo].upper() == valor.upper():
            return True
    return False


# ===================== FUNÇÕES DE FORMATAÇÃO =====================

def formatar_artista(artista):
    '''
    Retorna uma string com todos os dados de um artista.
    '''
    texto = f"CPF: {artista[0]} | Nome: {artista[1]}\n"
    texto = texto + f"   Telefones: {juntar_itens(artista[2], ', ')}\n"
    texto = texto + f"   Nascimento: {artista[3]} | Nacionalidade: {artista[4]}"
    texto = texto + f" | Estilo principal: {artista[5]}\n"
    texto = texto + f"   Redes sociais: {juntar_itens(artista[6], ', ')}"
    return texto


def formatar_obra(obra):
    '''
    Retorna uma string com todos os dados de uma obra.
    '''
    texto = f"Código: {obra[0]} | Título: {obra[1]} | Ano: {obra[2]} | Tipo: {obra[3]}\n"
    texto = texto + f"   Descrição: {obra[4]}\n"
    texto = texto + f"   Valor estimado: R$ {obra[5]}"
    return texto


def formatar_colaboracao(colaboracao, artistas, obras):
    '''
    Retorna uma string com todos os dados de uma colaboração,
    incluindo o nome do artista e o título da obra.
    '''
    saida = colaboracao[5]
    if saida == "":
        saida = "Em andamento"
    texto = f"Artista: {colaboracao[0]} - {nome_do_artista(artistas, colaboracao[0])}\n"
    texto = texto + f"   Obra: {colaboracao[1]} - {titulo_da_obra(obras, colaboracao[1])}\n"
    texto = texto + f"   Papel: {colaboracao[2]} | Contribuição: {colaboracao[3]}%\n"
    texto = texto + f"   Entrada: {colaboracao[4]} | Saída: {saida}"
    return texto


# ===================== FUNÇÕES DE ARQUIVO =====================

def carregar_artistas(nome_arquivo):
    '''
    Lê o arquivo de artistas e retorna uma lista de listas.
    '''
    artistas = []
    if existe_arquivo(nome_arquivo):
        ref_arquivo = open(nome_arquivo, "r", encoding="utf-8")
        for linha in ref_arquivo:
            linha = linha.strip()
            if linha != "":
                campos = linha.split(";")
                if len(campos) == 7:
                    artista = [campos[0], campos[1], separar_itens(campos[2]),
                               campos[3], campos[4], campos[5],
                               separar_itens(campos[6])]
                    artistas.append(artista)
        ref_arquivo.close()
    return artistas


def salvar_artistas(artistas, nome_arquivo):
    '''
    Grava todos os artistas no arquivo texto (sobrescreve o arquivo).
    '''
    ref_arquivo = open(nome_arquivo, "w", encoding="utf-8")
    for artista in artistas:
        linha = [artista[0], artista[1], juntar_itens(artista[2], ","),
                 artista[3], artista[4], artista[5], juntar_itens(artista[6], ",")]
        ref_arquivo.write(juntar_itens(linha, ";") + "\n")
    ref_arquivo.close()


def carregar_obras(nome_arquivo):
    '''
    Lê o arquivo de obras e retorna uma lista de listas.
    '''
    obras = []
    if existe_arquivo(nome_arquivo):
        ref_arquivo = open(nome_arquivo, "r", encoding="utf-8")
        for linha in ref_arquivo:
            linha = linha.strip()
            if linha != "":
                campos = linha.split(";")
                if len(campos) == 6:
                    obra = [campos[0], campos[1], int(campos[2]), campos[3],
                            campos[4], float(campos[5])]
                    obras.append(obra)
        ref_arquivo.close()
    return obras


def salvar_obras(obras, nome_arquivo):
    '''
    Grava todas as obras no arquivo texto (sobrescreve o arquivo).
    '''
    ref_arquivo = open(nome_arquivo, "w", encoding="utf-8")
    for obra in obras:
        ref_arquivo.write(juntar_itens(obra, ";") + "\n")
    ref_arquivo.close()


def carregar_colaboracoes(nome_arquivo):
    '''
    Lê o arquivo de colaborações e retorna uma lista de listas.
    '''
    colaboracoes = []
    if existe_arquivo(nome_arquivo):
        ref_arquivo = open(nome_arquivo, "r", encoding="utf-8")
        for linha in ref_arquivo:
            linha = linha.strip()
            if linha != "":
                campos = linha.split(";")
                if len(campos) == 6:
                    colaboracao = [campos[0], campos[1], campos[2],
                                   float(campos[3]), campos[4], campos[5]]
                    colaboracoes.append(colaboracao)
        ref_arquivo.close()
    return colaboracoes


def salvar_colaboracoes(colaboracoes, nome_arquivo):
    '''
    Grava todas as colaborações no arquivo texto (sobrescreve o arquivo).
    '''
    ref_arquivo = open(nome_arquivo, "w", encoding="utf-8")
    for colaboracao in colaboracoes:
        ref_arquivo.write(juntar_itens(colaboracao, ";") + "\n")
    ref_arquivo.close()


def exibir_e_salvar_relatorio(linhas, nome_arquivo):
    '''
    Mostra as linhas do relatório na tela e grava no arquivo texto.
    '''
    ref_arquivo = open(nome_arquivo, "w", encoding="utf-8")
    for linha in linhas:
        print(linha)
        ref_arquivo.write(linha + "\n")
    ref_arquivo.close()
    print(f"\nRelatório salvo no arquivo '{nome_arquivo}'.")


# ===================== SUBMENU GENÉRICO =====================

def mostrar_opcoes_submenu(titulo):
    '''
    Mostra as opções padrão de um submenu.
    '''
    print(f"\n---------- SUBMENU DE {titulo} ----------")
    print("1. Listar todos")
    print("2. Listar um")
    print("3. Incluir")
    print("4. Alterar")
    print("5. Excluir")
    print("6. Voltar ao menu principal")


# ===================== ARTISTAS =====================

def submenu_artistas(artistas, colaboracoes, nome_arquivo):
    '''
    Submenu com as operações sobre artistas.
    '''
    opcao = ""
    while opcao != "6":
        mostrar_opcoes_submenu("ARTISTA")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            listar_artistas(artistas)
        elif opcao == "2":
            listar_um_artista(artistas)
        elif opcao == "3":
            incluir_artista(artistas, nome_arquivo)
        elif opcao == "4":
            alterar_artista(artistas, nome_arquivo)
        elif opcao == "5":
            excluir_artista(artistas, colaboracoes, nome_arquivo)
        elif opcao != "6":
            print("Opção inválida!")


def listar_artistas(artistas):
    '''
    Mostra todos os artistas cadastrados.
    '''
    if len(artistas) == 0:
        print("Nenhum artista cadastrado.")
    else:
        print(f"\n=== {len(artistas)} artista(s) cadastrado(s) ===")
        for artista in artistas:
            print(formatar_artista(artista))
            print("-" * 50)


def listar_um_artista(artistas):
    '''
    Mostra os dados de um artista a partir do CPF.
    '''
    cpf = ler_valor("CPF do artista: ", "cpf")
    posicao = buscar_artista(artistas, cpf)
    if posicao == -1:
        print("Artista não encontrado!")
    else:
        print(formatar_artista(artistas[posicao]))


def incluir_artista(artistas, nome_arquivo):
    '''
    Inclui um novo artista, sem permitir CPF repetido.
    '''
    print("\n=== INCLUIR ARTISTA ===")
    cpf = ler_valor("CPF do artista: ", "cpf")
    if buscar_artista(artistas, cpf) != -1:
        print("Já existe um artista cadastrado com esse CPF!")
    else:
        nome = ler_valor("Nome: ", "texto")
        telefones = ler_lista_itens("telefones")
        data_nascimento = ler_valor("Data de nascimento (dd/mm/aaaa): ", "data")
        nacionalidade = ler_valor("Nacionalidade: ", "texto")
        estilo = ler_valor("Estilo principal: ", "texto")
        redes = ler_lista_itens("redes sociais")
        artistas.append([cpf, nome, telefones, data_nascimento,
                         nacionalidade, estilo, redes])
        salvar_artistas(artistas, nome_arquivo)
        print("Artista cadastrado com sucesso!")


def alterar_artista(artistas, nome_arquivo):
    '''
    Altera os dados de um artista (o CPF, que é a chave, não pode mudar).
    '''
    cpf = ler_valor("CPF do artista a alterar: ", "cpf")
    posicao = buscar_artista(artistas, cpf)
    if posicao == -1:
        print("Artista não encontrado!")
    else:
        artista = artistas[posicao]
        print(formatar_artista(artista))
        print("\nDigite os novos dados:")
        artista[1] = ler_alteracao("Nome", artista[1], "texto")
        if confirmar(f"Telefones atuais: {juntar_itens(artista[2], ', ')}. Deseja substituí-los?"):
            artista[2] = ler_lista_itens("telefones")
        artista[3] = ler_alteracao("Data de nascimento", artista[3], "data")
        artista[4] = ler_alteracao("Nacionalidade", artista[4], "texto")
        artista[5] = ler_alteracao("Estilo principal", artista[5], "texto")
        if confirmar(f"Redes sociais atuais: {juntar_itens(artista[6], ', ')}. Deseja substituí-las?"):
            artista[6] = ler_lista_itens("redes sociais")
        salvar_artistas(artistas, nome_arquivo)
        print("Artista alterado com sucesso!")


def excluir_artista(artistas, colaboracoes, nome_arquivo):
    '''
    Exclui um artista após a confirmação dos dados.
    '''
    cpf = ler_valor("CPF do artista a excluir: ", "cpf")
    posicao = buscar_artista(artistas, cpf)
    if posicao == -1:
        print("Artista não encontrado!")
    elif possui_colaboracao(colaboracoes, cpf, 0):
        print("Não é possível excluir: o artista possui colaborações cadastradas.")
        print("Exclua as colaborações dele primeiro.")
    else:
        print(formatar_artista(artistas[posicao]))
        if confirmar("Confirma a exclusão deste artista?"):
            del artistas[posicao]
            salvar_artistas(artistas, nome_arquivo)
            print("Artista excluído com sucesso!")
        else:
            print("Exclusão cancelada.")


# ===================== OBRAS =====================

def submenu_obras(obras, colaboracoes, nome_arquivo):
    '''
    Submenu com as operações sobre obras.
    '''
    opcao = ""
    while opcao != "6":
        mostrar_opcoes_submenu("OBRA")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            listar_obras(obras)
        elif opcao == "2":
            listar_uma_obra(obras)
        elif opcao == "3":
            incluir_obra(obras, nome_arquivo)
        elif opcao == "4":
            alterar_obra(obras, nome_arquivo)
        elif opcao == "5":
            excluir_obra(obras, colaboracoes, nome_arquivo)
        elif opcao != "6":
            print("Opção inválida!")


def listar_obras(obras):
    '''
    Mostra todas as obras cadastradas.
    '''
    if len(obras) == 0:
        print("Nenhuma obra cadastrada.")
    else:
        print(f"\n=== {len(obras)} obra(s) cadastrada(s) ===")
        for obra in obras:
            print(formatar_obra(obra))
            print("-" * 50)


def listar_uma_obra(obras):
    '''
    Mostra os dados de uma obra a partir do código.
    '''
    codigo = ler_valor("Código da obra: ", "texto")
    posicao = buscar_obra(obras, codigo)
    if posicao == -1:
        print("Obra não encontrada!")
    else:
        print(formatar_obra(obras[posicao]))


def incluir_obra(obras, nome_arquivo):
    '''
    Inclui uma nova obra, sem permitir código repetido.
    '''
    print("\n=== INCLUIR OBRA ===")
    codigo = ler_valor("Código da obra: ", "texto")
    if buscar_obra(obras, codigo) != -1:
        print("Já existe uma obra cadastrada com esse código!")
    else:
        titulo = ler_valor("Título: ", "texto")
        ano = ler_valor("Ano de criação: ", "inteiro")
        tipo = ler_tipo_obra()
        descricao = ler_valor("Descrição: ", "texto")
        valor = ler_valor("Valor estimado (R$): ", "real")
        obras.append([codigo, titulo, ano, tipo, descricao, valor])
        salvar_obras(obras, nome_arquivo)
        print("Obra cadastrada com sucesso!")


def alterar_obra(obras, nome_arquivo):
    '''
    Altera os dados de uma obra (o código, que é a chave, não pode mudar).
    '''
    codigo = ler_valor("Código da obra a alterar: ", "texto")
    posicao = buscar_obra(obras, codigo)
    if posicao == -1:
        print("Obra não encontrada!")
    else:
        obra = obras[posicao]
        print(formatar_obra(obra))
        print("\nDigite os novos dados:")
        obra[1] = ler_alteracao("Título", obra[1], "texto")
        obra[2] = ler_alteracao("Ano de criação", obra[2], "inteiro")
        if confirmar(f"Tipo atual: {obra[3]}. Deseja alterar o tipo?"):
            obra[3] = ler_tipo_obra()
        obra[4] = ler_alteracao("Descrição", obra[4], "texto")
        obra[5] = ler_alteracao("Valor estimado (R$)", obra[5], "real")
        salvar_obras(obras, nome_arquivo)
        print("Obra alterada com sucesso!")


def excluir_obra(obras, colaboracoes, nome_arquivo):
    '''
    Exclui uma obra após a confirmação dos dados.
    '''
    codigo = ler_valor("Código da obra a excluir: ", "texto")
    posicao = buscar_obra(obras, codigo)
    if posicao == -1:
        print("Obra não encontrada!")
    elif possui_colaboracao(colaboracoes, codigo, 1):
        print("Não é possível excluir: a obra possui colaborações cadastradas.")
        print("Exclua as colaborações dela primeiro.")
    else:
        print(formatar_obra(obras[posicao]))
        if confirmar("Confirma a exclusão desta obra?"):
            del obras[posicao]
            salvar_obras(obras, nome_arquivo)
            print("Obra excluída com sucesso!")
        else:
            print("Exclusão cancelada.")


# ===================== COLABORAÇÕES =====================

def submenu_colaboracoes(colaboracoes, artistas, obras, nome_arquivo):
    '''
    Submenu com as operações sobre colaborações.
    '''
    opcao = ""
    while opcao != "6":
        mostrar_opcoes_submenu("COLABORAÇÃO")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            listar_colaboracoes(colaboracoes, artistas, obras)
        elif opcao == "2":
            listar_uma_colaboracao(colaboracoes, artistas, obras)
        elif opcao == "3":
            incluir_colaboracao(colaboracoes, artistas, obras, nome_arquivo)
        elif opcao == "4":
            alterar_colaboracao(colaboracoes, artistas, obras, nome_arquivo)
        elif opcao == "5":
            excluir_colaboracao(colaboracoes, artistas, obras, nome_arquivo)
        elif opcao != "6":
            print("Opção inválida!")


def soma_percentuais_obra(colaboracoes, codigo, posicao_ignorada):
    '''
    Soma os percentuais de contribuição já cadastrados para uma obra,
    ignorando a colaboração da posição informada (usado na alteração).
    '''
    soma = 0
    for i in range(len(colaboracoes)):
        if i != posicao_ignorada and colaboracoes[i][1].upper() == codigo.upper():
            soma = soma + colaboracoes[i][3]
    return soma


def ler_data_saida(data_entrada, valor_atual, alterando):
    '''
    Lê a data de saída (pode ficar vazia se a colaboração está em andamento)
    e garante que ela não seja anterior à data de entrada.
    '''
    data_ok = False
    while not data_ok:
        if alterando:
            data_saida = ler_alteracao("Data de saída", valor_atual, "data_opcional")
        else:
            data_saida = ler_valor("Data de saída (dd/mm/aaaa ou Enter se em andamento): ",
                                   "data_opcional")
        if data_saida == "" or data_para_numero(data_saida) >= data_para_numero(data_entrada):
            data_ok = True
        else:
            print("A data de saída não pode ser anterior à data de entrada!")
    return data_saida


def ler_percentual(colaboracoes, codigo, valor_atual, posicao_ignorada):
    '''
    Lê o percentual de contribuição, garantindo que a soma dos
    percentuais da obra não ultrapasse 100%.
    '''
    ja_usado = soma_percentuais_obra(colaboracoes, codigo, posicao_ignorada)
    print(f"Percentual já distribuído nesta obra: {ja_usado}%")
    percentual_ok = False
    while not percentual_ok:
        if valor_atual == -1:
            percentual = ler_valor("Percentual de contribuição (%): ", "percentual")
        else:
            percentual = ler_alteracao("Percentual de contribuição (%)", valor_atual, "percentual")
        if ja_usado + percentual <= 100:
            percentual_ok = True
        else:
            print(f"A soma dos percentuais da obra passaria de 100%! Máximo: {100 - ja_usado}%")
    return percentual


def listar_colaboracoes(colaboracoes, artistas, obras):
    '''
    Mostra todas as colaborações cadastradas.
    '''
    if len(colaboracoes) == 0:
        print("Nenhuma colaboração cadastrada.")
    else:
        print(f"\n=== {len(colaboracoes)} colaboração(ões) cadastrada(s) ===")
        for colaboracao in colaboracoes:
            print(formatar_colaboracao(colaboracao, artistas, obras))
            print("-" * 50)


def listar_uma_colaboracao(colaboracoes, artistas, obras):
    '''
    Mostra os dados de uma colaboração a partir do CPF e do código da obra.
    '''
    cpf = ler_valor("CPF do artista: ", "cpf")
    codigo = ler_valor("Código da obra: ", "texto")
    posicao = buscar_colaboracao(colaboracoes, cpf, codigo)
    if posicao == -1:
        print("Colaboração não encontrada!")
    else:
        print(formatar_colaboracao(colaboracoes[posicao], artistas, obras))


def incluir_colaboracao(colaboracoes, artistas, obras, nome_arquivo):
    '''
    Inclui uma nova colaboração. O artista e a obra precisam existir
    e não pode haver outra colaboração com o mesmo CPF e código de obra.
    '''
    print("\n=== INCLUIR COLABORAÇÃO ===")
    cpf = ler_valor("CPF do artista: ", "cpf")
    posicao_artista = buscar_artista(artistas, cpf)
    if posicao_artista == -1:
        print("Artista não cadastrado! Cadastre o artista primeiro.")
        return
    codigo = ler_valor("Código da obra: ", "texto")
    posicao_obra = buscar_obra(obras, codigo)
    if posicao_obra == -1:
        print("Obra não cadastrada! Cadastre a obra primeiro.")
        return
    codigo = obras[posicao_obra][0]
    if buscar_colaboracao(colaboracoes, cpf, codigo) != -1:
        print("Esse artista já possui colaboração cadastrada nessa obra!")
        return

    print(f"Artista: {artistas[posicao_artista][1]} | Obra: {obras[posicao_obra][1]}")
    papel = ler_valor("Papel (Modelagem, Textura, Roteiro, Animação, etc.): ", "texto")
    percentual = ler_percentual(colaboracoes, codigo, -1, -1)
    data_entrada = ler_valor("Data de entrada (dd/mm/aaaa): ", "data")
    data_saida = ler_data_saida(data_entrada, "", False)
    colaboracoes.append([cpf, codigo, papel, percentual, data_entrada, data_saida])
    salvar_colaboracoes(colaboracoes, nome_arquivo)
    print("Colaboração cadastrada com sucesso!")


def alterar_colaboracao(colaboracoes, artistas, obras, nome_arquivo):
    '''
    Altera os dados de uma colaboração (CPF e código da obra não mudam).
    '''
    cpf = ler_valor("CPF do artista: ", "cpf")
    codigo = ler_valor("Código da obra: ", "texto")
    posicao = buscar_colaboracao(colaboracoes, cpf, codigo)
    if posicao == -1:
        print("Colaboração não encontrada!")
    else:
        colaboracao = colaboracoes[posicao]
        print(formatar_colaboracao(colaboracao, artistas, obras))
        print("\nDigite os novos dados:")
        colaboracao[2] = ler_alteracao("Papel", colaboracao[2], "texto")
        colaboracao[3] = ler_percentual(colaboracoes, colaboracao[1], colaboracao[3], posicao)
        colaboracao[4] = ler_alteracao("Data de entrada", colaboracao[4], "data")
        colaboracao[5] = ler_data_saida(colaboracao[4], colaboracao[5], True)
        salvar_colaboracoes(colaboracoes, nome_arquivo)
        print("Colaboração alterada com sucesso!")


def excluir_colaboracao(colaboracoes, artistas, obras, nome_arquivo):
    '''
    Exclui uma colaboração após a confirmação dos dados.
    '''
    cpf = ler_valor("CPF do artista: ", "cpf")
    codigo = ler_valor("Código da obra: ", "texto")
    posicao = buscar_colaboracao(colaboracoes, cpf, codigo)
    if posicao == -1:
        print("Colaboração não encontrada!")
    else:
        print(formatar_colaboracao(colaboracoes[posicao], artistas, obras))
        if confirmar("Confirma a exclusão desta colaboração?"):
            del colaboracoes[posicao]
            salvar_colaboracoes(colaboracoes, nome_arquivo)
            print("Colaboração excluída com sucesso!")
        else:
            print("Exclusão cancelada.")


# ===================== RELATÓRIOS =====================

def submenu_relatorios(artistas, obras, colaboracoes):
    '''
    Submenu com os relatórios solicitados.
    '''
    opcao = ""
    while opcao != "4":
        print("\n---------- SUBMENU RELATÓRIOS ----------")
        print("1. Obras de um artista (por CPF)")
        print("2. Obras de um tipo específico")
        print("3. Colaborações entre duas datas")
        print("4. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            relatorio_obras_do_artista(artistas, obras, colaboracoes)
        elif opcao == "2":
            relatorio_obras_por_tipo(artistas, obras, colaboracoes)
        elif opcao == "3":
            relatorio_colaboracoes_periodo(artistas, obras, colaboracoes)
        elif opcao != "4":
            print("Opção inválida!")


def relatorio_obras_do_artista(artistas, obras, colaboracoes):
    '''
    a) Mostra todas as obras de um artista (CPF fornecido pelo usuário),
    incluindo o nome do artista e as redes sociais.
    '''
    cpf = ler_valor("CPF do artista: ", "cpf")
    posicao_artista = buscar_artista(artistas, cpf)
    if posicao_artista == -1:
        print("Artista não encontrado!")
        return

    artista = artistas[posicao_artista]
    linhas = ["===== RELATÓRIO: OBRAS DO ARTISTA =====",
              f"Artista: {artista[1]} (CPF: {artista[0]})",
              f"Redes sociais: {juntar_itens(artista[6], ', ')}",
              ""]
    quantidade = 0
    for colaboracao in colaboracoes:
        if colaboracao[0] == cpf:
            posicao_obra = buscar_obra(obras, colaboracao[1])
            if posicao_obra != -1:
                linhas.append(formatar_obra(obras[posicao_obra]))
                linhas.append(f"   Papel do artista: {colaboracao[2]} ({colaboracao[3]}%)")
                linhas.append("-" * 50)
                quantidade = quantidade + 1
    if quantidade == 0:
        linhas.append("Nenhuma obra encontrada para este artista.")
    else:
        linhas.append(f"Total de obras: {quantidade}")
    exibir_e_salvar_relatorio(linhas, "relatorio_obras_artista.txt")


def relatorio_obras_por_tipo(artistas, obras, colaboracoes):
    '''
    b) Mostra os dados de todas as obras de um tipo específico,
    bem como o nome do(s) artista(s) de cada obra.
    '''
    tipo = ler_tipo_obra()
    linhas = [f"===== RELATÓRIO: OBRAS DO TIPO {tipo.upper()} =====", ""]
    quantidade = 0
    for obra in obras:
        if obra[3] == tipo:
            nomes_artistas = []
            for colaboracao in colaboracoes:
                if colaboracao[1].upper() == obra[0].upper():
                    nomes_artistas.append(nome_do_artista(artistas, colaboracao[0]))
            linhas.append(formatar_obra(obra))
            if len(nomes_artistas) == 0:
                linhas.append("   Artista(s): nenhum artista vinculado")
            else:
                linhas.append(f"   Artista(s): {juntar_itens(nomes_artistas, ', ')}")
            linhas.append("-" * 50)
            quantidade = quantidade + 1
    if quantidade == 0:
        linhas.append("Nenhuma obra encontrada desse tipo.")
    else:
        linhas.append(f"Total de obras: {quantidade}")
    exibir_e_salvar_relatorio(linhas, "relatorio_obras_tipo.txt")


def relatorio_colaboracoes_periodo(artistas, obras, colaboracoes):
    '''
    c) Mostra todas as colaborações com data de entrada entre as datas X e Y
    (inclusive), apresentando nome do artista, título da obra, papel e
    percentual de contribuição.
    '''
    data_inicial = ler_valor("Data inicial (dd/mm/aaaa): ", "data")
    data_final = ler_valor("Data final (dd/mm/aaaa): ", "data")
    while data_para_numero(data_final) < data_para_numero(data_inicial):
        print("A data final não pode ser anterior à data inicial!")
        data_final = ler_valor("Data final (dd/mm/aaaa): ", "data")

    inicio = data_para_numero(data_inicial)
    fim = data_para_numero(data_final)
    linhas = [f"===== RELATÓRIO: COLABORAÇÕES DE {data_inicial} A {data_final} =====", ""]
    quantidade = 0
    for colaboracao in colaboracoes:
        entrada = data_para_numero(colaboracao[4])
        if entrada >= inicio and entrada <= fim:
            linhas.append(f"Artista: {nome_do_artista(artistas, colaboracao[0])}")
            linhas.append(f"   Obra: {titulo_da_obra(obras, colaboracao[1])}")
            linhas.append(f"   Papel: {colaboracao[2]} | Contribuição: {colaboracao[3]}%")
            linhas.append(f"   Data de entrada: {colaboracao[4]}")
            linhas.append("-" * 50)
            quantidade = quantidade + 1
    if quantidade == 0:
        linhas.append("Nenhuma colaboração encontrada nesse período.")
    else:
        linhas.append(f"Total de colaborações: {quantidade}")
    exibir_e_salvar_relatorio(linhas, "relatorio_colaboracoes_periodo.txt")


# início da execução do programa
#-----------------------------------------------------
main()  # chamada da função main
