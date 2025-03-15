from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Inicialize o app e o banco de dados
app = Flask(__name__)

# Defina a URI do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:senha@localhost/cinematch_db'  # Substitua 'senha' pela sua senha
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração de chave secreta
app.config['SECRET_KEY'] = os.urandom(24)

# Inicialize o banco de dados
db = SQLAlchemy(app)

# Configuração do login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Defina o modelo de Usuário
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Função para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rota da página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        # Verificar se o usuário existe e se a senha está correta
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
    return render_template('login.html')


# Rota de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='sha256')

        # Verificar se o usuário já existe
        if User.query.filter_by(email=email).first():
            flash('Email já registrado. Tente outro email.', 'error')
            return redirect(url_for('register'))

        # Criação do novo usuário
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Cadastro bem-sucedido! Agora, faça login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


# Rota de recomendações de filmes
@app.route('/home')
@login_required
def home():
    # Aqui você passaria uma lista de filmes para a página
    movies = [
        {'id': 1, 'title': 'Filme A', 'genre': 'Ação'},
        {'id': 2, 'title': 'Filme B', 'genre': 'Comédia'},
        {'id': 3, 'title': 'Filme C', 'genre': 'Drama'}
    ]
    return render_template('home.html', movies=movies)


# Rota de detalhes do filme
@app.route('/movie/<int:movie_id>')
@login_required
def movie_detail(movie_id):
    # Aqui você recuperaria detalhes de um filme a partir do banco de dados
    movie = {'id': movie_id, 'title': f'Filme {movie_id}', 'genre': 'Ação', 'description': 'Descrição do filme'}
    return render_template('movie_detail.html', movie=movie)


# Rota de perfil do usuário
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
