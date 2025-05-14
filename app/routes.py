
from flask import blueprints, render_template, request, redirect, url_for, flash, session
from . import mysql, bcrypt

main = blueprints.Blueprint('main', __name__)

# Página inicial
@main.route('/')
def homepage():
    return "<a href='/login'><h1>Login</h1></a>"

# Página de login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario and bcrypt.check_password_hash(usuario[3], senha):
            session['usuario_id'] = usuario[0]
            session['usuario_nome'] = usuario[1]
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.perfil'))
        else:
            flash('Email ou senha incorretos!', 'error')
    return render_template('login.html')

# Página de cadastro
@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = bcrypt.generate_password_hash(request.form['senha']).decode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        mysql.connection.commit()
        cursor.close()

        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('main.homepage'))
    return render_template('cadastro.html')

# Listagem de produtos
@main.route('/produtos')
def produtos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    cursor.close()
    return render_template('produtos.html', produtos=produtos)

# Página de perfil do usuário
@main.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    cursor = mysql.connection.cursor()

    # Compras do usuário
    cursor.execute("SELECT * FROM compras WHERE usuario_id = %s", (session['usuario_id'],))
    compras = cursor.fetchall()

    # Endereços do usuário
    cursor.execute("SELECT * FROM endereco WHERE usuario_id = %s", (session['usuario_id'],))
    enderecos = cursor.fetchall()

    # Cartões do usuário
    cursor.execute("SELECT * FROM cartoes WHERE usuario_id = %s", (session['usuario_id'],))
    cartoes = cursor.fetchall()

    cursor.close()

    return render_template('perfil.html', compras=compras, enderecos=enderecos, cartoes=cartoes)

# Logout do usuário
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))



@main.route('/enderecos', methods=['GET', 'POST'])
def enderecos():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        usuario = session['usuario_id']
        endereco = request.form['endereco']
        cidade = request.form['cidade']
        estado = request.form['estado']
        cep = request.form['cep']

        if usuario:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO endereco (usuario_id, endereco, cidade, estado, cep) VALUES (%s, %s, %s, %s, %s)",
        (usuario, endereco, cidade, estado, cep)
        )
            mysql.connection.commit()
            cursor.close()
            flash("Endereço registrado com sucesso!", "success")
        else:
            flash("endereço não registrado!", "error")

        return redirect(url_for('main.perfil'))

    return render_template('registrarinfo.html')


#registrar cartão
@main.route('/cartoes', methods=['GET', 'POST'])
def cartoes():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        usuario = session['usuario_id']
        numero_cartao = request.form['numero_cartao']
        nome_titular = request.form['nome_titular']
        validade = request.form['validade']
        cvv = request.form['cvv']

        if usuario:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO cartoes (usuario_id, numero_cartao, nome_titular, validade, cvv) VALUES (%s, %s, %s, %s, %s)",
                           (usuario, numero_cartao, nome_titular, validade, cvv))
            mysql.connection.commit()
            cursor.close()
            flash("Cartão registrado com sucesso!", "success")
        else:
            flash("Cartão não registrado!", "error")
        return redirect(url_for('main.perfil'))

    return render_template('cartaoinfo.html')