from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete,  asc, desc


#initialize sqlAlchemy

db =SQLAlchemy()
#connect app to db instance
def connectdb(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Pet table creation"""
    __tablename__ ='users'

    id= db.Column(db.Integer, primary_key = True, autoincrement =True)    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(250))

    @classmethod
    def delete_user(cls, user_id):
        User.query.filter_by(id =user_id).delete()
        db.session.commit()

