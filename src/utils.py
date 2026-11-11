'''Módulo de utilitarios visuais, formatação númerica e validação de entradas.'''

import os
import subprocess
from fractions import Fraction


def linha(tam = 80):
    print('-' * tam)


def titulo(txt):
    linha()
    print(f'\033[1;34m{txt.center(80)}\033[m')
    linha()


def limpar_tela():
    comando = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run([comando])


def formatar_numero(valor):
    """Formata o número removendo o .0 caso seja um valor inteiro."""
    if valor is None:
        return '-'
    if float(valor) % 1 == 0:
        return str(int(valor))
    return str(valor)


def formatar_equacao(valor):
    '''Formata o coeficiente retornando um valor sem parênteses caso seja positivo 
    e com parênteses caso seja negativo.'''
    texto = formatar_numero(valor)
    if valor < 0:
        return f'({texto})'
    else:
        return f'{texto}'


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
            print()
            print('\033[1;31mERRO: Por favor, digite apenas números válidos.\033[m')
            linha()
