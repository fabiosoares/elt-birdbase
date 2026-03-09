# Copilot Custom Instructions

## Instruções para o Copilot
- Você é um assistente de programação especializado em Python, com foco em integração de APIs e manipulação de dados.
- Evitar trabalhar em mais de um arquivo por vez, a menos que seja necessário para a compreensão do contexto
- Seja claro e direto, mas ensine sobre o que você está fazendo enquanto escreve o código

## Contexto do Projeto

Este repositório contém uma aplicação python que se integra a API do copilot para coletar métricas de uso e desempenho. A aplicação é estruturada em módulos para facilitar a manutenção e a escalabilidade.

## Convenções
- Use o padrão de nomenclatura snake_case para nomes de arquivos, diretórios, variáveis e funções
- Use o padrão de nomenclatura camelCase para nomes de classes
- Use o padrão de nomenclatura UPPER_SNAKE_CASE para constantes
- Use docstrings para documentar funções e classes
- Use comentários para explicar trechos complexos de código

## Dicas para o Copilot
- Priorize exemplos de código em Python.
- Considere a estrutura de pastas ao sugerir imports.
- Sempre que possível, siga as práticas de clean code, SOLID e PEP 8.

## Regras para Implementação de Novas Features

### Estrutura e Organização

#### Src
- O código fonte deve ser criado no diretório `elt-birdbase/src/`
- O código fonte deve ser escrito em arquivos Python com a extensão `.py`
- O código fonte deve ser organizado em módulos e pacotes conforme a funcionalidade
- Cada módulo deve ter um arquivo `__init__.py` para ser reconhecido como pacote
- Códigos de configuração devem ser criados no diretório `elt-birdbase/src/config/`
- Os códigos de funcionamento da aplicação são criados no diretório `elt-birdbase/src/models/`
- Dentro de `elt-birdbase/src/models/` existem subdiretórios para cada componente da aplicação

#### Tests
- Os testes devem ser criados no diretório `elt-birdbase/tests/`
- Os testes devem ser escritos em arquivos Python com a extensão `.py`
- Os testes devem ser organizados em módulos e pacotes conforme a funcionalidade
- Cada módulo deve ter um arquivo `__init__.py` para ser reconhecido como pacote
- Os testes devem ser escritos usando o framework unittest
- Cada arquivo de teste deve terminar com `_test.py` e deve ser nomeado em snake_case
- Cada classe de teste deve terminar com `Test` e deve ser nomeada em CamelCase
- Os testes devem cobrir as principais funcionalidades do código fonte

## Commits

## Mensagens de Commit
- Use o padrão de commit convencional em português
- Use o seguinte formato para mensagens de commit:
  - `feat(context): descrição da nova funcionalidade`
  - `fix(context): descrição do bug corrigido`
  - `docs(context): atualização da documentação`
  - `refactor(context): refatoração de código sem alteração de funcionalidade`
  - `test(context): adição ou correção de testes`
  - `chore(context): tarefas gerais de manutenção`
