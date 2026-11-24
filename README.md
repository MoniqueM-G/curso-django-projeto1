Projeto em Django que utiliza suporte a processamento assíncrono de tarefas com Celery. Resgata aleatoriamente receitas de uma API. Atualiza as receitas da tela inicial toda vez que a página inicial é acessada.

Ao dar clone no projeto, é necessário criar um novo ambiente virtual, para instalar as dependências e rodar o projeto

P/ criar o ambiente:

python -m venv env

P/ ativar:

./env/Scripts/activate

Após ativar o ambiente, é necessário baixar as dependências, através do documento "requirements.txt"

pip install -r requirements.txt

**continua ainda

Terminal 1 — Servidor Django:

python manage.py runserver

Acesse no navegador: http://127.0.0.1:8000/

Terminal 2 — Worker do Celery:

celery -A projeto worker -l info --pool=solo

