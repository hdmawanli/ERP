from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import ExpenseCategory as ExpenseType, Expense as ExpenseEntry, ExpenseAllocation, AccountingSubject
from datetime import datetime
from app.expense import expense

# 费用管理首页
@expense.route('/')
@login_required
def index():
    return redirect(url_for('expense.entries'))

# 费用类型管理
@expense.route('/types')
@login_required
def types():
    expense_types = ExpenseType.query.all()
    return render_template('expense/type_list.html', expense_types=expense_types)

@expense.route('/type/add', methods=['GET', 'POST'])
@login_required
def add_type():
    if request.method == 'POST':
        type_name = request.form['type_name']
        description = request.form['description']
        
        new_type = ExpenseType(
            type_name=type_name,
            description=description,
            status=1
        )
        
        db.session.add(new_type)
        db.session.commit()
        flash('费用类型创建成功', 'success')
        return redirect(url_for('expense.types'))
    
    return render_template('expense/type_form.html', title='添加费用类型')

@expense.route('/type/edit/<int:type_id>', methods=['GET', 'POST'])
@login_required
def edit_type(type_id):
    expense_type = ExpenseType.query.get_or_404(type_id)
    
    if request.method == 'POST':
        expense_type.type_name = request.form['type_name']
        expense_type.description = request.form['description']
        
        db.session.commit()
        flash('费用类型更新成功', 'success')
        return redirect(url_for('expense.types'))
    
    return render_template('expense/type_form.html', title='编辑费用类型', expense_type=expense_type)

# 会计科目管理
@expense.route('/subjects')
@login_required
def subjects():
    subjects = AccountingSubject.query.all()
    return render_template('expense/subject_list.html', subjects=subjects)

@expense.route('/subject/add', methods=['GET', 'POST'])
@login_required
def add_subject():
    if request.method == 'POST':
        subject_code = request.form['subject_code']
        subject_name = request.form['subject_name']
        subject_type = request.form['subject_type']
        
        new_subject = AccountingSubject(
            subject_code=subject_code,
            subject_name=subject_name,
            subject_type=subject_type,
            status=1
        )
        
        db.session.add(new_subject)
        db.session.commit()
        flash('会计科目创建成功', 'success')
        return redirect(url_for('expense.subjects'))
    
    return render_template('expense/subject_form.html', title='添加会计科目')

@expense.route('/subject/edit/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id):
    subject = AccountingSubject.query.get_or_404(subject_id)
    
    if request.method == 'POST':
        subject.subject_code = request.form['subject_code']
        subject.subject_name = request.form['subject_name']
        subject.subject_type = request.form['subject_type']
        
        db.session.commit()
        flash('会计科目更新成功', 'success')
        return redirect(url_for('expense.subjects'))
    
    return render_template('expense/subject_form.html', title='编辑会计科目', subject=subject)

@expense.route('/subject/delete/<int:subject_id>')
@login_required
def delete_subject(subject_id):
    subject = AccountingSubject.query.get_or_404(subject_id)
    subject.status = 0  # 软删除
    db.session.commit()
    flash('会计科目已删除', 'success')
    return redirect(url_for('expense.subjects'))

# 费用录入
@expense.route('/entries')
@login_required
def entries():
    entries = ExpenseEntry.query.all()
    return render_template('expense/entry_list.html', entries=entries)

@expense.route('/entry/add', methods=['GET', 'POST'])
@login_required
def add_entry():
    expense_types = ExpenseType.query.filter_by(status=1).all()
    accounting_subjects = AccountingSubject.query.filter_by(status=1).all()
    
    if request.method == 'POST':
        entry_date = datetime.strptime(request.form['entry_date'], '%Y-%m-%d').date()
        type_id = int(request.form['type_id'])
        subject_id = int(request.form['subject_id'])
        amount = float(request.form['amount'])
        description = request.form['description']
        department_id = int(request.form['department_id'])
        
        new_entry = ExpenseEntry(
            entry_date=entry_date,
            type_id=type_id,
            subject_id=subject_id,
            amount=amount,
            description=description,
            department_id=department_id,
            created_by=current_user.user_id
        )
        
        db.session.add(new_entry)
        db.session.commit()
        flash('费用录入成功', 'success')
        return redirect(url_for('expense.entries'))
    
    return render_template('expense/entry_form.html', title='添加费用录入', expense_types=expense_types, accounting_subjects=accounting_subjects)

@expense.route('/entry/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    entry = ExpenseEntry.query.get_or_404(entry_id)
    expense_types = ExpenseType.query.filter_by(status=1).all()
    accounting_subjects = AccountingSubject.query.filter_by(status=1).all()
    
    if request.method == 'POST':
        entry.entry_date = datetime.strptime(request.form['entry_date'], '%Y-%m-%d').date()
        entry.type_id = int(request.form['type_id'])
        entry.subject_id = int(request.form['subject_id'])
        entry.amount = float(request.form['amount'])
        entry.description = request.form['description']
        entry.department_id = int(request.form['department_id'])
        
        db.session.commit()
        flash('费用更新成功', 'success')
        return redirect(url_for('expense.entries'))
    
    return render_template('expense/entry_form.html', title='编辑费用录入', entry=entry, expense_types=expense_types, accounting_subjects=accounting_subjects)

# 费用分摊
@expense.route('/allocations')
@login_required
def allocations():
    allocations = ExpenseAllocation.query.all()
    return render_template('expense/allocation_list.html', allocations=allocations)

@expense.route('/allocation/add', methods=['GET', 'POST'])
@login_required
def add_allocation():
    entries = ExpenseEntry.query.all()
    
    if request.method == 'POST':
        entry_id = int(request.form['entry_id'])
        allocation_date = datetime.strptime(request.form['allocation_date'], '%Y-%m-%d').date()
        cost_center = request.form['cost_center']
        allocated_amount = float(request.form['allocated_amount'])
        description = request.form['description']
        
        # 验证分摊金额不超过费用金额
        entry = ExpenseEntry.query.get(entry_id)
        total_allocated = db.session.query(db.func.sum(ExpenseAllocation.allocated_amount)).filter_by(entry_id=entry_id).scalar() or 0
        remaining_amount = entry.amount - total_allocated
        
        if allocated_amount > remaining_amount:
            flash('分摊金额不能超过剩余未分摊金额', 'error')
            return redirect(url_for('expense.add_allocation'))
        
        new_allocation = ExpenseAllocation(
            entry_id=entry_id,
            allocation_date=allocation_date,
            cost_center=cost_center,
            allocated_amount=allocated_amount,
            description=description,
            created_by=current_user.user_id
        )
        
        db.session.add(new_allocation)
        db.session.commit()
        flash('费用分摊成功', 'success')
        return redirect(url_for('expense.allocations'))
    
    return render_template('expense/allocation_form.html', title='添加费用分摊', entries=entries)

@expense.route('/allocation/edit/<int:allocation_id>', methods=['GET', 'POST'])
@login_required
def edit_allocation(allocation_id):
    allocation = ExpenseAllocation.query.get_or_404(allocation_id)
    entries = ExpenseEntry.query.all()
    
    if request.method == 'POST':
        old_amount = allocation.allocated_amount
        
        allocation.entry_id = int(request.form['entry_id'])
        allocation.allocation_date = datetime.strptime(request.form['allocation_date'], '%Y-%m-%d').date()
        allocation.cost_center = request.form['cost_center']
        allocation.allocated_amount = float(request.form['allocated_amount'])
        allocation.description = request.form['description']
        
        # 验证分摊金额不超过费用金额
        entry = ExpenseEntry.query.get(allocation.entry_id)
        total_allocated = db.session.query(db.func.sum(ExpenseAllocation.allocated_amount)).filter_by(entry_id=allocation.entry_id).filter(ExpenseAllocation.allocation_id != allocation_id).scalar() or 0
        total_allocated += allocation.allocated_amount
        
        if total_allocated > entry.amount:
            flash('分摊金额总和不能超过费用金额', 'error')
            return redirect(url_for('expense.edit_allocation', allocation_id=allocation_id))
        
        db.session.commit()
        flash('费用分摊更新成功', 'success')
        return redirect(url_for('expense.allocations'))
    
    return render_template('expense/allocation_form.html', title='编辑费用分摊', allocation=allocation, entries=entries)