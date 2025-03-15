import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:ourlastnight@localhost/cinematch_db'
    SECRET_KEY = os.urandom(24)  # Gera uma chave aleatória
    API_KEY_TMDB = 'sua_api_key'
