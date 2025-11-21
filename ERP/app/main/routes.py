from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app.main import main

@main.route('/')
@login_required
def index():
    print("DEBUG: Index route called")
    print("DEBUG: Current user", current_user.username)
    return render_template('main/index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # 仪表盘页面，显示系统统计信息
    return render_template('main/dashboard.html')

@main.route('/navigate/<module>')
@login_required
def navigate(module):
    # 模块导航
    module_routes = {
        'bank': 'bank.index',
        'inventory': 'inventory.index',
        'purchase': 'purchase.index',
        'sales': 'sales.index',
        'assembly': 'assembly.index',
        'expense': 'expense.index',
        'opening': 'opening.index'
    }
    if module in module_routes:
        return redirect(url_for(module_routes[module]))
    return redirect(url_for('main.index'))