from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Customer, SalesOrder, SalesOrderDetail, Product as Inventory, InventoryBalance as Stock
from datetime import datetime
from app.sales import sales

# 销售订单列表
@sales.route('/')
@login_required
def index():
    # 获取查询参数
    order_no = request.args.get('order_no')
    customer_name = request.args.get('customer_name')
    status = request.args.get('status')
    
    # 构建查询，使用joinedload预加载客户和仓库数据
    from sqlalchemy.orm import joinedload
    query = SalesOrder.query.options(joinedload(SalesOrder.customer), joinedload(SalesOrder.warehouse))
    
    if order_no:
        query = query.filter(SalesOrder.order_no.like(f'%{order_no}%'))
    
    if customer_name:
        query = query.join(Customer).filter(Customer.customer_name.like(f'%{customer_name}%'))
    
    if status:
        query = query.filter(SalesOrder.status == int(status))
    
    orders = query.all()
    
    # 获取所有客户用于查询下拉框
    customers = Customer.query.all()
    
    return render_template('sales/order_list.html', orders=orders, customers=customers, 
                           order_no=order_no, customer_name=customer_name, status=status)

# 添加销售订单
@sales.route('/order/add', methods=['GET', 'POST'])
@login_required
def add_sale_order():
    customers = Customer.query.filter_by(status=1).all()
    inventory_items = Inventory.query.filter_by(status=1).all()  # 移除type=1筛选条件
    
    if request.method == 'POST':
        customer_id = int(request.form['customer_id'])
        order_no = request.form['order_no']
        order_date = datetime.strptime(request.form['order_date'], '%Y-%m-%d').date()
        warehouse_id = int(request.form['warehouse_id']) if request.form['warehouse_id'] else 1
        
        # 处理销售订单明细
        items = request.form.getlist('item_id[]')
        quantities = request.form.getlist('quantity[]')
        unit_prices = request.form.getlist('unit_price[]')
        
        # 验证库存是否足够
        for i in range(len(items)):
            item_id = int(items[i])
            quantity = float(quantities[i])
            
            stock = Stock.query.filter_by(item_id=item_id, warehouse_id=warehouse_id, type='product').first()  # 添加type='product'
            if not stock or stock.quantity < quantity:
                flash(f'商品 {Inventory.query.get(item_id).product_name} 库存不足', 'error')
                return redirect(url_for('sales.add_sale_order'))
        
        # 创建销售订单（不在订单表中保存仓库，仓库信息用于库存校验/出库）
        new_order = SalesOrder(
            customer_id=customer_id,
            order_no=order_no,
            order_date=order_date,
            status=1,
            created_by=current_user.user_id
        )
        
        db.session.add(new_order)
        db.session.flush()  # 获取order_id
        
        # 处理销售订单明细
        for i in range(len(items)):
            item_id = int(items[i])
            quantity = float(quantities[i])
            unit_price = float(unit_prices[i])
            amount = quantity * unit_price
            
            new_detail = SalesOrderDetail(
                order_id=new_order.order_id,
                product_id=item_id,
                quantity=quantity,
                price=unit_price,
                amount=amount
            )
            
            db.session.add(new_detail)
        
        # 更新库存数量
        for i in range(len(items)):
            item_id = int(items[i])
            quantity = float(quantities[i])
            
            stock = Stock.query.filter_by(item_id=item_id, warehouse_id=warehouse_id, type='product').first()  # 添加type='product'
            if stock:
                stock.quantity -= quantity
        
        db.session.commit()
        flash('销售订单创建成功，库存已更新', 'success')
        return redirect(url_for('sales.index'))
    
    return render_template('sales/order_form.html', title='添加销售订单', customers=customers, inventory_items=inventory_items)

# 销售订单详情
@sales.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = SalesOrder.query.get_or_404(order_id)
    details = SalesOrderDetail.query.filter_by(order_id=order_id).all()
    customer = Customer.query.get(order.customer_id)
    return render_template('sales/order_detail.html', order=order, details=details, customer=customer)

# 销售订单列表
@sales.route('/orders')
@login_required
def orders():
    orders = SalesOrder.query.all()
    return render_template('sales/order_list.html', orders=orders)

# 获取商品库存信息（用于AJAX请求）
@sales.route('/item/<int:item_id>/stock/<int:warehouse_id>')
@login_required
def get_item_stock(item_id, warehouse_id):
    stock = Stock.query.filter_by(item_id=item_id, warehouse_id=warehouse_id, type='product').first()  # 添加type='product'
    if stock:
        return jsonify({'quantity': float(stock.quantity)})
    else:
        return jsonify({'quantity': 0})

# 销售出库
@sales.route('/outbound')
@login_required
def outbound():
    from sqlalchemy.orm import joinedload
    orders = SalesOrder.query.filter_by(status=1).options(joinedload(SalesOrder.customer), joinedload(SalesOrder.warehouse)).all()  # 仅显示已审核待出库的订单
    return render_template('sales/outbound_list.html', orders=orders)

# 销售出库处理
@sales.route('/outbound/<int:order_id>', methods=['GET', 'POST'])
@login_required
def process_outbound(order_id):
    order = SalesOrder.query.get_or_404(order_id)
    
    if request.method == 'POST':
        # 更新销售订单状态为已出库
        order.status = 2  # 2: 已出库
        
        db.session.commit()
        flash('销售出库处理成功', 'success')
        return redirect(url_for('sales.outbound'))
    
    details = SalesOrderDetail.query.filter_by(order_id=order_id).all()
    customer = Customer.query.get(order.customer_id)
    return render_template('sales/outbound_form.html', order=order, details=details, customer=customer)

# 销售订单查询
@sales.route('/order/search')
@login_required
def search_order():
    order_no = request.args.get('order_no')
    customer_id = request.args.get('customer_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = SalesOrder.query
    
    if order_no:
        query = query.filter(SalesOrder.order_no.like(f'%{order_no}%'))
    if customer_id:
        query = query.filter_by(customer_id=int(customer_id))
    if start_date and end_date:
        query = query.filter(SalesOrder.order_date.between(start_date, end_date))
    
    orders = query.all()
    return render_template('sales/order_list.html', orders=orders)