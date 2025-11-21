from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import BankAccount, BankFlow
from datetime import datetime
from app.bank import bank

# 银行账户管理
@bank.route('/')
@login_required
def index():
    accounts = BankAccount.query.all()
    return render_template('bank/account_list.html', accounts=accounts)

@bank.route('/account/add', methods=['GET', 'POST'])
@login_required
def add_account():
    if request.method == 'POST':
        account_name = request.form['account_name']
        bank_name = request.form['bank_name']
        account_number = request.form['account_number']
        balance = float(request.form['balance']) if request.form['balance'] else 0.00
        
        new_account = BankAccount(
            account_name=account_name,
            bank_name=bank_name,
            account_number=account_number,
            balance=balance,
            status=1
        )
        
        db.session.add(new_account)
        db.session.commit()
        flash('银行账户创建成功', 'success')
        return redirect(url_for('bank.index'))
    
    return render_template('bank/account_form.html', title='添加银行账户')

@bank.route('/account/edit/<int:account_id>', methods=['GET', 'POST'])
@login_required
def edit_account(account_id):
    account = BankAccount.query.get_or_404(account_id)
    
    if request.method == 'POST':
        account.account_name = request.form['account_name']
        account.bank_name = request.form['bank_name']
        account.account_number = request.form['account_number']
        account.balance = float(request.form['balance']) if request.form['balance'] else 0.00
        
        db.session.commit()
        flash('银行账户更新成功', 'success')
        return redirect(url_for('bank.index'))
    
    return render_template('bank/account_form.html', title='编辑银行账户', account=account)

@bank.route('/account/delete/<int:account_id>')
@login_required
def delete_account(account_id):
    account = BankAccount.query.get_or_404(account_id)
    account.status = 0  # 软删除
    db.session.commit()
    flash('银行账户已删除', 'success')
    return redirect(url_for('bank.index'))

# 银行流水管理
@bank.route('/flows')
@login_required
def flows():
    account_id = request.args.get('account_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = BankFlow.query
    
    if account_id:
        query = query.filter_by(account_id=int(account_id))
    
    if start_date and end_date:
        query = query.filter(BankFlow.flow_date.between(start_date, end_date))
    
    flows = query.order_by(BankFlow.flow_date.desc()).all()
    accounts = BankAccount.query.filter_by(status=1).all()
    
    return render_template('bank/flow_list.html', flows=flows, accounts=accounts)

@bank.route('/flow/add', methods=['GET', 'POST'])
@login_required
def add_flow():
    accounts = BankAccount.query.filter_by(status=1).all()
    
    if request.method == 'POST':
        account_id = int(request.form['account_id'])
        flow_date = datetime.strptime(request.form['flow_date'], '%Y-%m-%d').date()
        type = int(request.form['type'])
        amount = float(request.form['amount'])
        summary = request.form['summary']
        
        # 更新银行账户余额
        account = BankAccount.query.get(account_id)
        if type == 1:  # 收入
            account.balance += amount
        elif type == 2:  # 支出
            account.balance -= amount
        
        # 创建银行流水
        new_flow = BankFlow(
            account_id=account_id,
            flow_date=flow_date,
            type=type,
            amount=amount,
            summary=summary,
            created_by=current_user.user_id
        )
        
        db.session.add(new_flow)
        db.session.commit()
        flash('银行流水添加成功', 'success')
        return redirect(url_for('bank.flows'))
    
    return render_template('bank/flow_form.html', accounts=accounts, title='添加银行流水')

@bank.route('/account/flows/<int:account_id>')
@login_required
def account_flows(account_id):
    account = BankAccount.query.get_or_404(account_id)
    flows = BankFlow.query.filter_by(account_id=account_id).order_by(BankFlow.flow_date.desc()).all()
    accounts = BankAccount.query.filter_by(status=1).all()
    
    return render_template('bank/flow_list.html', flows=flows, accounts=accounts, selected_account=account_id)