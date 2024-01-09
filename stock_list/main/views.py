from flask import Blueprint,render_template,redirect,request,url_for,flash,abort
from flask_login import login_required,current_user
from stock_list.models import TableCategory,Stock
from stock_list.main.forms import TableCategoryForm,UpdateCategoryForm,AddFactorForm,AddQuantityForm,IssueQuantityForm,UpdateStockForm
from stock_list import db

main = Blueprint("main",__name__)

@main.route("/",methods =["GET","POST"])
@login_required
def home():
    table_categories =  TableCategory.query.order_by(TableCategory.id).all()
    form=TableCategoryForm()
    if form.validate_on_submit():
        table_category =TableCategory(category=form.category.data,text=form.text.data)
        db.session.add(table_category)
        db.session.commit()
        flash('表が追加されました')
        return redirect(url_for('main.home'))
    elif form.errors:
        form.category.data=""
        flash(form.errors['category'][0])
    
    return render_template("home.html",table_categories=table_categories,form=form)

@main.route("/<int:table_category_id>/table_category>",methods =["GET","POST"])
@login_required
def table_category(table_category_id):
    if not current_user.is_administrator():
        abort(403)
    table_category = TableCategory.query.get_or_404(table_category_id)
    form = UpdateCategoryForm(table_category_id)
    if form.validate_on_submit():
        table_category.category = form.category.data
        table_category.text=form.text.data
        db.session.commit()
        flash('カテゴリが更新されました')
        return redirect(url_for('main.home'))
    elif request.method == "GET":
        form.category.data = table_category.category
        form.text.data = table_category.text
    return render_template('table_category.html',form=form)




@main.route("/<int:table_category_id>/delete_category",methods =["GET","POST"])
@login_required
def delete_category(table_category_id):
    if not current_user.is_administrator():
        abort(403)
    table_category = TableCategory.query.get_or_404(table_category_id)
    stock=Stock.query.filter_by(category_id=table_category_id).all()
    db.session.delete(table_category,stock)
    db.session.commit()
    flash('カテゴリが削除されました')
    return redirect(url_for('main.home'))

@main.route("/<int:table_category_id>/table",methods =["GET","POST"])
@login_required
def table(table_category_id):
    stocks = Stock.query.filter_by(category_id=table_category_id).all()
    category =TableCategory.query.get_or_404(table_category_id)
    form = AddFactorForm(category_id=table_category_id)
    if form.validate_on_submit():
        stock =Stock(stock_name=form.stock_name.data,quantity=form.quantity.data,category_id=table_category_id)
        db.session.add(stock)
        db.session.commit()
        flash('アイテムが追加されました')
        return redirect(url_for('main.table',table_category_id=table_category_id))
    elif form.errors:
        form.stock_name.data=""
        flash(form.errors['stock_name'][0]) 
    
    return render_template("table.html",stocks=stocks,form=form,category=category)

@main.route("/<int:stock_id>/update_stock>",methods =["GET","POST"])
@login_required
def update_stock(stock_id):
    if not current_user.is_administrator():
        abort(403)
    stock = Stock.query.get_or_404(stock_id)
    form = UpdateStockForm(stock_id)
    table_category_id=stock.category_id
    stock_id=stock_id
    if form.validate_on_submit():
        stock.stock_name = form.stock_name.data
        stock.quantity=form.quantity.data
        db.session.commit()
        flash('ストック情報が更新されました')
        return redirect(url_for('main.table',table_category_id=table_category_id))
    elif request.method == "GET":
        form.stock_name.data = stock.stock_name
        form.quantity.data = stock.quantity
    return render_template('update_stock.html',form=form,stock_id=stock_id)



@main.route("/<int:stock_id>/delete_stock",methods =["GET","POST"])
@login_required
def delete_stock(stock_id):
    if not current_user.is_administrator():
        abort(403)
    stock = Stock.query.get_or_404(stock_id)
    table_category_id=stock.category_id
    db.session.delete(stock)
    db.session.commit()
    flash('ストックが削除されました')
    return redirect(url_for('main.table',table_category_id=table_category_id))


@main.route("/<int:stock_id>/add_quantity",methods =["GET","POST"])
@login_required
def add_quantity(stock_id):
    stock = Stock.query.filter_by(id=stock_id).first_or_404()
    existing_quantity=stock.quantity
    table_category_id=stock.category_id
    form = AddQuantityForm()
    if form.validate_on_submit():
        new_quantity =form.quantity.data + existing_quantity
        stock.quantity = new_quantity
        db.session.commit()
        flash('アイテムが追加されました')
        return redirect(url_for('main.table',table_category_id=table_category_id))
    return render_template("add_quantity.html",stock=stock,form=form)

@main.route("/<int:stock_id>/issue_stock",methods =["GET","POST"])
@login_required
def issue_stock(stock_id):
    stock = Stock.query.filter_by(id=stock_id).first_or_404()
    existing_quantity=stock.quantity
    table_category_id=stock.category_id
    form = IssueQuantityForm()
    if form.validate_on_submit():
        new_quantity =existing_quantity - form.quantity.data
        stock.quantity = new_quantity
        db.session.commit()
        flash('アイテムが出庫されました')
        return redirect(url_for('main.table',table_category_id=table_category_id))
    return render_template("issue_stock.html",stock=stock,form=form)

#受け取ったquantityを元の在庫の値に足してdb.commitで行けるはず