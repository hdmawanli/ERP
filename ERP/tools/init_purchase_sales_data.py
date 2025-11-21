#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app, db
from datetime import datetime

app = create_app()

with app.app_context():
    print("开始初始化采购销售模块数据...")
    
    # 初始化采购订单数据
    from app.models import PurchaseOrder, PurchaseOrderDetail
    from app.models import Supplier, Product, Unit
    
    # 获取供应商
    supplier_a = Supplier.query.filter_by(supplier_code='SP001').first()
    
    if supplier_a:
            # 检查采购订单是否已存在
            po1 = PurchaseOrder.query.filter_by(order_no='PO20240501001').first()
            if not po1:
                # 创建采购订单
                po1 = PurchaseOrder(
                    order_no='PO20240501001',
                    supplier_id=supplier_a.supplier_id,
                    order_date=datetime.today(),
                    total_amount=10500.00,
                    status=1,
                    created_by=1
                )
                db.session.add(po1)
                db.session.commit()
                
                # 获取产品
                prod001 = Product.query.filter_by(product_code='PROD001').first()
                prod002 = Product.query.filter_by(product_code='PROD002').first()
                
                if prod001 and prod002:
                    # 创建采购订单明细
                    pod1 = PurchaseOrderDetail(
                        order_id=po1.order_id,
                        material_id=prod001.product_id,
                        quantity=2,
                        price=5000.00,
                        amount=10000.00
                    )
                    db.session.add(pod1)
                    
                    pod2 = PurchaseOrderDetail(
                        order_id=po1.order_id,
                        material_id=prod002.product_id,
                        quantity=10,
                        price=50.00,
                        amount=500.00
                    )
                    db.session.add(pod2)
                    
                    db.session.commit()
                    print("采购订单数据初始化完成")
            else:
                print("采购订单已存在，跳过创建")
    
    # 初始化销售订单数据
    from app.models import SalesOrder, SalesOrderDetail
    from app.models import Customer, Product, Warehouse
    
    # 获取客户
    customer_x = Customer.query.filter_by(customer_code='CU001').first()
    
    if customer_x:
            # 获取仓库
            warehouse_main = Warehouse.query.filter_by(warehouse_code='WH001').first()
            
            if warehouse_main:
                # 检查销售订单是否已存在
                so1 = SalesOrder.query.filter_by(order_no='SO20240501001').first()
                if not so1:
                    # 创建销售订单
                    so1 = SalesOrder(
                        order_no='SO20240501001',
                        customer_id=customer_x.customer_id,
                        warehouse_id=warehouse_main.warehouse_id,
                        order_date=datetime.today(),
                        total_amount=6500.00,
                        status=1,
                        created_by=1
                    )
                    db.session.add(so1)
                    db.session.commit()
                    
                    # 获取产品
                    prod001 = Product.query.filter_by(product_code='PROD001').first()
                    
                    if prod001:
                        # 创建销售订单明细
                        sod1 = SalesOrderDetail(
                            order_id=so1.order_id,
                            product_id=prod001.product_id,
                            quantity=1,
                            price=6500.00,
                            amount=6500.00
                        )
                        db.session.add(sod1)
                        db.session.commit()
                        print("销售订单数据初始化完成")
                else:
                    print("销售订单已存在，跳过创建")
    
    print("采购销售模块数据初始化完成！")