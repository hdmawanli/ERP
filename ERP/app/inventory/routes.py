from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Product as Inventory, InventoryFlow, InventoryBalance as Stock, ProductCategory, Unit, SeedBatch
from datetime import datetime
from app.inventory import inventory

# 库存商品管理
@inventory.route('/')
@login_required
def index():
    items = Inventory.query.all()
    return render_template('inventory/item_list.html', items=items)

@inventory.route('/item/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        item_code = request.form['item_code']
        item_name = request.form['item_name']
        category_id = int(request.form['category_id'])
        unit_id = int(request.form['unit_id'])
        purchase_price = float(request.form['purchase_price'])
        sale_price = float(request.form['sale_price'])
        
        new_item = Inventory(
            item_code=item_code,
            product_name=item_name,
            category_id=category_id,
            unit_id=unit_id,
            purchase_price=purchase_price,
            sale_price=sale_price,
            status=1
        )
        
        db.session.add(new_item)
        db.session.flush()  # 刷新以获取item_id
        
        # 创建库存记录
        new_stock = Stock(
            type='product',
            item_id=new_item.product_id,
            quantity=0,
            warehouse_id=1
        )
        
        db.session.add(new_stock)
        db.session.commit()
        flash('库存商品创建成功', 'success')
        return redirect(url_for('inventory.index'))
    
    categories = ProductCategory.query.all()
    units = Unit.query.all()
    return render_template('inventory/item_form.html', title='添加库存商品', categories=categories, units=units)

@inventory.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Inventory.query.get_or_404(item_id)
    
    if request.method == 'POST':
        item.item_code = request.form['item_code']
        item.product_name = request.form['item_name']
        item.category_id = int(request.form['category_id'])
        item.unit_id = int(request.form['unit_id'])
        item.purchase_price = float(request.form['purchase_price'])
        item.sale_price = float(request.form['sale_price'])
        
        db.session.commit()
        flash('库存商品更新成功', 'success')
        return redirect(url_for('inventory.index'))
    
    categories = ProductCategory.query.all()
    units = Unit.query.all()
    return render_template('inventory/item_form.html', item=item, title='编辑库存商品', categories=categories, units=units)

@inventory.route('/item/delete/<int:item_id>')
@login_required
def delete_item(item_id):
    item = Inventory.query.get_or_404(item_id)
    item.status = 0  # 软删除
    db.session.commit()
    flash('库存商品已删除', 'success')
    return redirect(url_for('inventory.index'))

# 库存现存量查询
@inventory.route('/stock/query')
@login_required
def stock_query():
    keyword = request.args.get('keyword', '')
    
    query = Stock.query.join(Inventory, Stock.item_id == Inventory.product_id).filter(
            Stock.type == 'product',
            Inventory.status == 1
        )
    
    if keyword:
        query = query.filter((Inventory.item_code.like(f'%{keyword}%')) | (Inventory.product_name.like(f'%{keyword}%')))
    
    stocks = query.all()
    
    return render_template('inventory/stock_query.html', stocks=stocks, keyword=keyword)

@inventory.route('/stock/detail/<int:item_id>')
@login_required
def stock_detail(item_id):
    item = Inventory.query.get_or_404(item_id)
    stock = Stock.query.filter_by(type='product', item_id=item_id).first()
    return render_template('inventory/stock_detail.html', item=item, stock=stock)