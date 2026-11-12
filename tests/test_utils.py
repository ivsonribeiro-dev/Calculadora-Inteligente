"""Testes automatizados para o módulo de utilitários e formatação (src/utils.py)."""

import os
import sys
import unittest

# Adiciona a pasta src/ ao caminho do python para permitir os imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils import formatar_equacao, formatar_numero, formatar_resultado

class TestUtils(unittest.TestCase):
    """Conjunto de testes para validação de strings, números e frações."""


    def test_formatar_numero(self):
        self.assertEqual(formatar_numero(10.0), '10')
        self.assertEqual(formatar_numero(3.75), '3.75')
        self.assertEqual(formatar_numero(None), '-')


    def test_formatar_equacao(self):
        self.assertEqual(formatar_equacao(5), '5')
        self.assertEqual(formatar_equacao(-4), '(-4)')


    def test_formatar_resultado_fracoes(self):
        self.assertEqual(formatar_resultado(0.5), '¹/₂')
        self.assertEqual(formatar_resultado(-0.25), '-¹/₄')
        self.assertEqual(formatar_resultado(4.0), '4')


if __name__ == '__main__':
    unittest.main()
