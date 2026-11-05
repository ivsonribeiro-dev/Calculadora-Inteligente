from time import sleep
from datetime import datetime
import sqlite3
import sys
import os

def linha(tam = 40):
    return '-' * tam


def titulo(msg):
       """
    -> Função para criar um titulo principal já formatado, centralizado, de acordo com o tamanho da linha.
    :param msg: nome do titulo escolhido
    :return: sem retorno
    """
       print(linha())
       print(msg.center(40))
       print(linha())


def formatar_numero(valor):
       """
    -> Função para formatar os valores numericos de acordo com o que for digitado, voltando um número inteiro ou décimal.
    :param valor: número digitado pelo usúario
    :return: retorno de um número inteiro ou décimal com sua formatação de casas já pré definidas
    """
       if valor .is_integer():
           return str(int(valor))
       else:
           texto = f'{valor:.4f}'.rstrip('0').rstrip('.')
           return texto.replace('.', ',')


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

#Banco de Dados
caminho_da_pasta = os.path.dirname(os.path.abspath(__file__))
caminho_do_banco = os.path.join(caminho_da_pasta, 'calculadora.db')
conn = sqlite3.connect(caminho_do_banco)
cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   num1 REAL,
                   operacao TEXT,
                   num2 REAL,
                   resultado REAL
        )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultado_acumulado (
                   id INTEGER PRIMARY KEY,
                   acumulador REAL
        )
    ''')
conn.commit()

try:
    cursor.execute('ALTER TABLE historico ADD COLUMN data_hora TEXT')
    conn.commit()
except sqlite3.OperationalError:
    pass

cursor.execute('SELECT acumulador FROM resultado_acumulado WHERE id = 1')
resultado_banco = cursor.fetchone()

if resultado_banco is None:
    total = 0.0
    cursor.execute('INSERT INTO resultado_acumulado (id, acumulador) VALUES (1, ?)', (total,))
    conn.commit()
else:
    total = resultado_banco[0]

#Programa Principal
total = 0
sinais_permitidos = ['+', '-', '*', '/']

while True:
    try:
        limpar_tela()
        titulo('CALCULADORA')
        print('MENU:')
        print('-' * 5)
        print('\033[1;33m1\033[m - \033[1;36mNova operação\033[m')
        print('\033[1;33m2\033[m - \033[1;36mContinuar Operação\033[m')
        print('\033[1;33m3\033[m - \033[1;36mVer Histórico\033[m')
        print('\033[1;33m4\033[m - \033[1;36mLimpar Histórico\033[m')
        print('\033[1;33m5\033[m - \033[1;36mSair\033[m')
        acao = input('Escolha uma opção: ')
        print(linha())
        
        if acao == '1' or acao == '2':
            try:
                if acao == '1':
                    n1 = float(input('Digite o primeiro número: ').replace(',', '.'))
                else:
                    n1 = total
                    print(f'Resultado anterior: {n1}')
                op = input('Digite a operação (\033[1;32m+\033[m | \033[1;32m-\033[m |\033[1;32m *\033[m | \033[1;32m/\033[m): ')
                if op not in sinais_permitidos or op == ' ':
                     print('\033[1;31mERRO: Operação Inválida!\033[m')
                     print(linha())
                     input()
                     continue
                n2 = float(input('Digite o segundo número: ').replace(',', '.'))
                if op == '+':
                    resp = n1 + n2
                elif op == '-':
                    resp = n1 - n2
                elif op == '*':
                    resp = n1 * n2
                elif op == '/':
                    if n2 == 0:
                        print('\033[1;31mERRO: Divisão por zero!\033[m')
                        print(linha())
                        input()
                        continue
                    resp = n1 / n2
                n1_fmt = formatar_numero(n1) 
                n2_fmt = formatar_numero(n2)
                resp_fmt = formatar_numero(resp)
                print(f'\033[1;32mResultado: {n1_fmt} {op} {n2_fmt} = {resp_fmt}\033[m')
                agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                total = resp
                cursor.execute('INSERT INTO historico (num1, operacao, num2, resultado, data_hora) VALUES (?, ?, ?, ?, ?)', (n1, op, n2, resp, agora))
                cursor.execute('UPDATE resultado_acumulado SET acumulador = ? WHERE id = 1', (total,))
                conn.commit()
                print(linha())
                print('Operação salva com sucesso!')
                input()
            except (NameError):
                print('\033[1;31mERRO: Operação Inválida!\033[m')
                print(linha())
                input()
            except (ValueError, TypeError):
                print('\033[1;31mERRO: Por favor, digite apenas números válidos.\033[m')
                print(linha())
                input()
            except (KeyboardInterrupt):
                print('\033[1;31mOperação cancelada pelo usúario.\033[m')
                print(linha())
                input()
        
        elif acao == '3':
            limpar_tela()
            cursor.execute('SELECT num1, operacao, num2, resultado, data_hora FROM historico')
            linhas = cursor.fetchall()
            titulo('=== HISTÓRICO DE CALCULOS ===')
            if not linhas:
                print('Nenhum registro encontrado.')
            else:
                print(f"{'DATA / HORA':^19} | {'OPERAÇÃO':^18}")
                print(f"{'-'*19}-+-{'-'*18}")
                for reg in linhas:
                    n1_h = formatar_numero(reg[0])
                    op_h = reg[1]
                    n2_h = formatar_numero(reg[2])
                    res_h = formatar_numero(reg[3])
                    dt_h = reg[4] if reg[4] is not None else 'Sem Data'
                    print(f"{dt_h:^19} | {n1_h:>2} {op_h:^3} {n2_h:<2} {'=':^1} {res_h:<8}")
            print(linha())
            input()
        
        elif acao == '4':
            certeza = input('Apagar todo o histórico definitivamente? (s/n): ').lower()
            if certeza == 's':
                cursor.execute('DELETE FROM historico')
                total = 0.0
                cursor.execute('UPDATE resultado_acumulado SET acumulador = ? WHERE id = 1', (total,))
                conn.commit()
                print('Histórico limpo!')
                input()
            else:
                input()
        
        elif acao == '5':
            print('Saindo...')
            sleep(1)
            print('\033[1;32mFINALIZADO!!!\033[m')
            break
        
        elif acao > '5':
            print('\033[1;31mERRO! Opção inválida, Tente Novamente!\033[m')
            print(linha())
            sleep(4)
    
    except (KeyboardInterrupt):
            print('\033[1;31mOperação cancelada pelo usúario.\033[m')
            
conn.close()
