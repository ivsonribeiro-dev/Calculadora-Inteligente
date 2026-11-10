import cmath
import os
import sqlite3
import subprocess
from datetime import datetime
from fractions import Fraction
from time import sleep

# Utilidades: Funções utilitárias para exibição visualmente limpa do sistema.


def linha(tam = 80):
    print('-' * tam)


def titulo(msg):
       linha()
       print(msg.center(80))
       linha()


def limpar_tela():
    comando = 'cls' if os.name == 'nt' else 'clear'
    try:
        subprocess.run(comando, shell=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n" * 100)


def ler_coeficiente(mensagem, permitir_zero=True):
    '''Lê e valida um coeficiente numérico, impedindo zero quando exigido.'''
    while True:
        try:
            entrada = input(mensagem).strip().replace(',', '.')
            valor = float(entrada)
            if not permitir_zero and valor == 0:
                print('\033[1;31mERRO: O coeficiente "a" não pode ser zero.\033[m')
                linha()
                continue
            return valor
        except ValueError:
            print('\033[1;31mERRO: Por favor, digite apenas números válidos.\033[m')
            linha()


# Frações e Cálculos: Funções para formatação de números, equações e resultados, incluindo suporte a frações e números complexos.


def formatar_numero(valor):
    """Formata os valores númericos, retornando um número inteiro ou decimal."""
    if valor .is_integer():
        return str(int(valor))
    else:
        texto = f'{valor:.4f}'.rstrip('0').rstrip('.')
        return texto.replace('.', ',')


def formatar_equacao(valor):
    '''Formata o valor da equação retornando um número sem parênteses caso seja positivo 
    e com parênteses caso seja negativo.'''
    if valor >= 0:
        return f'{valor:.0f}'
    else:
        return f'({valor:.0f})'


def formatar_resultado(valor):
    '''Converte números decimais em frações formadas por sobrescritos e subscritos.'''
    # Extrai a parte real caso o número complexo não possua parte imaginária
    if isinstance(valor, complex):
        if valor.imag == 0:
            valor = valor.real
        else:
            return str(valor)
            
    if valor % 1 == 0:
        return str(int(valor))

    # Converte o decimal para a fração simplificada mais próxima
    fracao = Fraction(valor).limit_denominator()
    num = fracao.numerator
    den = fracao.denominator
    
    # Mapas unicode para representação visual de numerador e denominador
    sobrescritos = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}
    subscritos = {"0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉"}
    
    topo = "".join(sobrescritos[digito] for digito in str(abs(num)))
    baixo = "".join(subscritos[digito] for digito in str(den))
    sinal = "-" if num < 0 else ""
    return f"{sinal}{topo}/{baixo}"


def bhaskara(coef_a, coef_b, coef_c):
    '''Calcula as raízes reais ou complexas de uma equação do 2º grau.'''
    if coef_a == 0:
        return ("O coeficiente 'a' não pode ser igual a zero.")
    
    print('Equação'.center(30))
    print()
    print('Calculando o discriminante...')
    sleep(2)
    print()

    # Formata os coeficientes para exibição na equação
    format_a = formatar_equacao(coef_a)
    format_b = formatar_equacao(coef_b)
    format_c = formatar_equacao(coef_c)
    
    delta = (coef_b ** 2) - (4 * coef_a * coef_c)
    print(f'∆ = {format_b}² - 4.{format_a}.{format_c}')
    conta1 = (coef_b ** 2)
    conta2 = (-4 * coef_a * coef_c)
    if conta2 >=0:
        print(f'∆ = {conta1:.0f} + {conta2:.0f}')
    else:
        numero = conta2 * -1
        print(f'∆ = {conta1:.0f} - {numero:.0f}')
    print(f'∆ = {delta:.0f}')
    print()
    
    print('Bhaskara'.center(30))
    print()
    print('Aplicando a fórmula de Bhaskara...')
    sleep(3)
    print()

    # Usa cmath para suportar raízes complexas quando o delta for negativo
    print(f'x = -{format_b} ± √{delta:.0f} / 2.{coef_a:.0f}')
    x1 = (-coef_b + cmath.sqrt(delta)) / (2 * coef_a)
    x2 = (-coef_b - cmath.sqrt(delta)) / (2 * coef_a)
    conta3 = (cmath.sqrt(delta))
    conta4 = (2 * coef_a)
    valor_b = coef_b * -1

    if coef_b <= 0:
        print(f'x = {valor_b:.0f} ± {conta3.real:.0f} / {conta4:.0f}')
    else:
        print(f'x = -{coef_b:.0f} ± {conta3.real:.0f} / {conta4:.0f}')
    print()

    conta5 = (-coef_b + cmath.sqrt(delta))
    conta6 = (-coef_b - cmath.sqrt(delta))

    if coef_b <= 0:
        print(f'x¹ = {valor_b:.0f} + {conta3.real:.0f} / {conta4:.0f}')
    else:
        print(f'x¹ = -{coef_b:.0f} + {conta3.real:.0f} / {conta4:.0f}')
        print(f'x¹ = {conta5.real:.0f} / {conta4:.0f}')
        print()

    if coef_b <= 0:
        print(f'x² = {valor_b:.0f} - {conta3.real:.0f} / {conta4:.0f}')
    else:
        print(f'x² = -{coef_b:.0f} - {conta3.real:.0f} / {conta4}')
        print(f'x² = {conta6.real:.0f} / {conta4:.0f}')
        print()

    try:
        txt_x1 = formatar_resultado(x1)
        txt_x2 = formatar_resultado(x2)

        if delta < 0:
            txt_res_banco = f"Sem reais. x¹={txt_x1} x²={txt_x2}"
        elif delta == 0:
            txt_res_banco = f"x = {txt_x1}"
        else:
            txt_res_banco = f"x¹={txt_x1} x²={txt_x2}"

        agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        conn = sqlite3.connect(caminho_do_banco)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO historico_expressoes (tipo, coef_a, coef_b, coef_c, resultado_texto, data_hora)
            VALUES (?, ?, ?, ?, ?, ?)''', ('2_GRAU', coef_a, coef_b, coef_c, txt_res_banco, agora))
        conn.commit()
        conn.close()
    except Exception as erro_banco:
        print(f"\n\033[1;31mAviso: Não foi possível salvar no histórico.({erro_banco})\033[m")
        linha()

    if delta < 0:
        print()
        return (f'A equação não possui raizes reais: \n x¹ = {formatar_resultado(x1)}\n x² = {formatar_resultado(x2)}')
    elif delta == 0:
        print()
        return (f'A equação possui apenas uma única raiz real: x = {formatar_resultado(x1)}')
    else:
        print()
        return (f'As raizes da equação são reais: \n x¹ = {formatar_resultado(x1)}\n x² = {formatar_resultado(x2)}')


def primeiro_grau(coef_a, coef_b):
    '''Calcula a raiz de uma equação do 1º grau.'''
    if coef_a == 0:
        return ('O coeficiente "a" não pode ser igual a zero.')
    
    print('Resolução passo a passo:'.center(40))
    print()                          

    sinal_b = f"+ {coef_b:.0f}" if coef_b >= 0 else f"- {abs(coef_b):.0f}"
    print(f"Equação montada: {coef_a:.0f}x {sinal_b} = 0")
    print()
    sleep(1)

    valor_b_invertido = coef_b * -1
    print(f"Passo 1: {coef_a:.0f}x = {valor_b_invertido:.0f}")
    sleep(1)

    print(f"Passo 2: x = {valor_b_invertido:.0f} / {coef_a:.0f}")
    print()
    sleep(1)

    resultado_x = valor_b_invertido / coef_a
    try:
        txt_res_banco = f"x = {formatar_resultado(resultado_x)}"
        agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        conn = sqlite3.connect(caminho_do_banco)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO historico_expressoes (tipo, coef_a, coef_b, coef_c, resultado_texto, data_hora)
            VALUES (?, ?, ?, ?, ?, ?)''', ('1_GRAU', coef_a, coef_b, 0, txt_res_banco, agora))
        conn.commit()
        conn.close()
    except Exception as erro_banco:
        print(f"\n\033[1;31mAviso: Não foi possível salvar no histórico.({erro_banco})\033[m")
        linha()

    return (f'Resultado Final: \nx = {formatar_resultado(resultado_x)}')


# Banco de Dados: Inicialização do banco de dados SQLite para armazenar o histórico de operações e expressões.

caminho_da_pasta = os.path.dirname(os.path.abspath(__file__))
caminho_do_banco = os.path.join(caminho_da_pasta, 'calculadorav2.db')
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

cursor.execute ('''
    CREATE TABLE IF NOT EXISTS historico_expressoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        coef_a REAL,
        coef_b REAL,
        coef_c REAL,
        resultado_texto TEXT,
        data_hora TEXT
    )
''')
conn.commit()
conn.close()

# Programa Principal
total = 0
sinais_permitidos = ['+', '-', '*', '/', '%']

while True:
    try:
        limpar_tela()
        titulo('CALCULADORA INTELIGENTE')
        print('MENU:')
        print('-' * 5)
        print('\033[1;33m1\033[m - \033[1;36mNova operação\033[m')
        print('\033[1;33m2\033[m - \033[1;36mExpressões Númericas\033[m')
        print('\033[1;33m3\033[m - \033[1;36mVer Histórico\033[m')
        print('\033[1;33m4\033[m - \033[1;36mLimpar Histórico\033[m')
        print('\033[1;33m5\033[m - \033[1;36mSair\033[m')
        print()
        acao = input('Escolha uma opção: ').strip()
        linha()
        
        if acao == '1':
            limpar_tela()
            titulo('Nova Operação')
            print('Use [\033[1;32m=\033[m] para ver o resultado final.')
            print('Digite [\033[1;33mM\033[m] na operação para voltar ao menu.')
            linha()
            
            while True:
                entrada_n1 = input('Digite o primeiro número: ').strip().lower()
                if entrada_n1 in ('', 'm'):
                    break
                try:
                    resultado_parcial = float(entrada_n1.replace(',', '.'))
                    break
                except ValueError:
                    linha()
                    print('\033[1;31mERRO: Por favor, digite apenas números válidos.\033[m')
                    linha()

            if entrada_n1 in ('', 'm'):    
                continue

            while True:
                op = input('Digite a operação (\033[1;32m+\033[m | \033[1;32m-\033[m |\033[1;32m *\033[m | \033[1;32m/\033[m | \033[1;32m%\033[m | \033[1;32m=\033[m): ').strip().lower()
                    
                if op == 'm':
                    break
                if op == '=':
                    linha()
                    print(f'\033[1;32mResultado Final: {formatar_numero(resultado_parcial)}\033[m')
                    linha()
                        
                    total = resultado_parcial
                    conn = sqlite3.connect(caminho_do_banco)
                    cursor = conn.cursor()
                    cursor.execute('UPDATE resultado_acumulado SET acumulador = ? WHERE id = 1', (total,))
                    conn.commit()
                    conn.close()
                    while True:
                        opcao_fim = input('Deseja [C]ontinuar ou voltar ao [M]enu? ').strip().upper()
                        if opcao_fim in ('C', 'M'):
                            break
                        linha()
                        print('\033[1;31mERRO: Opção Inválida.\033[m')
                        linha()
   
                    if opcao_fim == 'C':
                        linha()
                        continue
                    else:
                        break
                    
                if op not in sinais_permitidos or op == ' ':
                    linha()
                    print('\033[1;31mERRO: Operação Inválida!\033[m')
                    linha()
                    input('Pressione [ENTER] para tentar novamente...')
                    linha()
                    continue

                while True:
                    try:
                        entrada_n2 = input('Digite o segundo número: ')
                        n2 = float(entrada_n2.replace(',', '.'))
                        break
                    except ValueError:
                        print('\033[1;31mERRO: Por favor, digite apenas números válidos.\033[m')
                        linha()
                        
                if op == '+':
                    prox_resultado = resultado_parcial + n2
                elif op == '-':
                    prox_resultado = resultado_parcial - n2
                elif op == '*':
                    prox_resultado = resultado_parcial * n2
                elif op == '/':
                    if n2 == 0:
                        print('\033[1;31mERRO: Divisão por zero!\033[m')
                        linha()
                        input('Pressione [ENTER] para voltar á operação...')
                        continue
                    prox_resultado = resultado_parcial / n2
                elif op == '%':
                    prox_resultado = resultado_parcial * (n2 / 100)
                    
                conn = sqlite3.connect(caminho_do_banco)
                cursor = conn.cursor()
                agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                cursor.execute('INSERT INTO historico (num1, operacao, num2, resultado, data_hora) VALUES (?, ?, ?, ?, ?)', (resultado_parcial, op, n2, prox_resultado, agora))
                conn.commit()
                conn.close()
                    
                resultado_parcial = prox_resultado
        
        elif acao == '2':
            while True:
                try:
                    limpar_tela()
                    titulo('Expressões Númericas')
                    print('\033[1;33m1\033[m - \033[1;36mEquações do Primeiro Grau\033[m')
                    print('\033[1;33m2\033[m - \033[1;36mEquações do Segundo Grau / Bhaskara\033[m')
                    print('\033[1;33m3\033[m - \033[1;36mVer Histórico\033[m')
                    print('\033[1;33m4\033[m - \033[1;36mLimpar Histórico\033[m')
                    print('\033[1;33m5\033[m - \033[1;36mVoltar ao Menu\033[m')
                    print()
                    escolha = input('Escolha o tipo de expressão: ').strip()

                    if escolha == '1':
                        while True:
                            try:
                                limpar_tela()
                                titulo('Equações do Primeiro Grau')
                                print('ax + b = 0')
                                linha()
                                print('Digite os Coeficientes: [a], [b]')
                                linha()
                                coef_a = ler_coeficiente('Valor de a: ', permitir_zero=False)
                                coef_b = ler_coeficiente('Valor de b: ')
                                linha()

                                resultado = primeiro_grau(coef_a, coef_b)
                                print(resultado)
                                linha()
                                while True:
                                    continuar = input('Deseja fazer outra conta? [S/N]: ').strip().upper()
                                    if continuar in ('S', 'N'):
                                        break
                                    linha()
                                    print('\033[1;31mERRO: Opção Inválida.\033[m')
                                    linha()
                                if continuar == 'S':
                                    linha()
                                    continue
                                else:
                                    break

                            except ValueError:
                                print()
                                print('\033[1;31mERRO: Por favor, digite apenas números válidos.\033[m')
                                input('Pressione [ENTER] para tentar novamente...')
                            continue

                    elif escolha == '2':
                        while True:
                            try:
                                limpar_tela()
                                titulo('Equações do Segundo Grau / Bhaskara')
                                print('∆ = b² - 4.a.c')
                                print('x = (-b ± √∆) / 2.a')
                                linha()
                                print('Digite os Coeficientes: [a], [b], [c]')
                                linha()
                                coef_a = ler_coeficiente('Valor de a: ', permitir_zero=False)
                                coef_b = ler_coeficiente('Valor de b: ')
                                coef_c = ler_coeficiente('Valor de c: ')
                                linha()

                                resultado = bhaskara(coef_a, coef_b, coef_c)
                                print(resultado)
                                linha()

                                while True:
                                    continuar = input('Deseja fazer outra conta? [S/N]: ').strip().upper()
                                    if continuar in ('S', 'N'):
                                        break
                                    linha()
                                    print('\033[1;31mERRO: Opção Inválida.\033[m')
                                    linha()
                                if continuar == 'S':
                                    linha()
                                    continue
                                else:
                                    break

                            except ValueError:
                                print()
                                print('\033[1;31mERRO: Por favor, digite apenas números válidos.\033[m')
                                input('Pressione [ENTER] para tentar novamente...')
                            continue

                    elif escolha == '3':
                        limpar_tela()
                        print(f"|{'-'*21}-{'-'*6}-{'-'*24}-{'-'*24}|")
                        print(f"{'HISTÓRICO DE EXPRESSÕES'.center(80)}")

                        conn = sqlite3.connect(caminho_do_banco)
                        cursor = conn.cursor()
                        cursor.execute('SELECT tipo, coef_a, coef_b, coef_c, resultado_texto, data_hora FROM historico_expressoes')
                        linhas = cursor.fetchall()
                        conn.close()

                        if not linhas:
                            print(f"|{'-'*21}-{'-'*6}-{'-'*24}-{'-'*24}|")
                            print()
                            print('Nenhum registro de equação encontrado.')
                            linha()
                        else:
                            print(f"|{'-'*21}-{'-'*6}-{'-'*24}-{'-'*24}|")
                            print(f"| {'DATA / HORA':^19} | {'TIPO':^4} | {'COEFICIENTES':^22} | {'RESULTADO':^22} |")
                            print(f"|{'-'*21}+{'-'*6}+{'-'*24}+{'-'*24}|")

                            for reg in linhas:
                                tipo_txt = '1ºG' if reg[0] == '1_GRAU' else '2ºG'
                                dt_h = reg[5] if reg[5] is not None else 'Sem Data'

                                if reg[0] == '1_GRAU':
                                    coefs = f"a:{formatar_numero(reg[1])}, b:{formatar_numero(reg[2])}"
                                else:
                                    coefs = f"a:{formatar_numero(reg[1])}, b:{formatar_numero(reg[2])}, c:{formatar_numero(reg[3])}"
                                
                                rest_txt = reg[4].replace('\n', ' ')
                                print(f"| {dt_h:^19} | {tipo_txt:^4} | {coefs:<22} | {rest_txt:<22} |")
                            print(f"|{'-'*21}-{'-'*6}-{'-'*24}-{'-'*24}|")
                        input('Pressione [ENTER] para voltar ao menu...')
                        continue
                                                    
                    elif escolha == '4':
                        limpar_tela()
                        titulo('LIMPAR HISTÓRICO DE EXPRESSÕES')

                        while True:
                            certeza = input('Apagar todo o histórico de equações? (s/n): ').strip().lower()
                            if certeza in ('s', 'n'):
                                break
                            linha()
                            print('\033[1;31mERRO: Digite apenas S ou N.\033[m')
                            linha()

                        linha()
                        if certeza == 's':
                            conn = sqlite3.connect(caminho_do_banco)
                            cursor = conn.cursor()
                            cursor.execute('DELETE FROM historico_expressoes')
                            conn.commit()
                            conn.close()
                            print('\033[1;32mHistórico de Expressões Limpo com Sucesso!\033[m')
                            linha()
                        else:
                            print('\033[1;33mOperação Cancelada.\033[m')
                            linha()
                        
                        input('Pressione [ENTER] para voltar ao menu...')
                        continue
                    
                    elif escolha == '5':
                        break
                    else:
                        print('\033[1;31mERRO! Opção inválida. Tente Novamente...\033[m')
                        linha()
                        sleep(2)
           
                except (ValueError):
                    print()
                    print('\033[1;31mERRO: Digite apenas um número válido do menu...\033[m')
                    input('Pressione [ENTER] para tentar novamente...')
            
        elif acao == '3':
            limpar_tela()
            conn = sqlite3.connect(caminho_do_banco)
            cursor = conn.cursor()
            cursor.execute('SELECT num1, operacao, num2, resultado, data_hora FROM historico')
            linhas = cursor.fetchall()
            conn.close()
            print(f"|{'-'*19}---{'-'*20}|")
            print('HISTÓRICO DE CÁLCULOS'.center(44))
            if not linhas:
                print(f"|{'-'*19}---{'-'*20}|")
                print()
                print('Nenhum registro de cálculos encontrado.')
                print('-' * 44)
            else:
                print(f"|{'-'*19}---{'-'*20}|")
                print(f"|{'DATA / HORA':^19} | {'OPERAÇÃO':^20}|")
                print(f"|{'-'*19}-+-{'-'*20}|")
                for reg in linhas:
                    n1_h = formatar_numero(reg[0])
                    op_h = reg[1]
                    n2_h = formatar_numero(reg[2])
                    res_h = formatar_numero(reg[3])
                    dt_h = reg[4] if reg[4] is not None else 'Sem Data'
                    conta = f"{n1_h} {op_h} {n2_h} = {res_h}"
                    print(f"|{dt_h:^19} | {conta:<20}|")
                print(f"|{'-'*19}---{'-'*20}|")
            input('Pressione [ENTER] para voltar ao menu...')
        
        elif acao == '4':
            limpar_tela()
            titulo('LIMPAR HISTÓRICO DE CALCULOS')

            while True:
                certeza = input('Apagar todo o histórico definitivamente? (s/n): ').strip().lower()
                if certeza in ('s', 'n'):
                    break
                linha()
                print('\033[1;31mERRO: Digite apenas S ou N.\033[m')
                linha()

            linha()
            if certeza == 's':
                conn = sqlite3.connect(caminho_do_banco)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM historico')
                total = 0.0
                cursor.execute('UPDATE resultado_acumulado SET acumulador = ? WHERE id = 1', (total,))
                conn.commit()
                conn.close()
                print('\033[1;32mHistórico limpo!\033[m')
                linha()
            else:
                print('\033[1;33mOperação Cancelada.\033[m')
                linha()
            input('Pressione [ENTER] para voltar ao menu...')
        
        elif acao == '5':
            print('\033[1;32mSaindo...\033[m')
            sleep(1)
            print('\033[1;32mFINALIZADO!!!\033[m')
            break
        
        else:
            print('\033[1;31mERRO! Opção inválida, Tente Novamente!\033[m')
            linha()
            sleep(2)
    
    except (KeyboardInterrupt):
            print('\033[1;31mOperação cancelada pelo usúario.\033[m')
            sleep(2)
