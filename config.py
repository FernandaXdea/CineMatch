import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:ourlastnight@localhost/cinematch_db'
    SECRET_KEY = os.urandom(24)  # Gera uma chave aleatória
    API_KEY_TRAKT = 'f926e2d7eb07250ab684a5424c587976455cc948a8e976a517f3ace63793b36a'
