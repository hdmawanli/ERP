import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath('e:/PYTHON/ERP'))

from app import create_app
from app.models import db, OpeningBalanceInventory

# 创建应用并初始化数据库
app = create_app()
with app.app_context():
    # 查询所有表
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print('tables:')
    for table in sorted(tables):
        print(f'- {table}')
    
    # 查询指定表的结构
    print(f'\nStructure of opening_balance_inventory:')
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    columns = inspector.get_columns('opening_balance_inventory')
    for column in columns:
        # 打印所有键，找出primary_key的正确键名
        print(f"- {column['name']}: {column}")
