from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import QualityTest, QualityTestItem, SeedBatch
from datetime import datetime
from app.quality_control import quality_control

# 质量检测列表
@quality_control.route('/')
@login_required
def index():
    tests = QualityTest.query.all()
    return render_template('quality_control/test_list.html', tests=tests)

# 新建质量检测
@quality_control.route('/add', methods=['GET', 'POST'])
@login_required
def add_test():
    if request.method == 'POST':
        batch_id = request.form['batch_id']
        test_type = request.form['test_type']
        operator = request.form['operator']
        
        # 创建质量检测记录
        new_test = QualityTest(
            batch_id=batch_id,
            test_type=test_type,
            operator=operator
        )
        
        db.session.add(new_test)
        db.session.flush()  # 刷新以获取test_id
        
        # 保存检测项目
        test_item_names = request.form.getlist('test_item_name[]')
        test_values = request.form.getlist('test_value[]')
        units = request.form.getlist('unit[]')
        standard_values = request.form.getlist('standard_value[]')
        is_qualified_list = request.form.getlist('is_qualified[]')
        
        for i in range(len(test_item_names)):
            is_qualified = is_qualified_list[i] == 'on' if i < len(is_qualified_list) else True
            
            test_item = QualityTestItem(
                test_id=new_test.test_id,
                test_item_name=test_item_names[i],
                test_value=test_values[i],
                unit=units[i],
                standard_value=standard_values[i],
                is_qualified=is_qualified
            )
            db.session.add(test_item)
        
        # 计算整体结果
        all_qualified = all([item.is_qualified for item in new_test.test_items])
        new_test.overall_result = "合格" if all_qualified else "不合格"
        
        db.session.commit()
        flash('质量检测记录添加成功', 'success')
        return redirect(url_for('quality_control.index'))
    
    batches = SeedBatch.query.all()
    # 默认检测项目
    default_test_items = [
        {"name": "发芽率", "unit": "%", "standard": ">=85%"},
        {"name": "纯度", "unit": "%", "standard": ">=98%"},
        {"name": "净度", "unit": "%", "standard": ">=99%"},
        {"name": "水分", "unit": "%", "standard": "<=13%"}
    ]
    return render_template('quality_control/add_test.html', batches=batches, default_test_items=default_test_items)

# 编辑质量检测
@quality_control.route('/edit/<int:test_id>', methods=['GET', 'POST'])
@login_required
def edit_test(test_id):
    test = QualityTest.query.get_or_404(test_id)
    
    if request.method == 'POST':
        test.batch_id = request.form['batch_id']
        test.test_type = request.form['test_type']
        test.operator = request.form['operator']
        
        # 删除现有检测项目
        for item in test.test_items:
            db.session.delete(item)
        
        # 保存新的检测项目
        test_item_names = request.form.getlist('test_item_name[]')
        test_values = request.form.getlist('test_value[]')
        units = request.form.getlist('unit[]')
        standard_values = request.form.getlist('standard_value[]')
        is_qualified_list = request.form.getlist('is_qualified[]')
        
        for i in range(len(test_item_names)):
            is_qualified = is_qualified_list[i] == 'on' if i < len(is_qualified_list) else True
            
            test_item = QualityTestItem(
                test_id=test.test_id,
                test_item_name=test_item_names[i],
                test_value=test_values[i],
                unit=units[i],
                standard_value=standard_values[i],
                is_qualified=is_qualified
            )
            db.session.add(test_item)
        
        # 计算整体结果
        all_qualified = all([item.is_qualified for item in test.test_items])
        test.overall_result = "合格" if all_qualified else "不合格"
        
        db.session.commit()
        flash('质量检测记录更新成功', 'success')
        return redirect(url_for('quality_control.index'))
    
    batches = SeedBatch.query.all()
    return render_template('quality_control/edit_test.html', test=test, batches=batches)

# 删除质量检测
@quality_control.route('/delete/<int:test_id>', methods=['POST'])
@login_required
def delete_test(test_id):
    test = QualityTest.query.get_or_404(test_id)
    db.session.delete(test)
    db.session.commit()
    flash('质量检测记录删除成功', 'success')
    return redirect(url_for('quality_control.index'))

# 质量检测详情
@quality_control.route('/detail/<int:test_id>')
@login_required
def test_detail(test_id):
    test = QualityTest.query.get_or_404(test_id)
    return render_template('quality_control/test_detail.html', test=test)

# 质量检测报告
@quality_control.route('/report/<int:test_id>')
@login_required
def test_report(test_id):
    test = QualityTest.query.get_or_404(test_id)
    return render_template('quality_control/test_report.html', test=test)