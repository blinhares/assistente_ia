
<p align="center"><img src="https://img.shields.io/badge/Blinhares-white?logo=github&logoColor=181717&style=for-the-badge&label=git" /><p align="center">

# Titulo

Este projeto tem o intuito de dar acesso facil a um tecnologia que esta cada vez mais solicitada.
Encontra-se muito conteudo na internet utilizando OpenAI e chaves de API, mas nesse projeto, vamos te dar independencia total!

Aqui voce vai aprender a rodar uma inteligencia artificial de forma totalmente local, personaliza-la (ainda preparando essa parte) e conversar com arquivos! Isso mesmo! Voce sera capaz de ter um 'chatGPT' no seu computador e um 'analisador' de arquivos inteiramente `GRATIS`!

## Pre-Requisitos

- Python. [Ir para Site](https://www.python.org/)
- Ollama. [Ir para Site](https://ollama.com/)

## Ferramentas Utilizadas

[![langchain](https://python.langchain.com/v0.2/img/brand/wordmark-dark.png)](https://python.langchain.com/v0.2/docs/introduction/)
[![Ollama](https://ollama.com/public/ollama.png)](https://ollama.com/)

## Utilização

### Clonando Repositório

```bash
git clone <endereco git>
```

### Dependências

Existem algumas dependências necessárias para rodar o projeto, e vamos resolver isso facilmente com a instalação do poetry. Poetry é uma ferramenta interessante e recomendo conhece-la caso não tenha familiaridade.

```bash
pip install poetry
```

Acesse a pasta onde o repositório foi clonado. Estando na mesma pasta em que os arquivos `poetry.lock e pyproject.toml` execute o comando:

```bash
poetry install
```

Pronto, ambiente virtual criado e dependências instaladas.

### Executando

Deixei o script o mais facil possivel para utilizacao. Esta tudo devidamente configurado e todas as configuracoes podem sem encontradas em `src/config.py`.
Configurei os parametros com base nos melhores resultados que encontrei em meus teste mas sinta-se livre pra alterar como bem entender.

Para rodar o programa, basta executar o arquivo main.py, que, por linha de comando pode ser executado assim:

```bash
python main.py
```

Para conversar com algum arquivo, basta colocar os arquivos dos quais deseja ler dentro da pasta `source_documents`. Caso essa pasta não exista, ela sera criada logo que voce executar o programa pela primeira vez. Depois de inserir os arquivos na pasta, basta executar o programa e selecionar a opção correspondente.

