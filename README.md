# Serverless com Flask e spaCy

### Visão Geral

Este projeto é uma aplicação serverless desenvolvida com Flask, uma framework web em Python, projetada para facilitar a criação de APIs robustas e escaláveis. Integrada com spaCy para processamento avançado de linguagem natural, esta aplicação é ideal para analisar e processar dados de texto, oferecendo funcionalidades como agrupamento de dados baseados em características linguísticas.

### Principais Funcionalidades

- **API RESTful:** Interface para interação programática com funcionalidades do backend.

- **Processamento de Linguagem Natural:** Utiliza spaCy para realizar tarefas complexas de processamento de texto.

- **Cross-Origin Resource Sharing (CORS):** Configurado para aceitar requisições cross-origin, facilitando a integração com frontends em diferentes domínios.

### Tecnologias Utilizadas

- **Flask:** Framework web leve que serve como espinha dorsal da nossa API.

- **Flask-Cors:** Módulo para lidar com as questões de segurança associadas ao CORS.

- **spaCy:** Biblioteca avançada para processamento de linguagem natural.

- **numpy:** Utilizado para manipulações numéricas, especialmente útil em operações de processamento de linguagem.

### Dependências

Assegure-se de instalar todas as dependências necessárias para executar o projeto localmente. Você pode instalar todas as dependências utilizando o seguinte comando:

```bash

pip install -r requirements.txt

```

A lista completa de dependências está disponível no arquivo `requirements.txt`.

### Configuração Local

Para configurar e rodar a aplicação localmente, siga estes passos:

1. Clone o repositório para sua máquina local.

2. Instale as dependências usando o comando `pip install -r requirements.txt`.

3. Defina a variável de ambiente `FLASK_APP` para `app.py`.

4. Inicie o servidor Flask utilizando o comando:

```bash

flask run

```

Isso iniciará o servidor na porta padrão 5000, e você poderá acessar a API através de `http://localhost:5000/`.

### Rotas da API

A aplicação define as seguintes rotas para interação com o sistema:

- `/api/*`: Rota genérica para tratar requisições da API.

- `/cluster`: Especificamente destinada a funcionalidades de agrupamento de tickets ou dados de texto.

## Licença

Consulte o arquivo `LICENSE` para detalhes sobre os termos de uso e distribuição do software.