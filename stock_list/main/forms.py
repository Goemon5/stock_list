from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField,SubmitField,ValidationError,IntegerField
from wtforms.validators import DataRequired,NumberRange
from stock_list.models import TableCategory,Stock

class TableCategoryForm(FlaskForm):
    category = StringField("カテゴリ名",validators=[DataRequired()])
    text = StringField("説明文")
    submit =SubmitField("保存")
    
    def validate_category(self,field):
        if TableCategory.query.filter_by(category=field.data).first():
            raise ValidationError("入力されたカテゴリ名は既に使われています")
        

class UpdateCategoryForm(FlaskForm):
    category = StringField("カテゴリ名",validators=[DataRequired()])
    text = StringField("説明文")
    submit =SubmitField("更新")
    
    def __init__(self, table_category_id,*args,**kwargs):
        super(UpdateCategoryForm,self).__init__(*args,**kwargs)
        self.id = table_category_id
        
    def validate_category(self,field):
         if TableCategory.query.filter_by(category=field.data).first():
            raise ValidationError("入力されたカテゴリ名は既に使われています")
        
        
class AddFactorForm(FlaskForm):
    stock_name =StringField("商品名",validators=[DataRequired()])
    quantity= IntegerField("数値",validators=[DataRequired(),NumberRange(min=1)])
    category_id =IntegerField("カテゴリーID",validators=[DataRequired()])
    submit =SubmitField("追加")
    
    
    def validate_stock_name(self,field):
         if Stock.query.filter_by(stock_name=field.data).first():
            raise ValidationError("入力された商品名は既に使われています")
        
        
class UpdateStockForm(FlaskForm):
    stock_name =StringField("商品名",validators=[DataRequired()])
    quantity= IntegerField("数値",validators=[DataRequired(),NumberRange(min=1)])
    #category_id =IntegerField("カテゴリーID",validators=[DataRequired()])
    submit =SubmitField("更新")
    
    def __init__(self, stock_id,*args,**kwargs):
        super(UpdateStockForm,self).__init__(*args,**kwargs)
        self.id = stock_id
        
    def validate_stock_name(self,field):
         if Stock.query.filter_by(stock_name=field.data).first():
            raise ValidationError("入力された商品名は既に使われています")
        
class AddQuantityForm(FlaskForm):
    quantity= IntegerField("数値",validators=[DataRequired(),NumberRange(min=1)])
    submit =SubmitField("追加")
    
class IssueQuantityForm(FlaskForm):
    quantity= IntegerField("数値",validators=[DataRequired(),NumberRange(min=1)])
    submit =SubmitField("出庫")