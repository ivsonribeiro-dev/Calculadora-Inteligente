"""Testes automatizados para a camada de persistência em SQLite3 (src/banco.py)."""

import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import banco


class TestBancoDados(unittest.TestCase):
    """Testa criação de tabelas, gravação, busca e limpeza em banco temporário."""


    def setUp(self):
        """Executado ANTES de cada teste: cria um caminho de banco isolado."""
        self.banco_teste = os.path.join(os.path.dirname(__file__), 'temp.teste.db')
        self.patcher = patch('banco.caminho_do_banco', self.banco_teste)
        self.patcher.start()
        banco.inicializar_banco()


    def tearDown(self):
        """Executado DEPOIS de cada teste: desfaz o patch e apaga o banco temporário."""
        self.patcher.stop()
        if os.path.exists(self.banco_teste):
            os.remove(self.banco_teste)


    def test_salvar_e_buscar_operacao_aritmetica(self):
        banco.salvar_operacao(10, '+', 5, 15)
        registros = banco.buscar_historico_aritmetico()

        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0][0], 10)
        self.assertEqual(registros[0][1], '+')
        self.assertEqual(registros[0][2], 5)
        self.assertEqual(registros[0][3], 15)


    def test_limpar_historico_aritmetico_zera_acumulador(self):
        banco.salvar_operacao(20, '*', 2, 40)
        banco.atualizar_acumulador(40.0)
        banco.limpar_historico_aritmetico()

        registros = banco.buscar_historico_aritmetico()
        self.assertEqual(len(registros), 0)


    def test_salvar_e_buscar_expressao_primeiro_grau(self):
        banco.salvar_expressao('1° grau', 2, -4, None, 'x = 2')
        expressoes = banco.buscar_historico_expressoes()

        self.assertEqual(len(expressoes), 1)
        self.assertEqual(expressoes[0][0], '1° grau')
        self.assertEqual(expressoes[0][1], 2)
        self.assertEqual(expressoes[0][2], -4)
        self.assertEqual(expressoes[0][3], None)
        self.assertEqual(expressoes[0][4], 'x = 2')


    def test_salvar_e_buscar_expressao_segundo_grau(self):
        banco.salvar_expressao('2° grau', 1, -5, 6, 'x¹ = 3 | x² = 2')
        expressoes = banco.buscar_historico_expressoes()

        self.assertEqual(len(expressoes), 1)
        self.assertEqual(expressoes[0][0], '2° grau')
        self.assertEqual(expressoes[0][1], 1)
        self.assertEqual(expressoes[0][2], -5)
        self.assertEqual(expressoes[0][3], 6)
        self.assertEqual(expressoes[0][4], 'x¹ = 3 | x² = 2')


    def test_limpar_historico_expressoes(self):
        banco.salvar_expressao('1° grau', 2, -4, None, 'x = 2')
        banco.salvar_expressao('2° grau', 1, -5, 6, 'x¹ = 3 | x² = 2')
        banco.limpar_historico_expressoes()

        expressoes = banco.buscar_historico_expressoes()
        self.assertEqual(len(expressoes), 0)


if __name__ == '__main__':
    unittest.main()
