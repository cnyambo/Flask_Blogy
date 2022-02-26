from crypt import methods
from distutils.log import debug
from flask import Flask, request, render_template, redirect, jsonify, flash, session
from flask_debugtoolbar   import DebugToolbarExtension
from models import db, connectdb, User 


app = Flask(__name__)

# config DB url (connect to db)

app.config['SQLALCHEMY_DATABASE_URI']  =  'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False



app.config['SECRET_KEY'] = "test@123!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] =False
app.config['SQLALCHEMY_ECHO'] =True
debug = DebugToolbarExtension(app)
connectdb(app)

@app.route('/')
def print_users():
   
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html',users=users)

@app.route('/users/new')   
def user_form():
    """add a new user"""
    return render_template("add_user.html")

@app.route('/users/new',methods=['POST'])   
def create_user():
    """add a new user"""
    fname = request.form["first_name"]
    lname = request.form["last_name"]
    image_url = request.form["url"]
    new_user = User(first_name = fname, last_name=lname, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/users/{new_user.id}")

@app.route('/users/<int:user_id>')    
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def manage_user(user_id):
    user = User.query.get(user_id)
    if request.form['submit_button'] == 'edit':
        return render_template("edit.html", user=user)
    else:
        User.delete_user(user_id)  
        return redirect('/')

@app.route('/users/<int:user_id>/update', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    fname = request.form["first_name"]
    lname = request.form["last_name"]
    image_url = request.form["url"]
       
    if request.form['btn_submit'] == 'edit':
        user.first_name = fname
        user.last_name = lname
        user.image_url = image_url
        db.session.add(user)
        db.session.commit() 
        return redirect("/")
    else:
        return redirect('/')
