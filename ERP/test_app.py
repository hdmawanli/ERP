from flask import Flask, Blueprint

# 创建一个简单的应用
app = Flask(__name__)
print(f"App type: {type(app)}")
print(f"Has register_blueprint: {hasattr(app, 'register_blueprint')}")

# 创建一个简单的蓝图
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Hello, World!"

# 注册蓝图
try:
    app.register_blueprint(main)
    print("Blueprint registered successfully")

except AttributeError as e:
    print(f"Error registering blueprint: {e}")
    import traceback
    traceback.print_exc()

# 测试运行
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)