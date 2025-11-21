from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
import os

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
migrate = Migrate()

# 设置登录视图
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
    flask_app = Flask(__name__)
    
    # 配置
    flask_app.config['SECRET_KEY'] = 'your-secret-key-here'
    # 支持通过环境变量 `DATABASE_URL` 覆盖数据库连接，便于本地调试（例如 sqlite）
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'postgresql://postgres:666666@localhost/erp_db'
    )
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['PERMANENT_SESSION_LIFETIME'] = 1800
    
    # 初始化扩展
    db.init_app(flask_app)
    login_manager.init_app(flask_app)
    bootstrap.init_app(flask_app)
    migrate.init_app(flask_app, db)
    
    # 创建数据库表并初始化默认数据（可通过环境变量 SKIP_DB_CREATE=1 跳过）
    if not os.environ.get('SKIP_DB_CREATE'):
        with flask_app.app_context():
            import app.models
            from app.models import User, Department
            from werkzeug.security import generate_password_hash

            db.create_all()

            # 创建默认部门
            if not Department.query.first():
                admin_dept = Department(department_name='管理部门', parent_id=None, status=1)
                db.session.add(admin_dept)
                db.session.commit()

            # 创建默认管理员用户
            if not User.query.first():
                admin_user = User(
                    username='admin',
                    password=generate_password_hash('admin123456'),
                    real_name='系统管理员',
                    department_id=Department.query.filter_by(department_name='管理部门').first().department_id,
                    role='admin',
                    status=1
                )
                db.session.add(admin_user)
                db.session.commit()
    
    # 注册蓝图
    print("DEBUG: Registering main blueprint")
    from app.main import main as main_blueprint
    flask_app.register_blueprint(main_blueprint)
    
    print("DEBUG: Registering auth blueprint")
    from app.auth import auth as auth_blueprint
    flask_app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    print("DEBUG: Registering purchase blueprint")
    from app.purchase import purchase as purchase_blueprint
    flask_app.register_blueprint(purchase_blueprint, url_prefix='/purchase')
    
    print("DEBUG: Registering sales blueprint")
    from app.sales import sales as sales_blueprint
    flask_app.register_blueprint(sales_blueprint, url_prefix='/sales')

    print("DEBUG: Registering inventory blueprint")
    from app.inventory import inventory as inventory_blueprint
    flask_app.register_blueprint(inventory_blueprint, url_prefix='/inventory')

    print("DEBUG: Registering assembly blueprint")
    from app.assembly import assembly as assembly_blueprint
    flask_app.register_blueprint(assembly_blueprint, url_prefix='/assembly')

    print("DEBUG: Registering bank blueprint")
    from app.bank import bank as bank_blueprint
    flask_app.register_blueprint(bank_blueprint, url_prefix='/bank')

    print("DEBUG: Registering expense blueprint")
    from app.expense import expense as expense_blueprint
    flask_app.register_blueprint(expense_blueprint, url_prefix='/expense')

    print("DEBUG: Registering opening blueprint")
    from app.opening import opening as opening_blueprint
    flask_app.register_blueprint(opening_blueprint, url_prefix='/opening')

    print("DEBUG: Registering arap blueprint")
    from app.arap import arap as arap_blueprint
    flask_app.register_blueprint(arap_blueprint, url_prefix='/arap')

    print("DEBUG: Registering seed_batch blueprint")
    from app.seed_batch import seed_batch as seed_batch_blueprint
    flask_app.register_blueprint(seed_batch_blueprint, url_prefix='/seed_batch')

    print("DEBUG: Registering quality_control blueprint")
    from app.quality_control import quality_control as quality_control_blueprint
    flask_app.register_blueprint(quality_control_blueprint, url_prefix='/quality_control')

    print("DEBUG: Registering production blueprint")
    from app.production import production as production_blueprint
    flask_app.register_blueprint(production_blueprint, url_prefix='/production')

    print("DEBUG: Registering after_sales blueprint")
    from app.after_sales import after_sales as after_sales_blueprint
    flask_app.register_blueprint(after_sales_blueprint, url_prefix='/after_sales')
    
    print("DEBUG: Registering master_data blueprint")
    from app.master_data import master_data as master_data_blueprint
    flask_app.register_blueprint(master_data_blueprint, url_prefix='/master-data')
    
    # 打印所有注册的路由
    print(f"DEBUG: All app routes: {list(flask_app.url_map.iter_rules())}")
    return flask_app