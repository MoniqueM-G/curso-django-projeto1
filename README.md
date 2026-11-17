Projeto em Django que utiliza suporte a processamento assíncrono de tarefas com Celery. Resgata aleatoriamente receitas de uma API. Atualiza as receitas da tela inicial toda vez que a página inicial é acessada.

Terminal 1 — Servidor Django:

python manage.py runserver

Acesse no navegador: http://127.0.0.1:8000/

Terminal 2 — Worker do Celery:

celery -A projeto worker -l info --pool=solo


