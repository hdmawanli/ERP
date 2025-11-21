from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import AssemblyOrder, AssemblyOrderDetail, Material, Product, InventoryBalance as Stock
from datetime import datetime

from app.assembly import assembly

# 组装订单列表
@assembly.route('/')
@login_required
def index():
    orders = AssemblyOrder.query.all()
    return render_template('assembly/order_list.html', orders=orders)

# 添加组装订单
@assembly.route('/add', methods=['GET', 'POST'])
@login_required
def add_assembly_order():
    # 获取所有原材料和库存商品
    raw_materials = Material.query.filter_by(status=1).all()
    finished_goods = Product.query.filter_by(status=1).all()
    
    if request.method == 'POST':
        finished_goods_id = int(request.form['finished_goods_id'])
        production_date = datetime.strptime(request.form['production_date'], '%Y-%m-%d').date()
        quantity_produced = float(request.form['quantity_produced'])
        warehouse_id = int(request.form['warehouse_id']) if request.form['warehouse_id'] else 1
        
        # 处理组装所需原材料
        raw_items = request.form.getlist('raw_item_id[]')
        raw_quantities = request.form.getlist('raw_quantity[]')
        order_no = request.form['order_no']
        
        # 验证原材料库存是否足够
        for i in range(len(raw_items)):
            raw_item_id = int(raw_items[i])
            required_quantity = float(raw_quantities[i]) * quantity_produced  # 乘以生产数量
            
            # 检查库存
            stock = Stock.query.filter_by(type='material', item_id=raw_item_id, warehouse_id=warehouse_id).first()
            if not stock or stock.quantity < required_quantity:
                flash(f'原材料 {Material.query.get(raw_item_id).material_name} 库存不足', 'error')
                return redirect(url_for('assembly.add_assembly_order'))
        
        # 创建组装订单
        new_order = AssemblyOrder(
            order_no=order_no,
            product_id=finished_goods_id,
            order_date=production_date,
            quantity=quantity_produced,
            warehouse_id=warehouse_id,
            status=1,
            created_by=current_user.user_id
        )
        
        db.session.add(new_order)
        db.session.flush()  # 获取order_id
        
        # 创建组装原材料记录
        for i in range(len(raw_items)):
            raw_item_id = int(raw_items[i])
            raw_quantity = float(raw_quantities[i])
            
            new_order_detail = AssemblyOrderDetail(
                order_id=new_order.order_id,
                material_id=raw_item_id,
                quantity=raw_quantity
            )
            
            db.session.add(new_order_detail)
        
        # 更新原材料库存（减少）
        for i in range(len(raw_items)):
            raw_item_id = int(raw_items[i])
            required_quantity = float(raw_quantities[i]) * quantity_produced
            
            stock = Stock.query.filter_by(type='material', item_id=raw_item_id, warehouse_id=warehouse_id).first()
            if stock:
                stock.quantity -= required_quantity
        
        # 更新成品库存（增加）
        finished_stock = Stock.query.filter_by(type='product', item_id=finished_goods_id, warehouse_id=warehouse_id).first()
        if finished_stock:
            finished_stock.quantity += quantity_produced
        else:
            new_finished_stock = Stock(
                type='product',
                item_id=finished_goods_id,
                warehouse_id=warehouse_id,
                quantity=quantity_produced
            )
            db.session.add(new_finished_stock)
        
        db.session.commit()
        flash('组装生产完成，库存已更新', 'success')
        return redirect(url_for('assembly.index'))
    
    return render_template('assembly/order_form.html', title='添加组装订单', raw_materials=raw_materials, finished_goods=finished_goods)

# 组装订单详情
@assembly.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = AssemblyOrder.query.get_or_404(order_id)
    raw_materials = AssemblyOrderDetail.query.filter_by(order_id=order_id).all()
    finished_good = Product.query.get(order.product_id)
    return render_template('assembly/order_detail.html', order=order, raw_materials=raw_materials, finished_good=finished_good)

# 获取成品详情（用于AJAX请求）
@assembly.route('/finished-good/<int:item_id>')
@login_required
def get_finished_good(item_id):
    item = Product.query.get_or_404(item_id)
    return jsonify({
        'item_id': item.product_id,
        'item_name': item.product_name,
        'unit': item.unit.unit_name
    })

# 获取原材料详情（用于AJAX请求）
@assembly.route('/raw-material/<int:item_id>')
@login_required
def get_raw_material(item_id):
    item = Material.query.get_or_404(item_id)
    return jsonify({
        'item_id': item.material_id,
        'item_name': item.material_name,
        'unit': item.unit.unit_name
    })

# 组装订单列表
@assembly.route('/orders')
@login_required
def orders():
    orders = AssemblyOrder.query.all()
    return render_template('assembly/order_list.html', orders=orders)

# 组装生产单查询
@assembly.route('/order/search')
@login_required
def search_order():
    order_no = request.args.get('order_no')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = AssemblyOrder.query
    
    if order_no:
        query = query.filter(AssemblyOrder.order_no.like(f'%{order_no}%'))
    if start_date and end_date:
        query = query.filter(AssemblyOrder.order_date.between(start_date, end_date))
    
    orders = query.all()
    return render_template('assembly/order_list.html', orders=orders)