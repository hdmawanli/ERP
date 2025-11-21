from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import BreedingPlan, FieldManagement, HarvestManagement, SeedBatch
from datetime import datetime
from app.production import production

# 制种计划列表
@production.route('/')
@login_required
def plan_list():
    plans = BreedingPlan.query.all()
    return render_template('production/plan_list.html', plans=plans)

# 新建制种计划
@production.route('/add_plan', methods=['GET', 'POST'])
@login_required
def add_plan():
    if request.method == 'POST':
        plan_code = request.form['plan_code']
        crop_type = request.form['crop_type']
        variety = request.form['variety']
        planned_area = request.form['planned_area']
        planned_yield = request.form['planned_yield']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        status = request.form['status']
        operator = current_user.real_name
        
        # 创建新的制种计划
        new_plan = BreedingPlan(
            plan_code=plan_code,
            crop_type=crop_type,
            variety=variety,
            planned_area=planned_area,
            planned_yield=planned_yield,
            start_date=start_date,
            end_date=end_date,
            status=status,
            operator=operator
        )
        
        db.session.add(new_plan)
        db.session.commit()
        flash('制种计划添加成功', 'success')
        return redirect(url_for('production.plan_list'))
    
    return render_template('production/add_plan.html')

# 编辑制种计划
@production.route('/edit_plan/<int:plan_id>', methods=['GET', 'POST'])
@login_required
def edit_plan(plan_id):
    plan = BreedingPlan.query.get_or_404(plan_id)
    
    if request.method == 'POST':
        plan.plan_code = request.form['plan_code']
        plan.crop_type = request.form['crop_type']
        plan.variety = request.form['variety']
        plan.planned_area = request.form['planned_area']
        plan.planned_yield = request.form['planned_yield']
        plan.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        plan.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        plan.status = request.form['status']
        
        db.session.commit()
        flash('制种计划更新成功', 'success')
        return redirect(url_for('production.plan_list'))
    
    return render_template('production/edit_plan.html', plan=plan)

# 删除制种计划
@production.route('/delete_plan/<int:plan_id>', methods=['POST'])
@login_required
def delete_plan(plan_id):
    plan = BreedingPlan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    flash('制种计划删除成功', 'success')
    return redirect(url_for('production.plan_list'))

# 田间管理记录列表
@production.route('/field_list')
@login_required
def field_list():
    fields = FieldManagement.query.all()
    return render_template('production/field_list.html', fields=fields)

# 新建田间管理记录
@production.route('/add_field', methods=['GET', 'POST'])
@login_required
def add_field():
    if request.method == 'POST':
        plan_id = request.form['plan_id']
        field_name = request.form['field_name']
        area = request.form['area']
        planting_date = datetime.strptime(request.form['planting_date'], '%Y-%m-%d').date()
        sowing_rate = request.form['sowing_rate']
        fertilizer_usage = request.form['fertilizer_usage']
        pesticide_usage = request.form['pesticide_usage']
        irrigation_record = request.form['irrigation_record']
        growth_stage = request.form['growth_stage']
        inspection_date = datetime.strptime(request.form['inspection_date'], '%Y-%m-%d').date() if request.form['inspection_date'] else None
        inspection_results = request.form['inspection_results']
        operator = current_user.real_name
        
        new_field = FieldManagement(
            plan_id=plan_id,
            field_name=field_name,
            area=area,
            planting_date=planting_date,
            sowing_rate=sowing_rate,
            fertilizer_usage=fertilizer_usage,
            pesticide_usage=pesticide_usage,
            irrigation_record=irrigation_record,
            growth_stage=growth_stage,
            inspection_date=inspection_date,
            inspection_results=inspection_results,
            operator=operator
        )
        
        db.session.add(new_field)
        db.session.commit()
        flash('田间管理记录添加成功', 'success')
        return redirect(url_for('production.field_list'))
    
    plans = BreedingPlan.query.all()
    return render_template('production/add_field.html', plans=plans)

# 编辑田间管理记录
@production.route('/edit_field/<int:field_id>', methods=['GET', 'POST'])
@login_required
def edit_field(field_id):
    field = FieldManagement.query.get_or_404(field_id)
    
    if request.method == 'POST':
        field.plan_id = request.form['plan_id']
        field.field_name = request.form['field_name']
        field.area = request.form['area']
        field.planting_date = datetime.strptime(request.form['planting_date'], '%Y-%m-%d').date()
        field.sowing_rate = request.form['sowing_rate']
        field.fertilizer_usage = request.form['fertilizer_usage']
        field.pesticide_usage = request.form['pesticide_usage']
        field.irrigation_record = request.form['irrigation_record']
        field.growth_stage = request.form['growth_stage']
        field.inspection_date = datetime.strptime(request.form['inspection_date'], '%Y-%m-%d').date() if request.form['inspection_date'] else None
        field.inspection_results = request.form['inspection_results']
        
        db.session.commit()
        flash('田间管理记录更新成功', 'success')
        return redirect(url_for('production.field_list'))
    
    plans = BreedingPlan.query.all()
    return render_template('production/edit_field.html', field=field, plans=plans)

# 删除田间管理记录
@production.route('/delete_field/<int:field_id>', methods=['POST'])
@login_required
def delete_field(field_id):
    field = FieldManagement.query.get_or_404(field_id)
    db.session.delete(field)
    db.session.commit()
    flash('田间管理记录删除成功', 'success')
    return redirect(url_for('production.field_list'))

# 收获管理记录列表
@production.route('/harvest_list')
@login_required
def harvest_list():
    harvests = HarvestManagement.query.all()
    return render_template('production/harvest_list.html', harvests=harvests)

# 新建收获管理记录
@production.route('/add_harvest', methods=['GET', 'POST'])
@login_required
def add_harvest():
    if request.method == 'POST':
        plan_id = request.form['plan_id']
        harvest_date = datetime.strptime(request.form['harvest_date'], '%Y-%m-%d').date()
        actual_area = request.form['actual_area']
        actual_yield = request.form['actual_yield']
        moisture_content = request.form['moisture_content']
        impurity_rate = request.form['impurity_rate']
        batch_id = request.form['batch_id'] if request.form['batch_id'] else None
        operator = current_user.real_name
        
        new_harvest = HarvestManagement(
            plan_id=plan_id,
            harvest_date=harvest_date,
            actual_area=actual_area,
            actual_yield=actual_yield,
            moisture_content=moisture_content,
            impurity_rate=impurity_rate,
            batch_id=batch_id,
            operator=operator
        )
        
        db.session.add(new_harvest)
        db.session.commit()
        flash('收获管理记录添加成功', 'success')
        return redirect(url_for('production.harvest_list'))
    
    plans = BreedingPlan.query.all()
    batches = SeedBatch.query.all()
    return render_template('production/add_harvest.html', plans=plans, batches=batches)

# 编辑收获管理记录
@production.route('/edit_harvest/<int:harvest_id>', methods=['GET', 'POST'])
@login_required
def edit_harvest(harvest_id):
    harvest = HarvestManagement.query.get_or_404(harvest_id)
    
    if request.method == 'POST':
        harvest.plan_id = request.form['plan_id']
        harvest.harvest_date = datetime.strptime(request.form['harvest_date'], '%Y-%m-%d').date()
        harvest.actual_area = request.form['actual_area']
        harvest.actual_yield = request.form['actual_yield']
        harvest.moisture_content = request.form['moisture_content']
        harvest.impurity_rate = request.form['impurity_rate']
        harvest.batch_id = request.form['batch_id'] if request.form['batch_id'] else None
        
        db.session.commit()
        flash('收获管理记录更新成功', 'success')
        return redirect(url_for('production.harvest_list'))
    
    plans = BreedingPlan.query.all()
    batches = SeedBatch.query.all()
    return render_template('production/edit_harvest.html', harvest=harvest, plans=plans, batches=batches)

# 删除收获管理记录
@production.route('/delete_harvest/<int:harvest_id>', methods=['POST'])
@login_required
def delete_harvest(harvest_id):
    harvest = HarvestManagement.query.get_or_404(harvest_id)
    db.session.delete(harvest)
    db.session.commit()
    flash('收获管理记录删除成功', 'success')
    return redirect(url_for('production.harvest_list'))

# 制种计划详情
@production.route('/plan_detail/<int:plan_id>')
@login_required
def plan_detail(plan_id):
    plan = BreedingPlan.query.get_or_404(plan_id)
    return render_template('production/plan_detail.html', plan=plan)

# 生产报表
@production.route('/report')
@login_required
def production_report():
    plans = BreedingPlan.query.all()
    return render_template('production/production_report.html', plans=plans)