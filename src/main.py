"""Módulo principal (orquestrador) da Calculadora Inteligente."""

from banco import (
    atualizar_acumulador,
    buscar_historico_aritmetico,
    buscar_historico_expressoes,
    inicializar_banco,
    limpar_historico_aritmetico,
    limpar_historico_expressoes,
    salvar_operacao,
)
from funcoes import bhaskara, primeiro_grau
from time import sleep
from utils import (
    formatar_numero,
    ler_coeficiente,
    limpar_tela,
    linha,
    titulo,
)

total = inicializar_banco()
sinais_permitidos = ['+', '-', '*', '/', '%']

while True:
    try:
        limpar_tela()
        titulo('CALCULADORA INTELIGENTE')
        print('\033[1;34mMENU:\033[m')
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
                if entrada_n1 == 'm':
                    break
                try:
                    resultado_parcial = float(entrada_n1.replace(',', '.'))
                    break
                except ValueError:
                    linha()
                    print('\033[1;31mERRO: Por favor, digite apenas números válidos.\033[m')
                    linha()

            if entrada_n1 == 'm':    
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
                    atualizar_acumulador(total)
                    
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
                    
                salvar_operacao(resultado_parcial, op, n2, prox_resultado)
                    
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
                        print(f"\033[1;34m{'HISTÓRICO DE EXPRESSÕES'.center(80)}\033[m")
                    
                        linhas = buscar_historico_expressoes()

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
                                tipo_txt = '1ºG' if reg[0].lower() == '1° grau' else '2ºG'
                                dt_h = reg[5] if reg[5] is not None else 'Sem Data'
                        
                                if reg[3] is None:
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
                            limpar_historico_expressoes()
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
                        print()
                        print('\033[1;31mERRO! Opção inválida. Tente Novamente...\033[m')
                        linha()
                        sleep(2)
                               
                except (ValueError):
                    print()
                    print('\033[1;31mERRO: Digite apenas um número válido do menu...\033[m')
                    input('Pressione [ENTER] para tentar novamente...')

        elif acao == '3':
            limpar_tela()
            linhas = buscar_historico_aritmetico()
            print(f"|{'-'*19}---{'-'*20}|")
            print(f"\033[1;34m{'HISTÓRICO DE CÁLCULOS'.center(44)}\033[m")
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
                limpar_historico_aritmetico()
                total = 0.0
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