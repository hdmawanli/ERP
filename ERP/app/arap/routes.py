from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Customer, Supplier, Receivable, Payable, Receipt, Payment
from datetime import datetime

from app.arap import arap

# 客户管理
@arap.route('/customers')
@login_required
def customers():
    customers = Customer.query.all()
    return render_template('arap/customer_list.html', customers=customers)

@arap.route('/customer/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        customer_code = request.form['customer_code']
        customer_name = request.form['customer_name']
        contact_person = request.form['contact_person']
        phone = request.form['phone']
        address = request.form['address']
        credit_limit = float(request.form['credit_limit']) if request.form['credit_limit'] else 0.00
        
        new_customer = Customer(
            customer_code=customer_code,
            customer_name=customer_name,
            contact_person=contact_person,
            phone=phone,
            address=address,
            credit_limit=credit_limit,
            status=1
        )
        
        db.session.add(new_customer)
        db.session.commit()
        flash('客户创建成功', 'success')
        return redirect(url_for('arap.customers'))
    
    return render_template('arap/customer_form.html', title='添加客户')

@arap.route('/customer/edit/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'POST':
        customer.customer_code = request.form['customer_code']
        customer.customer_name = request.form['customer_name']
        customer.contact_person = request.form['contact_person']
        customer.phone = request.form['phone']
        customer.address = request.form['address']
        customer.credit_limit = float(request.form['credit_limit']) if request.form['credit_limit'] else 0.00
        
        db.session.commit()
        flash('客户信息更新成功', 'success')
        return redirect(url_for('arap.customers'))
    
    return render_template('arap/customer_form.html', title='编辑客户', customer=customer)

# 供应商管理
@arap.route('/suppliers')
@login_required
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('arap/supplier_list.html', suppliers=suppliers)

@arap.route('/supplier/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        supplier_code = request.form['supplier_code']
        supplier_name = request.form['supplier_name']
        contact_person = request.form['contact_person']
        phone = request.form['phone']
        address = request.form['address']
        payment_term = request.form['payment_term']
        
        new_supplier = Supplier(
            supplier_code=supplier_code,
            supplier_name=supplier_name,
            contact_person=contact_person,
            phone=phone,
            address=address,
            payment_term=payment_term,
            status=1
        )
        
        db.session.add(new_supplier)
        db.session.commit()
        flash('供应商创建成功', 'success')
        return redirect(url_for('arap.suppliers'))
    
    return render_template('arap/supplier_form.html', title='添加供应商')

@arap.route('/supplier/edit/<int:supplier_id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    
    if request.method == 'POST':
        supplier.supplier_code = request.form['supplier_code']
        supplier.supplier_name = request.form['supplier_name']
        supplier.contact_person = request.form['contact_person']
        supplier.phone = request.form['phone']
        supplier.address = request.form['address']
        supplier.payment_term = request.form['payment_term']
        
        db.session.commit()
        flash('供应商信息更新成功', 'success')
        return redirect(url_for('arap.suppliers'))
    
    return render_template('arap/supplier_form.html', title='编辑供应商', supplier=supplier)

# 应收账款
@arap.route('/ar/invoices')
@login_required
def ar_invoices():
    invoices = Receivable.query.all()
    return render_template('arap/ar_invoice_list.html', invoices=invoices)

@arap.route('/ar/invoice/add', methods=['GET', 'POST'])
@login_required
def add_ar_invoice():
    customers = Customer.query.filter_by(status=1).all()
    
    if request.method == 'POST':
        customer_id = int(request.form['customer_id'])
        # accept invoice_no/invoice_date from form if present but store into Receivable fields
        invoice_no = request.form.get('invoice_no')
        invoice_date_str = request.form.get('invoice_date')
        invoice_date = datetime.strptime(invoice_date_str, '%Y-%m-%d').date() if invoice_date_str else None
        due_date_str = request.form.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        amount = float(request.form['amount'])
        description = request.form['description']
        # Map to Receivable model (store amount and due_date). created_at will default to now;
        # if invoice_date provided, set created_at to that date/time.
        new_invoice = Receivable(
            customer_id=customer_id,
            amount=amount,
            balance=amount,
            due_date=due_date,
            status=1
        )
        if invoice_date:
            # set created_at to invoice_date at midnight
            from datetime import datetime as _dt
            new_invoice.created_at = _dt.combine(invoice_date, _dt.min.time())
        
        db.session.add(new_invoice)
        db.session.commit()
        flash('应收账款发票创建成功', 'success')
        return redirect(url_for('arap.ar_invoices'))
    
    return render_template('arap/ar_invoice_form.html', title='添加应收账款发票', customers=customers)

# 应付账款
@arap.route('/ap/invoices')
@login_required
def ap_invoices():
    invoices = Payable.query.all()
    return render_template('arap/ap_invoice_list.html', invoices=invoices)

@arap.route('/ap/invoice/add', methods=['GET', 'POST'])
@login_required
def add_ap_invoice():
    suppliers = Supplier.query.filter_by(status=1).all()
    
    if request.method == 'POST':
        supplier_id = int(request.form['supplier_id'])
        invoice_no = request.form.get('invoice_no')
        invoice_date_str = request.form.get('invoice_date')
        invoice_date = datetime.strptime(invoice_date_str, '%Y-%m-%d').date() if invoice_date_str else None
        due_date_str = request.form.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        amount = float(request.form['amount'])
        description = request.form['description']
        new_invoice = Payable(
            supplier_id=supplier_id,
            amount=amount,
            balance=amount,
            due_date=due_date,
            status=1
        )
        if invoice_date:
            from datetime import datetime as _dt
            new_invoice.created_at = _dt.combine(invoice_date, _dt.min.time())
        
        db.session.add(new_invoice)
        db.session.commit()
        flash('应付账款发票创建成功', 'success')
        return redirect(url_for('arap.ap_invoices'))
    
    return render_template('arap/ap_invoice_form.html', title='添加应付账款发票', suppliers=suppliers)

# 收款管理
@arap.route('/ar/payments')
@login_required
def ar_payments():
    payments = Receipt.query.all()
    return render_template('arap/ar_payment_list.html', payments=payments)

@arap.route('/ar/payment/add', methods=['GET', 'POST'])
@login_required
def add_ar_payment():
    invoices = Receivable.query.filter(Receivable.status==1, Receivable.balance>0).all()
    
    if request.method == 'POST':
        invoice_id = int(request.form['invoice_id'])
        payment_date = datetime.strptime(request.form['payment_date'], '%Y-%m-%d').date()
        amount = float(request.form['amount'])
        method = int(request.form['method'])
        reference = request.form.get('reference')
        account_id = int(request.form.get('account_id', 1))
        
        # 更新发票余额
        invoice = Receivable.query.get(invoice_id)
        if invoice.balance < amount:
            flash('付款金额不能超过发票余额', 'error')
            return redirect(url_for('arap.add_ar_payment'))
        
        invoice.balance -= amount
        
        # 创建收款记录
        new_payment = Receipt(
            receivable_id=invoice_id,
            customer_id=invoice.customer_id,
            receipt_date=payment_date,
            amount=amount,
            account_id=account_id,
            remark=reference,
            created_by=current_user.user_id
        )
        
        db.session.add(new_payment)
        db.session.commit()
        flash('收款记录添加成功', 'success')
        return redirect(url_for('arap.ar_payments'))
    
    return render_template('arap/ar_payment_form.html', title='添加收款记录', invoices=invoices)

# 付款管理
@arap.route('/ap/payments')
@login_required
def ap_payments():
    payments = Payment.query.all()
    return render_template('arap/ap_payment_list.html', payments=payments)

@arap.route('/ap/payment/add', methods=['GET', 'POST'])
@login_required
def add_ap_payment():
    invoices = Payable.query.filter(Payable.status==1, Payable.balance>0).all()
    
    if request.method == 'POST':
        invoice_id = int(request.form['invoice_id'])
        payment_date = datetime.strptime(request.form['payment_date'], '%Y-%m-%d').date()
        amount = float(request.form['amount'])
        method = int(request.form['method'])
        reference = request.form.get('reference')
        account_id = int(request.form.get('account_id', 1))
        
        # 更新发票余额
        invoice = Payable.query.get(invoice_id)
        if invoice.balance < amount:
            flash('付款金额不能超过发票余额', 'error')
            return redirect(url_for('arap.add_ap_payment'))
        
        invoice.balance -= amount
        
        # 创建付款记录
        new_payment = Payment(
            payable_id=invoice_id,
            supplier_id=invoice.supplier_id,
            payment_date=payment_date,
            amount=amount,
            account_id=account_id,
            remark=reference,
            created_by=current_user.user_id
        )
        
        db.session.add(new_payment)
        db.session.commit()
        flash('付款记录添加成功', 'success')
        return redirect(url_for('arap.ap_payments'))
    
    return render_template('arap/ap_payment_form.html', title='添加付款记录', invoices=invoices)