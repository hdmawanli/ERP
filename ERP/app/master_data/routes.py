from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app import db
from app.models import Product, ProductCategory, Unit, Supplier, Customer, Brand, Specification

master_data = Blueprint('master_data', __name__, url_prefix='/master-data')

# 商品管理
@master_data.route('/products')
@login_required
def product_list():
    items = Product.query.all()
    return render_template('master_data/product_list.html', items=items)

# 商品类别管理
@master_data.route('/categories')
@login_required
def category_list():
    categories = ProductCategory.query.all()
    return render_template('master_data/category_list.html', categories=categories)

@master_data.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        parent_id = int(request.form['parent_id']) if request.form['parent_id'] else None
        new_category = ProductCategory(category_name=category_name, parent_id=parent_id)
        db.session.add(new_category)
        db.session.commit()
        flash('商品类别添加成功', 'success')
        return redirect(url_for('master_data.category_list'))
    return render_template('master_data/category_form.html', title='添加商品类别')

@master_data.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = ProductCategory.query.get_or_404(category_id)
    if request.method == 'POST':
        category.category_name = request.form['category_name']
        category.parent_id = int(request.form['parent_id']) if request.form['parent_id'] else None
        db.session.commit()
        flash('商品类别更新成功', 'success')
        return redirect(url_for('master_data.category_list'))
    return render_template('master_data/category_form.html', title='编辑商品类别', category=category)

# 单位管理
@master_data.route('/units')
@login_required
def unit_list():
    units = Unit.query.all()
    return render_template('master_data/unit_list.html', units=units)

@master_data.route('/units/add', methods=['GET', 'POST'])
@login_required
def add_unit():
    if request.method == 'POST':
        unit_code = request.form['unit_code']
        unit_name = request.form['unit_name']
        new_unit = Unit(unit_code=unit_code, unit_name=unit_name)
        db.session.add(new_unit)
        db.session.commit()
        flash('单位添加成功', 'success')
        return redirect(url_for('master_data.unit_list'))
    return render_template('master_data/unit_form.html', title='添加单位')

@master_data.route('/units/edit/<int:unit_id>', methods=['GET', 'POST'])
@login_required
def edit_unit(unit_id):
    unit = Unit.query.get_or_404(unit_id)
    if request.method == 'POST':
        unit.unit_code = request.form['unit_code']
        unit.unit_name = request.form['unit_name']
        db.session.commit()
        flash('单位更新成功', 'success')
        return redirect(url_for('master_data.unit_list'))
    return render_template('master_data/unit_form.html', title='编辑单位', unit=unit)

# 供应商管理
@master_data.route('/suppliers')
@login_required
def supplier_list():
    suppliers = Supplier.query.all()
    return render_template('master_data/supplier_list.html', suppliers=suppliers)

# 客户管理
@master_data.route('/customers')
@login_required
def customer_list():
    customers = Customer.query.all()
    return render_template('master_data/customer_list.html', customers=customers)

# 品牌管理
@master_data.route('/brands')
@login_required
def brand_list():
    brands = Brand.query.all()
    return render_template('master_data/brand_list.html', brands=brands)

@master_data.route('/brands/add', methods=['GET', 'POST'])
@login_required
def add_brand():
    if request.method == 'POST':
        brand_name = request.form['brand_name']
        new_brand = Brand(brand_name=brand_name)
        db.session.add(new_brand)
        db.session.commit()
        flash('品牌添加成功', 'success')
        return redirect(url_for('master_data.brand_list'))
    return render_template('master_data/brand_form.html', title='添加品牌')

@master_data.route('/brands/edit/<int:brand_id>', methods=['GET', 'POST'])
@login_required
def edit_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    if request.method == 'POST':
        brand.brand_name = request.form['brand_name']
        db.session.commit()
        flash('品牌更新成功', 'success')
        return redirect(url_for('master_data.brand_list'))
    return render_template('master_data/brand_form.html', title='编辑品牌', brand=brand)

# 规格管理
@master_data.route('/specifications')
@login_required
def specification_list():
    specifications = Specification.query.all()
    return render_template('master_data/specification_list.html', specifications=specifications)

@master_data.route('/specifications/add', methods=['GET', 'POST'])
@login_required
def add_specification():
    if request.method == 'POST':
        spec_name = request.form['spec_name']
        new_spec = Specification(spec_name=spec_name)
        db.session.add(new_spec)
        db.session.commit()
        flash('规格添加成功', 'success')
        return redirect(url_for('master_data.specification_list'))
    return render_template('master_data/specification_form.html', title='添加规格')

@master_data.route('/specifications/edit/<int:spec_id>', methods=['GET', 'POST'])
@login_required
def edit_specification(spec_id):
    spec = Specification.query.get_or_404(spec_id)
    if request.method == 'POST':
        spec.spec_name = request.form['spec_name']
        db.session.commit()
        flash('规格更新成功', 'success')
        return redirect(url_for('master_data.specification_list'))
    return render_template('master_data/specification_form.html', title='编辑规格', spec=spec)