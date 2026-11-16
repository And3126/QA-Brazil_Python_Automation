# Urban Routes: Automação de Testes E2E

Testes automatizados do fluxo de pedido de táxi de um aplicativo web,
feitos com Python, Selenium e Pytest.

## Tecnologias
- Python
- Selenium WebDriver
- Pytest
- Page Object Model (POM)

## O que é testado
- Definir a rota e escolher o plano Comfort
- Cadastrar telefone com código de confirmação por SMS
- Adicionar cartão de crédito
- Comentário, cobertor, lenços e sorvetes
- Pedir o táxi

## Estrutura do projeto
- main.py: casos de teste
- pages.py: Page Object (localizadores e ações)
- data.py: dados de teste
- helpers.py: funções auxiliares

## Como rodar
pip install -r requirements.txt
pytest main.py
