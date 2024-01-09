from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField,PasswordField,SubmitField,ValidationError
from wtforms.validators import DataRequired,Email,EqualTo
from stock_list.models import User

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('ログイン')


class RegistrationForm(FlaskForm):
    username = StringField("ユーザーネーム",validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired(), EqualTo("pass_confirm", message="Passwords do not match")])
    pass_confirm = PasswordField("パスワード（確認）",validators=[DataRequired()])
    submit = SubmitField("Sign up")
    
    def validate_username(self,field):
        if User.query.filter_by(username =field.data).first():
            raise ValidationError("This UserName are already take")
        
    
class UpdateUserForm(FlaskForm):
    username = StringField("ユーザーネーム",validators=[DataRequired()])
    password = PasswordField("パスワード",validators=[DataRequired(),EqualTo("pass_confirm","Passwords do not match")])
    pass_confirm = PasswordField("パスワード（確認）")
    submit = SubmitField("更新")
    
    def __init__(self, user_id,*args,**kwargs):
        super(UpdateUserForm,self).__init__(*args,**kwargs)
        self.id =user_id
        
    def validate_username(self,field):
        if User.query.filter(User.id !=self.id).filter_by(username =field.data).first():
            raise ValidationError("This UserName are already take")
