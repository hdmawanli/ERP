#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app, db
from datetime import datetime

app = create_app()

with app.app_context():
    print("开始初始化库存相关数据...")
    
    # 初始化产品分类数据
    from app.models import ProductCategory
    product_categories = [
        {'category_name': '电子产品', 'parent_id': None, 'sort_order': 1},
        {'category_name': '办公用品', 'parent_id': None, 'sort_order': 2},
        {'category_name': '家居用品', 'parent_id': None, 'sort_order': 3},
    ]
    for cat_data in product_categories:
        cat = ProductCategory.query.filter_by(category_name=cat_data['category_name']).first()
        if not cat:
            cat = ProductCategory(**cat_data)
            db.session.add(cat)
    db.session.commit()
    print("产品分类数据初始化完成")
    
    # 初始化物料分类数据
    from app.models import MaterialCategory
    material_categories = [
        {'category_name': '原材料', 'parent_id': None, 'sort_order': 1},
        {'category_name': '半成品', 'parent_id': None, 'sort_order': 2},
        {'category_name': '包装材料', 'parent_id': None, 'sort_order': 3},
    ]
    for cat_data in material_categories:
        cat = MaterialCategory.query.filter_by(category_name=cat_data['category_name']).first()
        if not cat:
            cat = MaterialCategory(**cat_data)
            db.session.add(cat)
    db.session.commit()
    print("物料分类数据初始化完成")
    
    # 初始化产品数据
    from app.models import Product, Unit
    
    # 获取单位
    unit_pcs = Unit.query.filter_by(unit_code='PCS').first()
    unit_kg = Unit.query.filter_by(unit_code='KG').first()
    unit_box = Unit.query.filter_by(unit_code='BOX').first()
    unit_set = Unit.query.filter_by(unit_code='SET').first()
    
    if not unit_pcs or not unit_kg or not unit_box or not unit_set:
        print("错误：缺少必要的单位数据")
        sys.exit(1)
    
    # 获取产品分类
    cat_electronics = ProductCategory.query.filter_by(category_name='电子产品').first()
    cat_office = ProductCategory.query.filter_by(category_name='办公用品').first()
    cat_home = ProductCategory.query.filter_by(category_name='家居用品').first()
    
    products = [
        {
            'product_code': 'PROD001', 
            'product_name': '笔记本电脑', 
            'category_id': cat_electronics.category_id if cat_electronics else None,
            'unit_id': unit_pcs.unit_id, 
            'purchase_price': 5000.00, 
            'sale_price': 6500.00
        },
        {
            'product_code': 'PROD002', 
            'product_name': '无线鼠标', 
            'category_id': cat_electronics.category_id if cat_electronics else None,
            'unit_id': unit_pcs.unit_id, 
            'purchase_price': 50.00, 
            'sale_price': 80.00
        },
        {
            'product_code': 'PROD003', 
            'product_name': 'A4打印纸', 
            'category_id': cat_office.category_id if cat_office else None,
            'unit_id': unit_box.unit_id, 
            'purchase_price': 20.00, 
            'sale_price': 35.00
        },
        {
            'product_code': 'PROD004', 
            'product_name': '办公椅', 
            'category_id': cat_office.category_id if cat_office else None,
            'unit_id': unit_pcs.unit_id, 
            'purchase_price': 150.00, 
            'sale_price': 250.00
        },
        {
            'product_code': 'PROD005', 
            'product_name': '床上用品四件套', 
            'category_id': cat_home.category_id if cat_home else None,
            'unit_id': unit_set.unit_id, 
            'purchase_price': 100.00, 
            'sale_price': 200.00
        },
    ]
    
    # 特殊处理床上用品的单位（SET）
    unit_set = Unit.query.filter_by(unit_code='SET').first()
    if unit_set:
        products[4]['unit_id'] = unit_set.unit_id
    
    for prod_data in products:
        if prod_data['category_id'] is None:
            continue
            
        prod = Product.query.filter_by(product_code=prod_data['product_code']).first()
        if not prod:
            prod = Product(**prod_data)
            db.session.add(prod)
    db.session.commit()
    print("产品数据初始化完成")
    
    # 初始化物料数据
    from app.models import Material
    
    # 获取物料分类
    cat_raw = MaterialCategory.query.filter_by(category_name='原材料').first()
    cat_semi = MaterialCategory.query.filter_by(category_name='半成品').first()
    cat_pack = MaterialCategory.query.filter_by(category_name='包装材料').first()
    
    materials = [
        {
            'material_code': 'MAT001', 
            'material_name': '塑料颗粒', 
            'category_id': cat_raw.category_id if cat_raw else None,
            'unit_id': unit_kg.unit_id, 
            'purchase_price': 10.00
        },
        {
            'material_code': 'MAT002', 
            'material_name': '金属零件', 
            'category_id': cat_raw.category_id if cat_raw else None,
            'unit_id': unit_pcs.unit_id, 
            'purchase_price': 5.00
        },
        {
            'material_code': 'MAT003', 
            'material_name': '电路板', 
            'category_id': cat_semi.category_id if cat_semi else None,
            'unit_id': unit_pcs.unit_id, 
            'purchase_price': 50.00
        },
        {
            'material_code': 'MAT004', 
            'material_name': '纸箱', 
            'category_id': cat_pack.category_id if cat_pack else None,
            'unit_id': unit_box.unit_id, 
            'purchase_price': 2.00
        },
    ]
    
    for mat_data in materials:
        if mat_data['category_id'] is None:
            continue
            
        mat = Material.query.filter_by(material_code=mat_data['material_code']).first()
        if not mat:
            mat = Material(**mat_data)
            db.session.add(mat)
    db.session.commit()
    print("物料数据初始化完成")
    
    # 初始化库存期初数据
    from app.models import OpeningBalanceInventory
    
    # 获取仓库
    from app.models import Warehouse
    wh_main = Warehouse.query.filter_by(warehouse_code='WH001').first()
    
    if wh_main:
        opening_inventories = [
            {
                'item_code': 'PROD001', 
                'item_name': '笔记本电脑', 
                'spec': '15.6英寸', 
                'unit': 'PCS', 
                'quantity': 10, 
                'unit_cost': 5000.00, 
                'amount': 50000.00, 
                'created_by': 1
            },
            {
                'item_code': 'PROD002', 
                'item_name': '无线鼠标', 
                'spec': '2.4G', 
                'unit': 'PCS', 
                'quantity': 50, 
                'unit_cost': 50.00, 
                'amount': 2500.00, 
                'created_by': 1
            },
            {
                'item_code': 'PROD003', 
                'item_name': 'A4打印纸', 
                'spec': '70g', 
                'unit': 'BOX', 
                'quantity': 20, 
                'unit_cost': 20.00, 
                'amount': 400.00, 
                'created_by': 1
            },
            {
                'item_code': 'MAT001', 
                'item_name': '塑料颗粒', 
                'spec': 'PP', 
                'unit': 'KG', 
                'quantity': 100, 
                'unit_cost': 10.00, 
                'amount': 1000.00, 
                'created_by': 1
            },
            {
                'item_code': 'MAT002', 
                'item_name': '金属零件', 
                'spec': 'M4', 
                'unit': 'PCS', 
                'quantity': 200, 
                'unit_cost': 5.00, 
                'amount': 1000.00, 
                'created_by': 1
            },
        ]
        
        for inv_data in opening_inventories:
            inv = OpeningBalanceInventory.query.filter_by(item_code=inv_data['item_code']).first()
            if not inv:
                inv = OpeningBalanceInventory(**inv_data)
                db.session.add(inv)
        db.session.commit()
        print("库存期初数据初始化完成")
    else:
        print("警告：未找到主仓库数据，无法初始化库存期初数据")
    
    print("库存相关数据初始化完成！")