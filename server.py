from flask import Flask, render_template, session, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key="thekeytothecity"


@app.route('/')
def root():
    session['edit'] = 0      
    return render_template('index.html')

@app.route('/users')
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
    return redirect('/users/get_user/' + str(users_data))

@app.route('/users/<user_id>')
def show_me_the_dirt(user_id):          
    return render_template('details.html', users = user_id)

@app.route('/users/get_user/<user_id>')
def get_user(user_id):              
    mysql = connectToMySQL("flask_users")
    query = "SELECT * FROM friends WHERE id = (%(fn)s);"
    data = {
            "fn": user_id
        }
    session['secret_info'] = mysql.query_db(query, data)    
    if session['edit'] == "1":
        session['edit'] = 0
        return render_template("edit.html")
    else:
        return redirect('/users/' + user_id)

@app.route("/edit/<user_id>")
def edit_me(user_id):
    session['edit'] = 1
    return render_template('edit.html', users=user_id)

@app.route('/alter/<user_id>', methods=['POST'])
def push_edit(user_id):
    mysql = connectToMySQL("flask_users")
    query = "UPDATE friends SET first_name = %(fn)s, last_name = %(ln)s, email = %(e)s, updated_at = NOW() WHERE id =%(id)s"
    data = {
            "fn": request.form['edit_fname'],
            "ln": request.form['edit_lname'],
            "e": request.form['edit_email'],
            "id": user_id
        }
    check_yourself = mysql.query_db(query, data)
    return redirect('/users/get_user/' + user_id)

@app.route('/remove/<user_id>')
def make_delete(user_id):
    mysql = connectToMySQL("flask_users")
    query = "DELETE from friends WHERE id=%(id)s"
    data = {
        "id": user_id
    }    
    mysql.query_db(query, data)
    return redirect('/users')


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

if __name__ == '__main__':
    app.run(debug = True)