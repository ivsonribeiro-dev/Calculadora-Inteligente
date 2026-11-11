'''Módulo responsável pela conexão, criação de tabelas, manipulaçao 
e operações no banco SQLite3.'''

import os
import sqlite3
from datetime import datetime


# Define o caminho dinâmico do banco na pasta rais do projeto
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
caminho_do_banco = os.path.join(PASTA_ATUAL, 'calculadorav2.db')


def conectar():
    '''Abre e retorna uma conexão ativa com o banco de dados.'''
    return sqlite3.connect(caminho_do_banco)


def inicializar_banco():
    '''Cria as tabelas necessárias caso ainda não existam e carrega o acumulador.'''
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   num1 REAL,
                   operacao TEXT,
                   num2 REAL,
                   resultado REAL,
                   data_hora TEXT
        )
    ''')

    cursor.execute ('''
        CREATE TABLE IF NOT EXISTS historico_expressoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            coef_a REAL,
            coef_b REAL,
            coef_c REAL,
            resultado TEXT,
            data_hora TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultado_acumulado (
            id INTEGER PRIMARY KEY,
            acumulador REAL
        )
    ''')

    cursor.execute('SELECT acumulador FROM resultado_acumulado WHERE id = 1')
    resultado_banco = cursor.fetchone()
    if resultado_banco is None:
        cursor.execute('INSERT INTO resultado_acumulado (id, acumulador) VALUES (1, 0.0)')
        total_inicial = 0.0
    else:
        total_inicial = resultado_banco[0]

    conn.commit()
    conn.close()
    return total_inicial


# Operações Aritméticas


def salvar_operacao(num1, operacao, num2, resultado):
    '''Registra uma operação básica no histórico com data e hora.'''
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO historico (num1, operacao, num2, resultado, data_hora) VALUES (?, ?, ?, ?, ?)', 
        (num1, operacao, num2, resultado, agora)
    )
    conn.commit()
    conn.close()


def buscar_historico_aritmetico():
    '''Retorna todos os registros do histórico de operações básicas.'''
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT num1, operacao, num2, resultado, data_hora FROM historico')
    linhas = cursor.fetchall()
    conn.close()
    return linhas


def limpar_historico_aritmetico():
    """Apaga o histórico aritmético e zera o acumulador no banco."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM historico')
    cursor.execute('UPDATE resultado_acumulado SET acumulador = 0.0 WHERE id = 1')
    conn.commit()
    conn.close()


def atualizar_acumulador(novo_total):
    """Atualiza o valor do resultado acumulado no banco de dados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('UPDATE resultado_acumulado SET acumulador = ? WHERE id = 1', (novo_total,))
    conn.commit()
    conn.close()


# Operações de Expressões / Equações

def salvar_expressao(tipo, coef_a, coef_b, coef_c, resultado):
    """Registra uma equação do 1° ou 2° grau no histórico separado."""
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO historico_expressoes (tipo, coef_a, coef_b, coef_c, resultado, data_hora) VALUES (?, ?, ?, ?, ?, ?)',
        (tipo, coef_a, coef_b, coef_c, resultado, agora)
    )
    conn.commit()
    conn.close()


def buscar_historico_expressoes():
    """Retorna todos os registros do histórico de equações."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT tipo, coef_a, coef_b, coef_c, resultado, data_hora FROM historico_expressoes')
    linhas = cursor.fetchall()
    conn.close()
    return linhas


def limpar_historico_expressoes():
    """Apaga todos os registros da tabela de equações."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM historico_expressoes')
    conn.commit()
    conn.close()
