from flask import Flask, render_template, session, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key="thekeytothecity"

@app.route('/')
def root():    
    return render_template('index.html')

@app.route('/users')
@app.route('/users.html')
def users():
    mysql = connectToMySQL("flask_users")
    session['users'] = mysql.query_db("SELECT id, first_name, last_name, email, created_at FROM friends")
    return render_template('users.html')

@app.route('/users/new')
def add_user():    
    return render_template('new.html')

@app.route('/users/add_user', methods=['POST'])
def add_it_up():    
    mysql = connectToMySQL("flask_users")
    query = "INSERT INTO friends (first_name, last_name, email, created_at) VALUES (%(fn)s, %(ln)s, %(e)s, NOW());"
    data = {
        "fn": request.form['first_name'],
        "ln": request.form['last_name'],
        "e": request.form['email']            
    }
    
    users_data = mysql.query_db(query, data)        
    return redirect('/users/' + str(users_data))

@app.route('/users/<user_id>')
def show_me_the_dirt(user_id):
    users_id = user_id    
    return render_template('details.html', users = users_id)



if __name__ == '__main__':
    app.run(debug = True)