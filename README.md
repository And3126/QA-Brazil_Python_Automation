# Urban Routes: Automação de Testes E2E

Testes automatizados do fluxo de pedido de táxi de um aplicativo web.

## Objetivo

Automatizar o fluxo completo de pedido de táxi do Urban Routes, para validar as principais funcionalidades de ponta a ponta e poder repetir os testes sempre que o aplicativo mudar.

## Resultado

* Fluxo completo automatizado: rota, plano Comfort, telefone com código de confirmação por SMS, cartão, comentário para o motorista, cobertor e lenços, 2 sorvetes e pedido do táxi.
* Código organizado com Page Object Model: testes, localizadores, dados de teste e funções auxiliares em módulos separados.
* Testes independentes entre si: cada um abre a página do zero.
* Esperas explícitas centralizadas em métodos privados do Page Object.

## Ferramentas utilizadas

Python, Selenium WebDriver, Pytest, Page Object Model, Git e GitHub.

## O que aprendi

* Estruturar um projeto de automação com Page Object Model.
* Escrever testes independentes, que não dependem da ordem de execução.
* Usar esperas explícitas do Selenium em vez de pausas fixas.
* Organizar e executar testes com Pytest.

## Melhorias possíveis

* Gerar um relatório HTML dos testes com `pytest-html`.
* Rodar os testes automaticamente com GitHub Actions.
* Cobrir cenários negativos, como telefone ou cartão inválidos.

## Estrutura do projeto

* `main.py`: casos de teste
* `pages.py`: Page Object (localizadores e ações)
* `data.py`: dados de teste
* `helpers.py`: funções auxiliares

## Como executar

```bash
pip install -r requirements.txt
pytest main.py
```
