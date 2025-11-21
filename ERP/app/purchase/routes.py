from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import PurchaseOrder, PurchaseOrderDetail, Supplier, Material, InventoryBalance
from datetime import datetime
from app.purchase import purchase

# 采购订单列表
@purchase.route('/')
@login_required
def index():
    # 获取查询参数
    order_no = request.args.get('order_no')
    supplier_name = request.args.get('supplier_name')
    status = request.args.get('status')
    
    # 构建查询，使用joinedload预加载供应商数据
    from sqlalchemy.orm import joinedload
    query = PurchaseOrder.query.options(joinedload(PurchaseOrder.supplier))
    
    if order_no:
        query = query.filter(PurchaseOrder.order_no.like(f'%{order_no}%'))
    
    if supplier_name:
        query = query.join(Supplier).filter(Supplier.supplier_name.like(f'%{supplier_name}%'))
    
    if status:
        query = query.filter(PurchaseOrder.status == int(status))
    
    orders = query.all()
    
    # 获取所有供应商用于查询下拉框
    suppliers = Supplier.query.all()
    
    return render_template('purchase/order_list.html', orders=orders, suppliers=suppliers, 
                           order_no=order_no, supplier_name=supplier_name, status=status)

# 添加采购订单
@purchase.route('/order/add', methods=['GET', 'POST'])
@login_required
def add_order():
    suppliers = Supplier.query.filter_by(status=1).all()
    raw_materials = Material.query.filter_by(status=1).all()
    
    if request.method == 'POST':
        supplier_id = int(request.form['supplier_id'])
        order_no = request.form['order_no']
        order_date = datetime.strptime(request.form['order_date'], '%Y-%m-%d').date()
        expected_date = datetime.strptime(request.form['expected_date'], '%Y-%m-%d').date()
        
        # 创建采购订单
        new_order = PurchaseOrder(
            supplier_id=supplier_id,
            order_no=order_no,
            order_date=order_date,
            expected_date=expected_date,
            status=1,  # 1: 待收货
            created_by=current_user.user_id
        )
        
        db.session.add(new_order)
        db.session.flush()  # 获取order_id
        
        # 处理采购订单明细
        items = request.form.getlist('item_id[]')
        quantities = request.form.getlist('quantity[]')
        unit_prices = request.form.getlist('unit_price[]')
        
        for i in range(len(items)):
            item_id = int(items[i])
            quantity = float(quantities[i])
            unit_price = float(unit_prices[i])
            amount = quantity * unit_price
            
            new_detail = PurchaseOrderDetail(
                order_id=new_order.order_id,
                material_id=item_id,
                quantity=quantity,
                price=unit_price,
                amount=amount
            )
            
            db.session.add(new_detail)
        
        db.session.commit()
        flash('采购订单创建成功', 'success')
        return redirect(url_for('purchase.index'))
    
    return render_template('purchase/order_form.html', title='添加采购订单', suppliers=suppliers, raw_materials=raw_materials)

# 采购订单详情
@purchase.route('/order/<int:order_id>')
def order_detail(order_id):
    order = PurchaseOrder.query.get_or_404(order_id)
    details = PurchaseOrderDetail.query.filter_by(order_id=order_id).all()
    return render_template('purchase/order_detail.html', order=order, details=details)

# 采购收货
@purchase.route('/receipt/add', methods=['GET', 'POST'])
@login_required
def add_receipt():
    # 仅显示待收货的采购订单
    pending_orders = PurchaseOrder.query.filter_by(status=1).all()
    
    if request.method == 'POST':
        order_id = int(request.form['order_id'])
        receipt_date = datetime.strptime(request.form['receipt_date'], '%Y-%m-%d').date()
        warehouse_id = 1  # 默认仓库
        
        # 更新采购订单状态为已收货
        purchase_order = PurchaseOrder.query.get_or_404(order_id)
        purchase_order.status = 2  # 2: 已收货
        purchase_order.receipt_date = receipt_date
        
        # 处理收货明细并更新库存
        details = PurchaseOrderDetail.query.filter_by(order_id=order_id).all()
        
        for detail in details:
            # 获取或创建库存记录
            stock = InventoryBalance.query.filter_by(type='material', item_id=detail.material_id, warehouse_id=warehouse_id).first()
            
            if stock:
                # 如果存在记录，更新数量
                stock.quantity += detail.quantity
                # 可以考虑更新成本价和金额，这里简单处理
                stock.amount = stock.quantity * stock.cost_price
            else:
                # 如果不存在记录，创建新记录
                new_stock = InventoryBalance(
                    type='material',
                    item_id=detail.material_id,
                    warehouse_id=warehouse_id,
                    quantity=detail.quantity,
                    cost_price=detail.price,
                    amount=detail.amount
                )
                db.session.add(new_stock)
        
        db.session.commit()
        flash('采购收货成功，库存已更新', 'success')
        return redirect(url_for('purchase.index'))
    
    return render_template('purchase/receipt_form.html', title='添加采购收货', pending_orders=pending_orders)

# 获取订单明细（用于AJAX请求）
@purchase.route('/order/<int:order_id>/details')
@login_required
def get_order_details(order_id):
    details = PurchaseOrderDetail.query.filter_by(order_id=order_id).all()
    result = []
    
    for detail in details:
        item = Material.query.get(detail.material_id)
        result.append({
            'item_id': detail.material_id,
            'item_name': item.material_name,
            'unit': item.unit.unit_name,
            'quantity': detail.quantity,
            'unit_price': float(detail.price),
            'amount': float(detail.amount)
        })
    
    return jsonify(result)

# 采购订单列表
@purchase.route('/orders')
@login_required
def orders():
    orders = PurchaseOrder.query.all()
    return render_template('purchase/order_list.html', orders=orders)