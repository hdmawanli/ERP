#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app, db
from datetime import datetime

app = create_app()

with app.app_context():
    print("开始初始化基础数据...")
    
    # 初始化单位数据
    from app.models import Unit
    units = [
        {'unit_code': 'PCS', 'unit_name': '件'},
        {'unit_code': 'KG', 'unit_name': '千克'},
        {'unit_code': 'M', 'unit_name': '米'},
        {'unit_code': 'BOX', 'unit_name': '箱'},
        {'unit_code': 'SET', 'unit_name': '套'},
    ]
    for unit_data in units:
        unit = Unit.query.filter_by(unit_code=unit_data['unit_code']).first()
        if not unit:
            unit = Unit(**unit_data)
            db.session.add(unit)
    db.session.commit()
    print("单位数据初始化完成")
    
    # 初始化仓库数据
    from app.models import Warehouse
    warehouses = [
        {'warehouse_code': 'WH001', 'warehouse_name': '主仓库', 'address': '北京市朝阳区建国路1号'},
        {'warehouse_code': 'WH002', 'warehouse_name': '分仓库', 'address': '上海市浦东新区张江高科技园'},
    ]
    for warehouse_data in warehouses:
        warehouse = Warehouse.query.filter_by(warehouse_code=warehouse_data['warehouse_code']).first()
        if not warehouse:
            warehouse = Warehouse(**warehouse_data)
            db.session.add(warehouse)
    db.session.commit()
    print("仓库数据初始化完成")
    
    # 初始化供应商数据
    from app.models import Supplier
    suppliers = [
        {'supplier_code': 'SP001', 'supplier_name': '供应商A', 'contact_person': '张三', 'phone': '13800138001', 'address': '广州市天河区'},
        {'supplier_code': 'SP002', 'supplier_name': '供应商B', 'contact_person': '李四', 'phone': '13900139001', 'address': '深圳市南山区'},
    ]
    for supplier_data in suppliers:
        supplier = Supplier.query.filter_by(supplier_code=supplier_data['supplier_code']).first()
        if not supplier:
            supplier = Supplier(**supplier_data)
            db.session.add(supplier)
    db.session.commit()
    print("供应商数据初始化完成")
    
    # 初始化客户数据
    from app.models import Customer
    customers = [
        {'customer_code': 'CU001', 'customer_name': '客户X', 'contact_person': '王五', 'phone': '13700137001', 'address': '成都市高新区'},
        {'customer_code': 'CU002', 'customer_name': '客户Y', 'contact_person': '赵六', 'phone': '13600136001', 'address': '杭州市西湖区'},
    ]
    for customer_data in customers:
        customer = Customer.query.filter_by(customer_code=customer_data['customer_code']).first()
        if not customer:
            customer = Customer(**customer_data)
            db.session.add(customer)
    db.session.commit()
    print("客户数据初始化完成")
    
    # 初始化部门数据
    from app.models import Department
    departments = [
        {'department_name': '财务部', 'parent_id': None},
        {'department_name': '采购部', 'parent_id': None},
        {'department_name': '销售部', 'parent_id': None},
        {'department_name': '仓库部', 'parent_id': None},
    ]
    for dept_data in departments:
        dept = Department.query.filter_by(department_name=dept_data['department_name']).first()
        if not dept:
            dept = Department(**dept_data)
            db.session.add(dept)
    db.session.commit()
    print("部门数据初始化完成")
    
    # 初始化银行账户数据
    from app.models import BankAccount
    bank_accounts = [
        {'account_name': '基本户', 'bank_name': '中国工商银行', 'account_number': '6222020100012345678', 'balance': 100000.00},
        {'account_name': '一般户', 'bank_name': '中国建设银行', 'account_number': '6217000100012345678', 'balance': 50000.00},
    ]
    for account_data in bank_accounts:
        account = BankAccount.query.filter_by(account_number=account_data['account_number']).first()
        if not account:
            account = BankAccount(**account_data)
            db.session.add(account)
    db.session.commit()
    print("银行账户数据初始化完成")
    
    print("所有模块基础数据初始化完成！")