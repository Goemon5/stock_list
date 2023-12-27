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
    password = PasswordField("パスワード", validators=[DataRequired(), EqualTo("pass_confirm", message="パスワードが一致していません")])
    pass_confirm = PasswordField("パスワード（確認）",validators=[DataRequired()])
    submit = SubmitField("登録")
    
    def validate_username(self,field):
        if User.query.filter_by(username =field.data).first():
            raise ValidationError("入力されたユーザー名は既に使われています")
        
    
class UpdateUserForm(FlaskForm):
    username = StringField("ユーザーネーム",validators=[DataRequired()])
    password = PasswordField("パスワード",validators=[DataRequired(),EqualTo("pass_confirm","パスワードが一致していません")])
    pass_confirm = PasswordField("パスワード（確認）")
    submit = SubmitField("更新")
    
    def __init__(self, user_id,*args,**kwargs):
        super(UpdateUserForm,self).__init__(*args,**kwargs)
        self.id =user_id
        
    def validate_username(self,field):
        if User.query.filter(User.id !=self.id).filter_by(username =field.data).first():
            raise ValidationError("入力されたユーザー名は既に使われています")
