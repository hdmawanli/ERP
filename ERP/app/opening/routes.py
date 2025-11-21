from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import OpeningBankBalance as OpeningBalanceBank, OpeningReceivable as OpeningBalanceAR, OpeningPayable as OpeningBalanceAP, OpeningProductStock, OpeningMaterialStock, OpeningBalanceInventory
from app.forms import OpeningInventoryForm
from datetime import datetime

from app.opening import opening

# 期初管理首页（在文件末尾有完整实现，删除此处重复的简易实现）

# 银行期初余额管理
@opening.route('/bank')
@login_required
def bank_opening():
    balances = OpeningBalanceBank.query.all()
    return render_template('opening/bank_list.html', balances=balances)

@opening.route('/bank/add', methods=['GET', 'POST'])
@login_required
def add_bank_opening():
    if request.method == 'POST':
        account_name = request.form['account_name']
        bank_name = request.form['bank_name']
        account_number = request.form['account_number']
        balance = float(request.form['balance']) if request.form['balance'] else 0.00
        opening_date = datetime.strptime(request.form['opening_date'], '%Y-%m-%d').date()
        description = request.form['description']
        
        new_balance = OpeningBalanceBank(
            account_name=account_name,
            bank_name=bank_name,
            account_number=account_number,
            balance=balance,
            opening_date=opening_date,
            description=description
        )
        
        db.session.add(new_balance)
        db.session.commit()
        flash('银行期初余额添加成功', 'success')
        return redirect(url_for('opening.bank_opening'))
    
    return render_template('opening/bank_form.html', title='添加银行期初余额')

@opening.route('/bank/edit/<int:balance_id>', methods=['GET', 'POST'])
@login_required
def edit_bank_opening(balance_id):
    balance = OpeningBalanceBank.query.get_or_404(balance_id)
    
    if request.method == 'POST':
        balance.account_name = request.form['account_name']
        balance.bank_name = request.form['bank_name']
        balance.account_number = request.form['account_number']
        balance.balance = float(request.form['balance']) if request.form['balance'] else 0.00
        balance.opening_date = datetime.strptime(request.form['opening_date'], '%Y-%m-%d').date()
        balance.description = request.form['description']
        
        db.session.commit()
        flash('银行期初余额更新成功', 'success')
        return redirect(url_for('opening.bank_opening'))
    
    return render_template('opening/bank_form.html', title='编辑银行期初余额', balance=balance)

# 应收期初余额管理
@opening.route('/ar')
@login_required
def ar_opening():
    balances = OpeningBalanceAR.query.all()
    return render_template('opening/ar_list.html', balances=balances)

@opening.route('/ar/add', methods=['GET', 'POST'])
@login_required
def add_ar_opening():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        amount = float(request.form['amount']) if request.form['amount'] else 0.00
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
        opening_date = datetime.strptime(request.form['opening_date'], '%Y-%m-%d').date()
        description = request.form['description']
        
        new_balance = OpeningBalanceAR(
            customer_name=customer_name,
            amount=amount,
            due_date=due_date,
            opening_date=opening_date,
            description=description
        )
        
        db.session.add(new_balance)
        db.session.commit()
        flash('应收期初余额添加成功', 'success')
        return redirect(url_for('opening.ar_opening'))
    
    return render_template('opening/ar_form.html', title='添加应收期初余额')

@opening.route('/ar/edit/<int:balance_id>', methods=['GET', 'POST'])
@login_required
def edit_ar_opening(balance_id):
    balance = OpeningBalanceAR.query.get_or_404(balance_id)
    
    if request.method == 'POST':
        balance.customer_name = request.form['customer_name']
        balance.amount = float(request.form['amount']) if request.form['amount'] else 0.00
        balance.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
        balance.opening_date = datetime.strptime(request.form['opening_date'], '%Y-%m-%d').date()
        balance.description = request.form['description']
        
        db.session.commit()
        flash('应收期初余额更新成功', 'success')
        return redirect(url_for('opening.ar_opening'))
    
    return render_template('opening/ar_form.html', title='编辑应收期初余额', balance=balance)

# 应付期初余额管理
@opening.route('/ap')
@login_required
def ap_opening():
    balances = OpeningBalanceAP.query.all()
    return render_template('opening/ap_list.html', balances=balances)

@opening.route('/ap/add', methods=['GET', 'POST'])
@login_required
def add_ap_opening():
    if request.method == 'POST':
        supplier_name = request.form['supplier_name']
        amount = float(request.form['amount']) if request.form['amount'] else 0.00
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
        opening_date = datetime.strptime(request.form['opening_date'], '%Y-%m-%d').date()
        description = request.form['description']
        
        new_balance = OpeningBalanceAP(
            supplier_name=supplier_name,
            amount=amount,
            due_date=due_date,
            opening_date=opening_date,
            description=description
        )
        
        db.session.add(new_balance)
        db.session.commit()
        flash('应付期初余额添加成功', 'success')
        return redirect(url_for('opening.ap_opening'))
    
    return render_template('opening/ap_form.html', title='添加应付期初余额')

@opening.route('/ap/edit/<int:balance_id>', methods=['GET', 'POST'])
@login_required
def edit_ap_opening(balance_id):
    balance = OpeningBalanceAP.query.get_or_404(balance_id)
    
    if request.method == 'POST':
        balance.supplier_name = request.form['supplier_name']
        balance.amount = float(request.form['amount']) if request.form['amount'] else 0.00
        balance.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
        balance.opening_date = datetime.strptime(request.form['opening_date'], '%Y-%m-%d').date()
        balance.description = request.form['description']
        
        db.session.commit()
        flash('应付期初余额更新成功', 'success')
        return redirect(url_for('opening.ap_opening'))
    
    return render_template('opening/ap_form.html', title='编辑应付期初余额', balance=balance)

# 库存期初余额管理
@opening.route('/inventory')
@login_required
def inventory_opening():
    balances = OpeningBalanceInventory.query.all()
    return render_template('opening/inventory_list.html', balances=balances)

@opening.route('/inventory/add', methods=['GET', 'POST'])
@login_required
def add_inventory_opening():
    form = OpeningInventoryForm()
    if form.validate_on_submit():
        opening_balance = OpeningBalanceInventory(
            item_code=form.item_code.data,
            item_name=form.item_name.data,
            spec=form.spec.data,
            unit=form.unit.data,
            quantity=form.quantity.data,
            unit_cost=form.unit_cost.data,
            amount=form.quantity.data * form.unit_cost.data,
            opening_date=form.opening_date.data,
            description=form.description.data,
            created_by=current_user.user_id
        )
        
        db.session.add(opening_balance)
        db.session.commit()
        
        flash('库存期初余额添加成功', 'success')
        return redirect(url_for('opening.inventory_opening'))
    
    return render_template('opening/inventory_form.html', title='添加库存期初余额', form=form)

@opening.route('/inventory/edit/<int:balance_id>', methods=['GET', 'POST'])
@login_required
def edit_inventory_opening(balance_id):
    balance = OpeningBalanceInventory.query.get_or_404(balance_id)
    form = OpeningInventoryForm(obj=balance)
    
    if form.validate_on_submit():
        form.populate_obj(balance)
        balance.amount = balance.quantity * balance.unit_cost
        
        db.session.commit()
        flash('库存期初余额更新成功', 'success')
        return redirect(url_for('opening.inventory_opening'))
    
    return render_template('opening/inventory_form.html', title='编辑库存期初余额', balance=balance, form=form)

@opening.route('/')
@login_required
def index():
    # 显示所有期初余额统计
    total_bank = db.session.query(db.func.sum(OpeningBalanceBank.balance)).scalar() or 0
    total_ar = db.session.query(db.func.sum(OpeningBalanceAR.amount)).scalar() or 0
    total_ap = db.session.query(db.func.sum(OpeningBalanceAP.amount)).scalar() or 0
    total_inventory = db.session.query(db.func.sum(OpeningBalanceInventory.amount)).scalar() or 0
    
    return render_template('opening/index.html', total_bank=total_bank, total_ar=total_ar, total_ap=total_ap, total_inventory=total_inventory)