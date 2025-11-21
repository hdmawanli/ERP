from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User
from app.auth import auth

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):  # 使用哈希密码验证
            login_user(user)
            flash('登录成功', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误', 'danger')
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # 仅管理员可创建用户
    if current_user.is_authenticated and current_user.role == 'admin':
        if request.method == 'POST':
            username = request.form['username']
            real_name = request.form['real_name']
            password = request.form['password']
            role = request.form['role']
            
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('用户名已存在', 'danger')
                return redirect(url_for('auth.register'))
            
            new_user = User(username=username, real_name=real_name, password=password, role=role, status=1)
            db.session.add(new_user)
            db.session.commit()
            flash('用户创建成功', 'success')
            return redirect(url_for('auth.register'))
        return render_template('auth/register.html')
    else:
        flash('无权限访问', 'danger')
        return redirect(url_for('auth.login'))