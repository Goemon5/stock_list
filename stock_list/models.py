from flask_login import UserMixin
from werkzeug.security import check_password_hash,generate_password_hash
from stock_list import db,login_manager





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True,index=True)
    password_hash = db.Column(db.String(128))
    administrator = db.Column(db.String(1))
    
    def __init__(self,username,password,administrator):
        self.username=username
        self.password=password
        self.administrator = administrator
    def __repr__(self):
        return f"Username: {self.username}"
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise AttributeError("password is not readble attribute")

    @password.setter
    def password(self,password):
        self.password_hash= generate_password_hash(password)
        
    def is_administrator(self):
        if self.administrator == "1":
            return 1
        else:
            return 0
        
        
    
class Stock(db.Model):
    __tablelename__="stock_table"
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(140))
    quantity = db.Column(db.Integer)
    category_id = db.Column(db.Integer,db.ForeignKey("table_category.id"))
    
    def __init__(self,stock_name,quantity,category_id):
        self.stock_name= stock_name
        self.quantity=quantity
        self.category_id =category_id
        
        
    
    def __repr__(self):
        return f"PostID: {self.id},Stockname:{self.stock_name}/n"

class TableCategory(db.Model):
    __tablename__ = 'table_category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(140))
    text =db.Column(db.String(140))
    
    def __init__(self, category,text):
        self.category = category
        self.text=text
        
    
    def __repr__(self):
        return f"CategoryID: {self.id}, CategoryName: {self.category} ,Categorytext: {self.text}\n"

   