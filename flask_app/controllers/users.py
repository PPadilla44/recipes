from re import S
from flask_app import app
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
from flask import render_template,redirect,request,session,flash

from flask_app.config.mysqlconnection import connectToMySQL
from ..models.user import User
from ..models.recipe import Recipe

@app.route('/')
def index():

    if 'user' in session:
        return redirect('/recipes')

    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():

    if not User.register_validation(request.form):
        return redirect('/')

    hashy = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashy,
    }

    flash("Successfully logged in")
    user = User.save(data)
    session['user'] = user

    return redirect(f'/recipes')


@app.route('/recipes')
def recipes():

    if 'user' not in session:
        flash("Must be logged in to view recipes")
        return redirect('/')

    data = {
        'id': session['user']
    }
    
    return render_template('recipes.html',user = User.get_user_by_id(data),
    recipes=Recipe.get_all_user_recipes(data))


@app.route('/login', methods=['POST'])
def login():

    user = User.get_user_by_email({'email': request.form['email']})
    if not User.login_validation(user,request.form['password']):
        return redirect('/')
    
    flash("Successfully logged in")

    print(user.password)
    session['user'] = user.id

    return redirect('/recipes')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

