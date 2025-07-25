from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models import Usuario, Produto
from extensions import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user


routes = Blueprint('routes', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Página inicial
@routes.route('/')
def homepage():
    produtos_destaque = Produto.query.filter_by(destaque=True).all()
    ofertas_extras = Produto.query.filter_by(destaque=False).all()
    return render_template('index.html', produtos_destaque=produtos_destaque, ofertas_extras=ofertas_extras)

# Login
@routes.route('/login')
def login_page():
    return render_template('login.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['password']

        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and usuario.check_password(senha):
            login_user(usuario)  # ✅ ESSENCIAL
            flash('Login realizado com sucesso!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('routes.dashboard'))
        else:
            flash('Usuário ou senha inválidos.', 'error')

    return render_template('login.html')

# Painel administrativo
@routes.route('/dashboard')
@login_required
def dashboard():
    produtos_destaque = Produto.query.filter_by(destaque=True).all()
    ofertas_extras = Produto.query.filter_by(destaque=False).all()
    return render_template('dashboard.html', produtos_destaque=produtos_destaque, ofertas_extras=ofertas_extras)

# Logout
@routes.route('/logout')
def logout():
    logout_user()
    flash('Você saiu com sucesso.', 'info')
    return redirect(url_for('routes.login_page'))
# Formulário de novo produto
@routes.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
def novo_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        destaque = 'destaque' in request.form

        imagem_file = request.files.get('imagem_file')
        if imagem_file and imagem_file.filename != '':
            filename = secure_filename(imagem_file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            imagem_path = os.path.join(upload_folder, filename)
            imagem_file.save(imagem_path)
            imagem_url = url_for('static', filename='uploads/' + filename)
        else:
            imagem_url = None

        novo = Produto(nome=nome, descricao=descricao, imagem_url=imagem_url, destaque=destaque)
        db.session.add(novo)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('routes.dashboard'))

    return render_template('novo_produto.html')

# Edição de produto
@routes.route('/produtos/editar/<int:id>', methods=['GET'])
@login_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    return render_template('editar_produto.html', produto=produto)

@routes.route('/produtos/editar/<int:id>', methods=['POST'])
@login_required
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    produto.nome = request.form['nome']
    produto.descricao = request.form['descricao']
    produto.destaque = 'destaque' in request.form

    imagem_file = request.files.get('imagem_file')
    if imagem_file and imagem_file.filename != '':
        filename = secure_filename(imagem_file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        imagem_path = os.path.join(upload_folder, filename)
        imagem_file.save(imagem_path)
        produto.imagem_url = url_for('static', filename='uploads/' + filename)
    else:
        imagem_url = request.form.get('imagem_url')
        produto.imagem_url = imagem_url

    db.session.commit()
    flash('Produto atualizado com sucesso!', 'success')
    return redirect(url_for('routes.dashboard'))
