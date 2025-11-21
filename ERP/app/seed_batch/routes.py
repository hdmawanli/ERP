from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import SeedBatch, SeedBatchTrace, Product
from datetime import datetime, timedelta
from app.seed_batch import seed_batch

# 批次列表
@seed_batch.route('/')
@login_required
def index():
    batches = SeedBatch.query.all()
    return render_template('seed_batch/batch_list.html', batches=batches)

# 新建批次
@seed_batch.route('/add', methods=['GET', 'POST'])
@login_required
def add_batch():
    if request.method == 'POST':
        product_id = request.form['product_id']
        batch_number = request.form['batch_number']
        production_date = datetime.strptime(request.form['production_date'], '%Y-%m-%d').date()
        shelf_life = int(request.form['shelf_life'])
        storage_conditions = request.form['storage_conditions']
        
        # 计算保质期
        expiration_date = production_date + timedelta(days=shelf_life)
        
        # 检查批次号是否唯一
        existing_batch = SeedBatch.query.filter_by(batch_number=batch_number).first()
        if existing_batch:
            flash('批次号已存在', 'error')
            return redirect(url_for('seed_batch.add_batch'))
        
        new_batch = SeedBatch(
            batch_number=batch_number,
            product_id=product_id,
            production_date=production_date,
            shelf_life=shelf_life,
            expiration_date=expiration_date,
            storage_conditions=storage_conditions,
            status=1
        )
        
        db.session.add(new_batch)
        db.session.commit()
        flash('批次添加成功', 'success')
        return redirect(url_for('seed_batch.index'))
    
    products = Product.query.filter_by(status=1).all()
    return render_template('seed_batch/add_batch.html', products=products)

# 编辑批次
@seed_batch.route('/edit/<int:batch_id>', methods=['GET', 'POST'])
@login_required
def edit_batch(batch_id):
    batch = SeedBatch.query.get_or_404(batch_id)
    
    if request.method == 'POST':
        batch.product_id = request.form['product_id']
        batch.production_date = datetime.strptime(request.form['production_date'], '%Y-%m-%d').date()
        batch.shelf_life = int(request.form['shelf_life'])
        batch.expiration_date = batch.production_date + timedelta(days=batch.shelf_life)
        batch.storage_conditions = request.form['storage_conditions']
        
        # 更新状态
        today = datetime.today().date()
        if batch.expiration_date < today:
            batch.status = 3  # 已过期
        elif batch.expiration_date - today < timedelta(days=30):
            batch.status = 2  # 即将过期
        else:
            batch.status = 1  # 正常
        
        db.session.commit()
        flash('批次更新成功', 'success')
        return redirect(url_for('seed_batch.index'))
    
    products = Product.query.filter_by(status=1).all()
    return render_template('seed_batch/edit_batch.html', batch=batch, products=products)

# 删除批次
@seed_batch.route('/delete/<int:batch_id>', methods=['POST'])
@login_required
def delete_batch(batch_id):
    batch = SeedBatch.query.get_or_404(batch_id)
    db.session.delete(batch)
    db.session.commit()
    flash('批次删除成功', 'success')
    return redirect(url_for('seed_batch.index'))

# 批次详情
@seed_batch.route('/detail/<int:batch_id>')
@login_required
def batch_detail(batch_id):
    batch = SeedBatch.query.get_or_404(batch_id)
    traces = SeedBatchTrace.query.filter_by(batch_id=batch_id).order_by(SeedBatchTrace.trace_date.desc()).all()
    return render_template('seed_batch/batch_detail.html', batch=batch, traces=traces)

# 添加批次溯源记录
@seed_batch.route('/trace/add/<int:batch_id>', methods=['GET', 'POST'])
@login_required
def add_trace(batch_id):
    batch = SeedBatch.query.get_or_404(batch_id)
    
    if request.method == 'POST':
        trace_type = request.form['trace_type']
        trace_date = datetime.strptime(request.form['trace_date'], '%Y-%m-%d').date()
        description = request.form['description']
        operator = request.form['operator']
        
        new_trace = SeedBatchTrace(
            batch_id=batch_id,
            trace_type=trace_type,
            trace_date=trace_date,
            description=description,
            operator=operator
        )
        
        db.session.add(new_trace)
        db.session.commit()
        flash('溯源记录添加成功', 'success')
        return redirect(url_for('seed_batch.batch_detail', batch_id=batch_id))
    
    return render_template('seed_batch/add_trace.html', batch=batch)