"""Testes automatizados para as regras matemáticas (src/funcoes.py)."""

import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from funcoes import bhaskara, primeiro_grau


class TestFuncoesMatematicas(unittest.TestCase):
    """Testa equações do 1° e 2° grau sem sujar o banco de dados real."""


    @patch('funcoes.salvar_expressao')
    # 2x - 4 = 0 -> x = 2
    def test_primeiro_grau_simples(self, mock_salvar):
        resultado = primeiro_grau(2, -4)
        self.assertIn('2', resultado)
        mock_salvar.assert_called_once()


    @patch('funcoes.salvar_expressao')
    # x² - 5x + 6 = 0 -> x1 = 3, x2 = 2
    def test_bhaskara_duas_raizes(self, mock_salvar):
        resultado = bhaskara(1, -5, 6)
        self.assertIn('3', resultado)
        self.assertIn('2', resultado)
        mock_salvar.assert_called_once()


    @patch('funcoes.salvar_expressao')
    # x² + 2x + 5 = 0 -> delta = -16 (raízes complexas)
    def test_bhaskara_delta_negativo(self, mock_salvar):
        resultado = bhaskara(1, 2, 5)
        self.assertIsNotNone(resultado)
        mock_salvar.assert_called_once()


if __name__ == '__main__':
    unittest.main()
