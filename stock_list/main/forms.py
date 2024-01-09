from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField,SubmitField,ValidationError,IntegerField
from wtforms.validators import DataRequired,NumberRange
from stock_list.models import TableCategory,Stock

class TableCategoryForm(FlaskForm):
    category = StringField("CategoryName",validators=[DataRequired()])
    text = StringField("instruction")
    submit =SubmitField("submit")
    
    def validate_category(self,field):
        if TableCategory.query.filter_by(category=field.data).first():
            raise ValidationError("This Category Name are already taken")
        

class UpdateCategoryForm(FlaskForm):
    category = StringField("CategoryName",validators=[DataRequired()])
    text = StringField("instruction")
    submit =SubmitField("Update")
    
    def __init__(self, table_category_id,*args,**kwargs):
        super(UpdateCategoryForm,self).__init__(*args,**kwargs)
        self.id = table_category_id
        
    def validate_category(self,field):
         if TableCategory.query.filter_by(category=field.data).first():
            raise ValidationError("This Category Name are already taken")
        
        
class AddFactorForm(FlaskForm):
    stock_name =StringField("Stock Name",validators=[DataRequired()])
    quantity= IntegerField("Quantity",validators=[DataRequired(),NumberRange(min=1)])
    category_id =IntegerField("CategoryID",validators=[DataRequired()])
    submit =SubmitField("Add")
    
    
    def validate_stock_name(self,field):
         if Stock.query.filter_by(stock_name=field.data).first():
            raise ValidationError("This Stock Name are already taken")
        
        
class UpdateStockForm(FlaskForm):
    stock_name =StringField("Stock Name",validators=[DataRequired()])
    quantity= IntegerField("quantity",validators=[DataRequired(),NumberRange(min=1)])
    submit =SubmitField("Update")
    
    def __init__(self, stock_id,*args,**kwargs):
        super(UpdateStockForm,self).__init__(*args,**kwargs)
        self.id = stock_id
        
    def validate_stock_name(self,field):
         if Stock.query.filter_by(stock_name=field.data).first():
            raise ValidationError("This Stock Name are already taken")
        
class AddQuantityForm(FlaskForm):
    quantity= IntegerField("Quantity",validators=[DataRequired(),NumberRange(min=1)])
    submit =SubmitField("Add")
    
class IssueQuantityForm(FlaskForm):
    quantity= IntegerField("Quantity",validators=[DataRequired(),NumberRange(min=1)])
    submit =SubmitField("Issue")