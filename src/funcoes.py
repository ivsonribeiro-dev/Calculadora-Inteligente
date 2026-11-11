"""Módulo contendo as regras de negócio e cálculos das equações do 1° e 2° grau."""

import cmath
from banco import salvar_expressao
from time import sleep
from utils import formatar_equacao, formatar_resultado, linha


def bhaskara(coef_a, coef_b, coef_c):
    '''Calcula as raízes reais ou complexas de uma equação do 2º grau.'''
    if coef_a == 0:
        return ("\033[1;31mO coeficiente 'a' não pode ser igual a zero.\033[m")

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
    sleep(2)
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
        salvar_expressao('2° grau', coef_a, coef_b, coef_c, txt_res_banco)
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
        print('\033[1;31mO coeficiente "a" não pode ser igual a zero.\033[m')
        return

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
    txt_res_banco = f"x = {formatar_resultado(resultado_x)}"

    try:
        salvar_expressao('1° grau', coef_a, coef_b, None, txt_res_banco)
    except Exception as erro_banco:
        print(f"\n\033[1;31mAviso: Não foi possível salvar no histórico.({erro_banco})\033[m")
        linha()

    return (f'Resultado Final: \nx = {formatar_resultado(resultado_x)}')
