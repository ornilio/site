from app import app                 # importa o app Flask principal
from extensions import db           # importa a instância do banco (caso esteja separada)
from models import Usuario          # importa o modelo de usuário

# Criação dentro do contexto da aplicação
with app.app_context():
    # Cria novo usuário com username e senha
    novo_user = Usuario(username='admin', password='179325')
    
    # Adiciona e salva no banco
    db.session.add(novo_user)
    db.session.commit()

    print(f"Usuário {novo_user.username} criado com sucesso!")
