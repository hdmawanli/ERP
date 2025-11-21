from flask import Blueprint

# 创建售后服务蓝图
after_sales = Blueprint('after_sales', __name__, template_folder='templates', static_folder='static')

# 导入路由
from . import routes

# 导入模型
from .models import CustomerComplaint, ComplaintReply