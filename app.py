from flask import Flask
from flask_login import LoginManager, current_user
from extensions import db
from routes import routes
from models import Usuario  # modelo do usuário autenticado

app = Flask(__name__)
app.secret_key = 'alguma-chave-secreta'

# ✅ Configurações
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Inicializa banco de dados
db.init_app(app)

# ✅ Inicializa Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'routes.login'  # rota de login personalizada

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ✅ Injeta current_user nos templates Jinja
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# ✅ Registra Blueprints
app.register_blueprint(routes)

# ✅ Inicializa aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
