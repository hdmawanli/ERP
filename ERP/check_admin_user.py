from app import create_app
from app.models import User
from werkzeug.security import check_password_hash

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='admin').first()
    if user:
        print(f'管理员用户存在: 用户名={user.username}')
        print(f'密码验证: 通过' if check_password_hash(user.password, 'admin123456') else '密码验证: 不通过')
    else:
        print('管理员用户不存在')