from flask import Flask
from flask import blueprints, render_template, request, redirect, url_for, flash, session
from app import mysql, bcrypt


main = blueprints.Blueprint('main', __name__)







@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #verifica se o formulario foi enviado
        email = request.form['email']
        senha = request.form['senha']
        #pegando email e senha digitados pelo usuario
        cursor = mysql.connection.cursor()
        #abrindo a conexao
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        #procurando o email no banco de dados
        usuario = cursor.fetchone()
        cursor.close()
        #fecha o canal de comunicação do flask com o banco de dados
        if usuario and bcrypt.check_password_hash(usuario[3], senha):
            session['usuario_id'] = usuario[0]
            session['usuario_nome'] = usuario[1]
            flash('Login Realizada com Sucesso!', 'success')
            return redirect(url_for('main.produtos'))
        else:
            flash('Email ou senha incorretos!', 'error')
    return render_template('login.html')




@main.route('/produtos')
def produtos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    cursor.close()
    return render_template('produtos.html', produtos=produtos)


@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
    #quando o formulario for enviado
        nome = request.form['nome']
        email = request.form['email']
        senha = bcrypt.generate_password_hash(request.form['senha']).decode('utf-8')
        #criptografando a senha
        #são coletado esses dados

        cursor = mysql.connection.cursor()
    #"cursor" = criado para executar comandos SQL no banco
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        mysql.connection.commit()
    #salva as alterações no banco
        cursor.close()
    #fecha o cursor para liberar recurso

        flash('Usuario cadastrado!')
        return redirect(url_for('main.perfil'))
    #usuario redirecionado para a pagina principal após o cadastro
    return render_template('cadastro.html')
    #caso seja uma requisição get, mostra o formulario sem salvar nada





@main.route('/perfil')
def perfil():
    #verifica se o usuario não esta conectado
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))
    cursor = mysql.connection.cursor()
    #buscando compras do usuario
    cursor.execute("SELECT * FROM compras WHERE usuario_id = %s", (session['usuario_id'],))
    compras = cursor.fetchall()

    #buscando enderecos do usuario
    cursor.execute("SELECT * FROM endereco WHERE usuario_id = %s", (session['usuario_id'],))
    enderecos = cursor.fetchall()

    #buscando os cartoes dos usuarios
    cursor.execute("SELECT * FROM cartoes WHERE usuario_id = %s", (session['usuario_id'],))
    cartoes = cursor.fetchall()
    cursor.close()
    return render_template('perfil.html', compras=compras, enderecos=enderecos,
                           cartoes=cartoes)



# Página de logout
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))