# Project MarketPlace 
Projeto envolvendo a integração de uma tela de produtos em Vue js com uma API de produto em Django Rest e Banco Postgresql

## Configurando do Ambiente

Siga os passos abaixo para conseguir utilizar o sistema

### Clonar o repositório
1. git clone https://github.com/joseeusebio/project_marketplace.git

### Criação de um Virtual Enviroment
1. python -m venv .venv
2. Unix ou MacOs - source .venv/Scripts/Activate
3. Windows - venv\Scripts\activate

### Criação de um arquivo .env para incluir as variáveis de ambiente.
1. Dentro da pasta dotenv_files crie um novo arquivo (mkdir .env) e utilize o modelo de exemplo .env-example para preencher as variáveis de ambiente necessárias.

2. Dentro da pasta frontend crie também um arquivo .env e ponha a seguinte propiedade: VUE_APP_API_BASE_URL = "link do localhost onde está sendo executada a API", essa propiedade é necessária para que a página consiga renderizar as imagens.

### Iniciando o build do container docker
 1. Após a criação do arquivo .env execute o comando docker-compose up --build no console na raiz do projeto e aguarde a criação dos containners.

### Criação do superuser para utilizar os endpoints da API
1. Após a criação dos containners execute o seguinte comando no shell do docker djangoapi (python manage.py createsuperuser) esse usuário será importante para acessar a página de administração do django para criar novos usuários ou então utiliza-lo para acessar os endpoints.

### Criação de Produto para popular a tela
1. Após subir os containers e criar o superuser você deve acessar o link http://localhost:8000/admin/ e logar com o usuário que foi criado, na tela de administrado do django você poderá criar todos os recursos necessários para popular a página web, entretanto se desejar poderá criar através dos endpoints disponíveis na documentação.

2. A tela principal estará disponível através do link http://localhost:8080/

### Acessar a documentação da API
1. Para acessar a documentação da API basta acessar os links  http://localhost:8000/swagger/ ou http://localhost:8000/redoc/ após subir aplicação.
 



