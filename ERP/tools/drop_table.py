import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath('e:/PYTHON/ERP'))

from app import create_app
from app.models import db

# 创建应用实例
app = create_app()

with app.app_context():
    # 删除opening_balance_inventory表
    db.engine.execute('DROP TABLE IF EXISTS opening_balance_inventory CASCADE')
    print('Successfully dropped opening_balance_inventory table')