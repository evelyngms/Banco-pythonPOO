import random # biblioteca em python para gerar num aleatorio
import os # biblioteca em python para interação

class ContaCorrente:
    def __init__(self, nomeTitular, numeroConta, senha, saldo) -> None:
        self.nomeTitular = nomeTitular
        self.numeroConta = numeroConta
        self._senha = senha
        self._saldo = saldo

    # metodos de acesso ao saldo
    def get_saldo_corrente(self):
        return self._saldo

    def set_saldo_corrente(self, valor):
        self._saldo = valor

    def get_senha(self):
        return self._senha

    # metodos de operação na conta corrente
    def sacar(self, valorSaque):
        if self._saldo >= valorSaque:
            self._saldo -= valorSaque
            print(f"Saque de R${valorSaque} realizado com sucesso!")
            return True
        else:
            print("Saldo insuficiente")
            return False

    def depositar(self, valorDeposito):
        self._saldo += valorDeposito
        print(f"Depósito de R${valorDeposito} realizado com sucesso!")

    def aplicar(self, valorAplicacao, contaPoupanca):
        if self._saldo >= valorAplicacao:
            self._saldo -= valorAplicacao
            contaPoupanca.set_saldo_poupanca(contaPoupanca.get_saldo_poupanca() + valorAplicacao)
            print(f"Aplicação de R${valorAplicacao} realizada com sucesso na conta poupança!")
            return True
        else:
            print("Saldo insuficiente para aplicação")
            return False

class ContaPoupanca(ContaCorrente):
    def __init__(self, nomeTitular, numeroConta, senha, saldoCorrente, saldoPoupanca):
        super().__init__(nomeTitular, numeroConta, senha, saldoCorrente)
        self._saldoPoupanca = saldoPoupanca  # saldo da conta poupança

    # metodos de acesso ao saldo da poupança
    def get_saldo_poupanca(self):
        return self._saldoPoupanca

    def set_saldo_poupanca(self, valor):
        self._saldoPoupanca = valor

    def resgatar(self, valorResgate):
        if self.get_saldo_poupanca() >= valorResgate:  
            self.set_saldo_poupanca(self.get_saldo_poupanca() - valorResgate)  # atualiza o saldo da poupança
            contaCorrenteSaldo = self.get_saldo_corrente()  # acessa o saldo da conta corrente 
            self.set_saldo_corrente(contaCorrenteSaldo + valorResgate)  # atualiza o saldo da conta corrente
            print(f"Resgate de R${valorResgate} realizado com sucesso!")
            return True
        else:
            print("Saldo insuficiente na poupança para realizar o resgate.")
            return False


    # metodo de extrato 
    def extrato(self):
        print(f"\n+------------------------------------------------+")
        print(f"| Titular: {self.nomeTitular}")
        print(f"| Número da conta: {self.numeroConta}")
        print(f"| Saldo da Conta Corrente: R${self.get_saldo_corrente()}")
        print(f"| Saldo da Conta Poupança: R${self.get_saldo_poupanca()}")
        print(f"+------------------------------------------------+")

# funçao de verificaçao da senha
def verificarSenha(conta, senhaDigitada):
    return conta.get_senha() == senhaDigitada

def main():
    # cadastro de conta
    while True:
        nomeTitular = input("Informe seu nome completo: ")
        numeroConta = random.randint(100, 999) # gera o numero aleatorio de 3 digitos da conta
        senhaConta = input("Dê uma senha de 4 dígitos à sua conta: ")
        depositoInicial = float(input("Informe o valor do seu depósito inicial: "))
        
        if depositoInicial < 10:
            print("O depósito inicial deve ser de, no mínimo, R$ 10,00.")
            continue
        else:
            contaUsuario = ContaCorrente(nomeTitular, numeroConta, senhaConta, depositoInicial)
            contaPoupanca = ContaPoupanca(nomeTitular, numeroConta, senhaConta, depositoInicial, 0)
            break

    tentativas = 3
    while True:
        if tentativas == 0:
            print("Você errou a senha três vezes, sua conta foi bloqueada.")
            input("Pressione enter para continuar...")
            break

        print(''' INFORME A AÇÃO QUE DESEJA:
        0 - VISUALIZAR EXTRATO
        1 - SACAR
        2 - DEPOSITAR
        3 - APLICAR NA POUPANÇA
        4 - RESGATAR DA POUPANÇA
        5 - SAIR ''')
        
        acao = int(input())

        # solicita a senha antes de realizar qualquer operação
        senhaDigitada = input("Digite sua senha: ")
        if not verificarSenha(contaUsuario, senhaDigitada):
            tentativas -= 1
            print(f"Senha incorreta, você tem mais {tentativas} tentativas.")
            input("Pressione enter para continuar...")
            continue

        if acao == 0:
            contaPoupanca.extrato()
            input("Pressione enter para continuar...")

        elif acao == 1:
            valorSaque = float(input("Informe o valor do saque: "))
            if contaUsuario.sacar(valorSaque):
                print(f"Seu saldo atual é: R${contaUsuario.get_saldo_corrente()}")
            input("Pressione enter para continuar...")

        elif acao == 2:
            valorDeposito = float(input("Informe o valor do depósito: "))
            contaUsuario.depositar(valorDeposito)
            print(f"Seu saldo atual é: R${contaUsuario.get_saldo_corrente()}")
            input("Pressione enter para continuar...")

        elif acao == 3:
            valorAplicacao = float(input("Informe o valor a ser aplicado: "))
            if contaUsuario.aplicar(valorAplicacao, contaPoupanca):
                print(f"Seu saldo atual é: R${contaUsuario.get_saldo_corrente()}")
                print(f"Seu saldo na Poupança é: R${contaPoupanca.get_saldo_poupanca()}")
            input("Pressione enter para continuar...")

        elif acao == 4: 
            if isinstance(contaPoupanca, ContaPoupanca):  # verifica se é uma ContaPoupanca
                valorResgate = float(input("Informe o valor a resgatar: "))
                if contaPoupanca.resgatar(valorResgate):  
                    print(f"Seu saldo atual na Conta Corrente é: R${contaUsuario.get_saldo_corrente()}")
                    print(f"Seu saldo atual na Conta Poupança é: R${contaPoupanca.get_saldo_poupanca()}")
            else:
                print("Ação disponível apenas para contas Poupança.")
            input("Pressione enter para continuar...")


        elif acao == 5:
            break # encerra o sistema

        else:
            print("AÇÃO INVÁLIDA, TENTE NOVAMENTE.")
            input("Pressione enter para continuar...")

        os.system('cls')  # limpa a tela 

# verifica se o script esta sendo executado diretamente, e não importado de outro arquivo
if __name__ == "__main__":
    main()
