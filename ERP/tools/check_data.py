#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app, db

app = create_app()

with app.app_context():
    from app.models import OpeningBalanceInventory
    print(f"库存期初数据数量: {OpeningBalanceInventory.query.count()}")
    for item in OpeningBalanceInventory.query.all():
        print(f"商品: {item.item_name}, 数量: {item.quantity}, 金额: {item.amount}")
    
    from app.models import Product
    print(f"\n产品数据数量: {Product.query.count()}")
    for item in Product.query.all():
        print(f"产品: {item.product_name}, 单价: {item.sale_price}")