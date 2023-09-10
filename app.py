from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)



@app.route('/')
@app.route('/index')
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/usuarios')
def usuarios():
    # Handle the usuarios page logic here
    return render_template('usuarios.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/temas')
def temas():
    # Handle the temas page logic here
    return render_template('temas.html')

@app.route('/libreria')
def libreria():
    # Handle the librery page logic here
    return render_template('libreria.html')

if __name__ == '__main__':
    app.run(debug=True)
