from app import app, db
from flask_migrate import Migrate, upgrade

# 初始化迁移
migrate = Migrate(app, db)

# 创建所有表
with app.app_context():
    db.create_all()