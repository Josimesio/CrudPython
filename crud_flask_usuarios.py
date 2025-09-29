from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

# Configurações
APP_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(APP_DIR, 'usuarios.db')

app = Flask(__name__)
app.secret_key = 'troque_esta_chave_em_producao'

# ------------------------
# Banco de dados
# ------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
    ''')
    conn.commit()
    conn.close()

init_db()

# ------------------------
# Rotas
# ------------------------
@app.route('/')
def index():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios ORDER BY id').fetchall()
    conn.close()
    return render_template('index.html', usuarios=usuarios)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip().lower()
        if not nome or not email:
            flash('Nome e email são obrigatórios.')
            return redirect(url_for('create'))
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO usuarios (nome,email) VALUES (?,?)', (nome,email))
            conn.commit()
            conn.close()
            flash('Usuário criado com sucesso!')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash('Erro: email já cadastrado.')
            return redirect(url_for('create'))
    return render_template('form.html', title='Criar Usuário', usuario=None)

@app.route('/edit/<int:usuario_id>', methods=['GET','POST'])
def edit(usuario_id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id=?', (usuario_id,)).fetchone()
    conn.close()
    if not usuario:
        flash('Usuário não encontrado.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip().lower()
        if not nome or not email:
            flash('Nome e email são obrigatórios.')
            return redirect(url_for('edit', usuario_id=usuario_id))
        try:
            conn = get_db_connection()
            conn.execute('UPDATE usuarios SET nome=?, email=? WHERE id=?', (nome,email,usuario_id))
            conn.commit()
            conn.close()
            flash('Usuário atualizado com sucesso!')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash('Erro: email já cadastrado por outro usuário.')
            return redirect(url_for('edit', usuario_id=usuario_id))
    return render_template('form.html', title='Editar Usuário', usuario=usuario)

@app.route('/delete/<int:usuario_id>')
def delete(usuario_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM usuarios WHERE id=?', (usuario_id,))
    conn.commit()
    conn.close()
    flash('Usuário deletado.')
    return redirect(url_for('index'))

# ------------------------
# Rodar app
# ------------------------
if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    print("=" * 60)
    print("🚀 CRUD Flask iniciado com sucesso!")
    print(f"👉 Acesse localmente:  http://127.0.0.1:{port}")
    print(f"👉 Acesse na rede:    http://172.10.10.222:{port}")
    print("=" * 60)
    app.run(host=host, port=port, debug=True)
