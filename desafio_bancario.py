import datetime
import textwrap

def menu():
    menu = """
            [d] Depositar | [s] Sacar | [e] Extrato | [nu] Novo Usuário | [nc] Nova Conta | [lc] Listar Contas | [q] Sair
            => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /, conta):
    if valor > 0 and conta:
        conta['saldo'] += valor
        conta['extrato'] += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido ou conta não encontrada.")

    return conta['saldo'], conta['extrato']

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques, conta):
    if not conta:
        print("Operação falhou! Conta não encontrada.")
        return saldo, extrato

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        conta['saldo'] -= valor
        conta['extrato'] += f"Saque: R$ {valor:.2f}\n"
        conta['numero_saques'] += 1
        print("Saque realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return conta['saldo'], conta['extrato']

def exibir_extrato(saldo, /, *, extrato, conta):
    if not conta:
        print("Operação falhou! Conta não encontrada.")
        return

    print("\n================ EXTRATO ===============")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF, apenas números: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return
    
    nome = input("Informe o nome completo do cliente: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    logradouro = input("Vamos cadastrar o endereço\nInforme o Logradouro: ")
    nro = input("Informe o número: ")
    bairro = input("Informe o bairro: ")
    cidade = input("Informe a cidade: ")
    sigla_estado = input("Informe a sigla do estado: ")

    endereco = f'{logradouro}, {nro} - {bairro} - {cidade}/{sigla_estado}'

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")    

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:        
        print(f"Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": str(numero_conta), "usuario": usuario, "saldo": 0, "limite": 500, "extrato": "", "numero_saques": 0, "limite_saques": 3}
    else:
        print("Usuário não encontrado. Conta não pode ser criada.")

def listar_contas(contas):
    for conta in contas:
        registro = f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("---------------------------------------------------------------------------------------------------")
        print(textwrap.dedent(registro))

def obter_conta(agencia, numero_conta, contas):
    for conta in contas:
        if conta['agencia'] == agencia and conta['numero_conta'] == str(numero_conta):
            return conta
    return None

def app():
    
    AGENCIA = "0001"
    
    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "d":
            agencia = input("Informe a agência: ")
            numero_conta = input("Informe o número da conta: ")
            conta = obter_conta(agencia, numero_conta, contas)
            if conta:
                valor = float(input("Informe o valor do depósito: "))
                saldo, extrato = depositar(conta['saldo'], valor, conta['extrato'], conta=conta)
                conta['saldo'] = saldo
                conta['extrato'] = extrato
            else:
                print("Conta não encontrada.")
            

        elif opcao == "s":
            agencia = input("Informe a agência: ")
            numero_conta = input("Informe o número da conta: ")
            conta = obter_conta(agencia, numero_conta, contas)
            if conta:
                valor = float(input("Informe o valor do saque: "))
                saldo, extrato = sacar(
                    saldo=conta['saldo'], 
                    valor=valor, 
                    extrato=conta['extrato'], 
                    limite=conta['limite'], 
                    numero_saques=conta['numero_saques'], 
                    limite_saques=conta['limite_saques'], 
                    conta=conta
                )
                conta['saldo'] = saldo
                conta['extrato'] = extrato
            else:
                print("Conta não encontrada.")

        elif opcao == "e":
            agencia = input("Informe a agência: ")
            numero_conta = input("Informe o número da conta: ")
            conta = obter_conta(agencia, numero_conta, contas)
            if conta:
                exibir_extrato(conta['saldo'], extrato=conta['extrato'], conta=conta)
            else:
                print("Conta não encontrada.")

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

app()
