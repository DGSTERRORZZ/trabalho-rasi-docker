import os
import time
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template_string

app = Flask(__name__)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "meu_banco"),
    "user": os.getenv("DB_USER", "flaskuser"),
    "password": os.getenv("DB_PASSWORD", ""),
}

def conectar_banco():
    ultimo_erro = None
    for tentativa in range(10):
        try:
            return mysql.connector.connect(**DB_CONFIG, connection_timeout=5)
        except Error as erro:
            ultimo_erro = erro
            time.sleep(2)
    raise ultimo_erro

ESTILO = """
<style>
body{font-family:Arial,sans-serif;background:#f2f5f9;color:#1e293b;margin:0}
header{background:#12345a;color:white;padding:28px 8%}
main{max-width:900px;margin:35px auto;background:white;padding:30px;border-radius:12px;box-shadow:0 4px 18px #0001}
nav a{color:#dbeafe;margin-right:18px;font-weight:bold;text-decoration:none}
h1{color:#12345a}.tag{display:inline-block;background:#e0f2fe;padding:8px 12px;border-radius:20px}
li{padding:7px 0}footer{text-align:center;color:#64748b;padding:25px}
</style>
"""

def pagina(titulo, conteudo):
    return render_template_string("""
    <!doctype html><html lang="pt-br"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ titulo }}</title>{{ estilo|safe }}</head><body>
    <header><h2>Projeto RASI — Docker e Docker Compose</h2>
    <nav><a href="/">Início</a><a href="/sobre">Sobre</a>
    <a href="/contato">Contato</a><a href="/alunos">Alunos</a></nav></header>
    <main>{{ conteudo|safe }}</main><footer>IFSP — Campus Campos do Jordão</footer>
    </body></html>
    """, titulo=titulo, conteudo=conteudo, estilo=ESTILO)

@app.route("/")
def home():
    return pagina("Início | Projeto RASI",
        "<h1>Bem-vindo ao Flask no Docker</h1>"
        "<p>Aplicação web desenvolvida para a disciplina de Redes e Administração de Sistemas.</p>"
        "<p class='tag'>Python 3.14-slim • Flask • MySQL • Apache</p>"
        "<p>Utilize o menu para conhecer o projeto e consultar os alunos cadastrados.</p>")

@app.route("/sobre")
def sobre():
    return pagina("Sobre | Projeto RASI",
        "<h1>Sobre o projeto</h1><p>Este projeto demonstra a containerização de uma aplicação Python Flask "
        "e a integração de serviços independentes por meio do Docker Compose.</p>"
        "<p>A arquitetura utiliza Apache como proxy reverso, Flask na camada de aplicação e MySQL para persistência.</p>")

@app.route("/contato")
def contato():
    return pagina("Contato | Projeto RASI",
        "<h1>Contato institucional</h1><p>Instituto Federal de Educação, Ciência e Tecnologia de São Paulo.</p>"
        "<p>Campus Campos do Jordão — Curso Técnico em Informática Integrado ao Ensino Médio.</p>"
        "<p>Disciplina: Redes e Administração de Sistemas (RASI).</p>")

@app.route("/alunos")
def alunos():
    conexao = None
    cursor = None
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT id, nome FROM alunos ORDER BY id")
        registros = cursor.fetchall()
        linhas = "".join(f"<li>{a['id']} — {a['nome']}</li>" for a in registros)
        if not linhas:
            linhas = "<li>Nenhum aluno cadastrado.</li>"
        return pagina("Alunos | Projeto RASI",
            "<h1>Alunos cadastrados no MySQL</h1><ul>" + linhas + "</ul>"
            "<p>Os dados desta página são consultados diretamente no banco MySQL.</p>")
    except Error as erro:
        return pagina("Erro no banco | Projeto RASI",
            "<h1>Não foi possível consultar o banco</h1><p>Verifique os containers e os logs do serviço Flask.</p>"
            f"<pre>{str(erro)}</pre>"), 503
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
