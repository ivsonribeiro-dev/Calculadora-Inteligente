# Projeto Calculadora Inteligente Python

Este é um ecossistema completo de calculadora desenvolvido em python, focado no estudo de arquitetura modular, persistência de dados, tratamento de exceções e consumo de APIs REST de mercado.

O projeto foi iniciado originalmente no ambiente mobile (Pydroid3) e migrado para ambiente desktop (Linux Mint XFCE), servindo como portifólio prático de engenharia de software e boas práticas de desenvolvimento.

## Engenharia de Software e Desenvolvimento Incremental (Roadmap)

Para simular o ciclo de vida de um produto de software no mercado de trabalho, o projeto foi estruturado de forma incremental, registrando a evolução da maturidade do código através de marcos históricos:

### [CONCLUÍDO] Marco Zero: Versão 1 (`Versao_1/`)
* **Status:** Entregue e consolidada no GitHub.
* **Descrição:** Validação Inicial de Lógica matemática e fluxo de controle. Execução das operações aritméticas básicas rodando de forma linear diretamente no terminal, tratando a persistência de dados iniciais localmente, com um banco de dados simples, SQLite3 em fase inicial.

### [CONCLUÍDO] Versão 2 (`Versao_2/`): Álgebra, Equações e Persistência Isolada
* **Melhorias Aplicadas:**
  * **Banco de Dados:** Integração estruturada com `SQLite3` (Armazenamento persistente de acumuladores globais e tabelas de logs históricos, com datas e horários atualizados e bem estruturados).
  * **Tratamento de Exceções:** Tratamento defensivo de entradas e Implementação robusta de blocos `try/except` para blindagem contra quebras de tipo (`ValueError`, `TypeError`) e interrupções manuais do sistema (`KeyboardInterrupt`).
  * **Caminhos Dinâmicos:** Uso do escopo global do módulo `os` (`__file__`) para garantir portabilidade multiplataforma automática do banco de dados.
  * **Códigos:** Refatoração e manutenção dos códigos para melhor visibilidade e compreendimento, seguindo as normas de código limpo (`Clean Code`).

### [CONCLUÍDO] Script Auxiliar Integrado: Equações e Bhaskara
* **Descrição:** Acoplamento de um resolvedor avançado de equações de primeiro e segundo grau. Sendo capaz de tratar raízes complexas no conjunto dos números imaginários (`cmath`) e renderizar dízimas e dízimas periódicas no formato estético de frações reais através de caracteres sobrescritos e subscritos personalizados (`fractions`).

### [CONCLUÍDO] Refatoração Arquitetural e Modularização (`src/`)
* **Descrição:** Desmonte do arquivo monolítico de mais de 600 linhas da Versão 2 para adoção do **Princípio da Responsabilidade única (SOLID)**. O código foi fatiado em módulos limpos de baixa dependência:
  * `main.py`: Orquestração de entrada, rotas e menus (menos de 400 linhas).
  * `banco.py`: Encapsulamento completo de conexões, queries SQL e transações em banco.
  * `funcoes.py`: Isolamento puro das regras de cálculo aritmético e Bhaskara.
  * `utils.py`: Abstração de ferramentas visuais, limpeza nativa de tela (`subprocess.run`) e tratamento de strings.

### [PLANEJADO] Versão 3 (`Versao_3/`): Integração Web e Consumo de APIs web
* **Status:** Aguardando início da implementação; arquitetura modular (src/) já concluída e preparada para receber os endpoints.
* **Descrição:** Evolução para consumo de microsserviços online utilizando requisições HTTP (`requests`). Integração com a *AwesomeAPI* para conversão de moedas mundiais (Real, Dólar, Euro, Bitcoin) em tempo real, gravando o histórico de cotações diretamente no banco de dados.

## Tecnologias e Recursos Globais do Projeto
* **Python 3** (Linguagem Principal de Desenvolvimento)
* **SQLite3** (Mecanismo de Banco de Dados Relacional Embarcado)
* **Módulos Nativos:** `os`, `sys`, `subprocess`, `time`, `cmath`, `datetime`, `fractions`
* **Gerenciamento de Pacotes:** `pip` e isolamento de dependências via `requirements.txt`

## Como Executar a Versão atual (src/)
Certifique-se de estar com o terminal aberto na raiz do projeto e execute:
```bash
python3 "src/main.py"
```

## Testes Automatizados (`tests/`)
O projeto conta com uma suíte de testes unitários construída com a biblioteca nativa `unittest` e `unittest.mock`, garantindo a integridade matemática e o isolamento do banco de dados:
* **`tests/test_utils.py`:** Valida formatações númericas, parênteses de sinais e conversão para frações Unicode.
* **`tests/test_funcoes.py`:** Testa equações do 1° e 2° grau (incluindo raízes complexas) isolando o banco via *mock*.
* **`tests/test_banco.py`:** Verifica criação de tabelas, gravação, consulta e limpeza de históricos em banco temporário isolado.

### Como executar os testes:
```bash
python3 -m unittest discover -s tests -t . -v
```