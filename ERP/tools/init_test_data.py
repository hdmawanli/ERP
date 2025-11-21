#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app, db
from datetime import datetime

app = create_app()

with app.app_context():
    print("开始初始化测试数据...")
    
    # 1. 初始化品牌数据
    from app.models import Brand
    brands = [
        {'brand_code': 'BR001', 'brand_name': '联想'}, 
        {'brand_code': 'BR002', 'brand_name': '惠普'},
        {'brand_code': 'BR003', 'brand_name': '小米'},
        {'brand_code': 'BR004', 'brand_name': '华为'},
        {'brand_code': 'BR005', 'brand_name': '苹果'}
    ]
    for brand_data in brands:
        brand = Brand.query.filter_by(brand_code=brand_data['brand_code']).first()
        if not brand:
            brand = Brand(**brand_data)
            db.session.add(brand)
    db.session.commit()
    print("品牌数据初始化完成")
    
    # 2. 初始化规格数据
    from app.models import Specification
    specifications = [
        {'spec_code': 'SP001', 'spec_name': '14英寸笔记本'},
        {'spec_code': 'SP002', 'spec_name': '15.6英寸笔记本'},
        {'spec_code': 'SP003', 'spec_name': '无线蓝牙'},
        {'spec_code': 'SP004', 'spec_name': '有线USB'},
        {'spec_code': 'SP005', 'spec_name': '500g/袋'},
        {'spec_code': 'SP006', 'spec_name': '1000g/袋'}
    ]
    for spec_data in specifications:
        spec = Specification.query.filter_by(spec_code=spec_data['spec_code']).first()
        if not spec:
            spec = Specification(**spec_data)
            db.session.add(spec)
    db.session.commit()
    print("规格数据初始化完成")
    
    # 3. 更新现有产品，添加品牌和规格
    from app.models import Product
    
    # 获取品牌和规格
    lenovo_brand = Brand.query.filter_by(brand_code='BR001').first()
    hp_brand = Brand.query.filter_by(brand_code='BR002').first()
    xiaomi_brand = Brand.query.filter_by(brand_code='BR003').first()
    
    spec_14inch = Specification.query.filter_by(spec_code='SP001').first()
    spec_15inch = Specification.query.filter_by(spec_code='SP002').first()
    spec_wireless = Specification.query.filter_by(spec_code='SP003').first()
    
    # 更新产品
    product_prod001 = Product.query.filter_by(product_code='PROD001').first()
    if product_prod001:
        product_prod001.brand_id = lenovo_brand.brand_id if lenovo_brand else None
        product_prod001.spec_id = spec_14inch.spec_id if spec_14inch else None
        db.session.add(product_prod001)
    
    product_prod002 = Product.query.filter_by(product_code='PROD002').first()
    if product_prod002:
        product_prod002.brand_id = hp_brand.brand_id if hp_brand else None
        product_prod002.spec_id = spec_wireless.spec_id if spec_wireless else None
        db.session.add(product_prod002)
    
    # 添加新的测试产品，包含品牌和规格
    from app.models import ProductCategory, Unit
    
    # 获取分类和单位
    electronics_cat = ProductCategory.query.filter_by(category_name='电子产品').first()
    office_cat = ProductCategory.query.filter_by(category_name='办公用品').first()
    unit_pcs = Unit.query.filter_by(unit_code='PCS').first()
    unit_box = Unit.query.filter_by(unit_code='BOX').first()
    
    new_products = [
        {
            'product_code': 'PROD006', 
            'product_name': '小米手机', 
            'category_id': electronics_cat.category_id if electronics_cat else None,
            'unit_id': unit_pcs.unit_id, 
            'purchase_price': 3000.00, 
            'sale_price': 3500.00,
            'brand_id': xiaomi_brand.brand_id if xiaomi_brand else None,
            'spec_id': None
        },
        {
            'product_code': 'PROD007', 
            'product_name': '华为平板', 
            'category_id': electronics_cat.category_id if electronics_cat else None,
            'unit_id': unit_pcs.unit_id, 
            'purchase_price': 2000.00, 
            'sale_price': 2500.00,
            'brand_id': None,
            'spec_id': None
        },
        {
            'product_code': 'PROD008', 
            'product_name': '苹果笔记本', 
            'category_id': electronics_cat.category_id if electronics_cat else None,
            'unit_id': unit_pcs.unit_id, 
            'purchase_price': 10000.00, 
            'sale_price': 12000.00,
            'brand_id': None,
            'spec_id': None
        }
    ]
    
    for product_data in new_products:
        product = Product.query.filter_by(product_code=product_data['product_code']).first()
        if not product:
            product = Product(**product_data)
            db.session.add(product)
    
    db.session.commit()
    print("产品数据更新完成")
    
    # 4. 初始化库存期初数据
    from app.models import InventoryBalance, Warehouse
    
    # 获取仓库
    main_warehouse = Warehouse.query.filter_by(warehouse_code='WH001').first()
    
    # 获取所有产品
    all_products = Product.query.all()
    main_warehouse = Warehouse.query.first()
    
    inventory_balances = []
    for product in all_products:
        inventory_balances.append({
            'type': 'product',
            'item_id': product.product_id,
            'batch_id': None,
            'warehouse_id': main_warehouse.warehouse_id if main_warehouse else 1,
            'quantity': 100,  # 默认库存数量
            'cost_price': product.purchase_price,  # 使用产品的采购价格作为单位成本
            'amount': product.purchase_price * 100  # 总成本等于单位成本乘以总数量
        })
    
    for inv_data in inventory_balances:
        inv = InventoryBalance.query.filter_by(
            type='product',
            item_id=inv_data['item_id'],
            warehouse_id=inv_data['warehouse_id']
        ).first()
        if not inv:
            inv = InventoryBalance(**inv_data)
            db.session.add(inv)
    
    db.session.commit()
    print("库存期初数据初始化完成")
    
    print("所有测试数据初始化完成！")