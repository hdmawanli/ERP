# ERP系统功能模块代码介绍文档

## 1. 系统概述
该ERP系统是一个基于Flask框架开发的企业资源规划系统，包含多个功能模块，实现了企业日常运营的核心业务流程管理。

## 2. 模块结构
系统主要包含以下功能模块：
- **ARAP模块**：应收应付管理
- **Inventory模块**：库存管理
- **Assembly模块**：组装订单管理

## 3. 功能模块详细介绍

### 3.1 ARAP模块（应收应付管理）

#### 3.1.1 概述
ARAP模块负责管理企业的客户、供应商、应收账款和应付账款，实现了完整的应收应付业务流程。

#### 3.1.2 核心功能
- 客户信息管理（增删改查）
- 供应商信息管理（增删改查）
- 应收账款发票管理（新增、列表）
- 应付账款发票管理（新增、列表）
- 收款记录管理（新增、列表）
- 付款记录管理（新增、列表）

#### 3.1.3 关键路由
```python:e%3A%2FPYTHON%2FERP%2Fapp%2Farap%2Froutes.py
# 客户管理
@arap.route('/customers')  # 客户列表
@arap.route('/customer/add', methods=['GET', 'POST'])  # 新增客户
@arap.route('/customer/edit/<int:customer_id>', methods=['GET', 'POST'])  # 编辑客户

# 供应商管理
@arap.route('/suppliers')  # 供应商列表
@arap.route('/supplier/add', methods=['GET', 'POST'])  # 新增供应商
@arap.route('/supplier/edit/<int:supplier_id>', methods=['GET', 'POST'])  # 编辑供应商

# 应收账款
@arap.route('/ar/invoices')  # 应收账款发票列表
@arap.route('/ar/invoice/add', methods=['GET', 'POST'])  # 新增应收账款发票

# 应付账款
@arap.route('/ap/invoices')  # 应付账款发票列表
@arap.route('/ap/invoice/add', methods=['GET', 'POST'])  # 新增应付账款发票

# 收款管理
@arap.route('/ar/payments')  # 收款记录列表
@arap.route('/ar/payment/add', methods=['GET', 'POST'])  # 新增收款记录

# 付款管理
@arap.route('/ap/payments')  # 付款记录列表
@arap.route('/ap/payment/add', methods=['GET', 'POST'])  # 新增付款记录
```

#### 3.1.4 数据模型
```python:e%3A%2FPYTHON%2FERP%2Fapp%2Fmodels.py
class Customer(db.Model):  # 客户模型
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(30), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    # ... 其他字段

class Supplier(db.Model):  # 供应商模型
    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_code = db.Column(db.String(30), unique=True, nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)
    # ... 其他字段

class ARInvoice(db.Model):  # 应收账款发票模型
    invoice_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    invoice_no = db.Column(db.String(30), unique=True, nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    balance = db.Column(db.DECIMAL(18, 2), nullable=False)
    # ... 其他字段

class APInvoice(db.Model):  # 应付账款发票模型
    invoice_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    invoice_no = db.Column(db.String(30), unique=True, nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    balance = db.Column(db.DECIMAL(18, 2), nullable=False)
    # ... 其他字段

class ARPayment(db.Model):  # 收款记录模型
    payment_id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('ar_invoices.invoice_id'), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    # ... 其他字段

class APPayment(db.Model):  # 付款记录模型
    payment_id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('ap_invoices.invoice_id'), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    # ... 其他字段
```

#### 3.1.5 核心业务逻辑
- 收款/付款时自动更新对应发票的余额
- 发票余额不能为负数
- 客户/供应商信息支持软删除

### 3.2 Inventory模块（库存管理）

#### 3.2.1 概述
Inventory模块负责管理企业的库存商品，包括商品信息维护和库存余额查询功能。

#### 3.2.2 核心功能
- 库存商品信息管理（增删改查）
- 库存现存量查询
- 库存详情查询

#### 3.2.3 关键路由
```python:e%3A%2FPYTHON%2FERP%2Fapp%2Finventory%2Froutes.py
# 库存商品管理
@inventory.route('/')  # 库存商品列表
@inventory.route('/item/add', methods=['GET', 'POST'])  # 新增库存商品
@inventory.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])  # 编辑库存商品
@inventory.route('/item/delete/<int:item_id>')  # 删除库存商品（软删除）

# 库存查询
@inventory.route('/stock/query')  # 库存现存量查询
@inventory.route('/stock/detail/<int:item_id>')  # 库存详情查询
```

#### 3.2.4 数据模型
```python:e%3A%2FPYTHON%2FERP%2Fapp%2Fmodels.py
class Product(db.Model):  # 库存商品模型
    product_id = db.Column(db.Integer, primary_key=True)
    item_code = db.Column(db.String(30), unique=True, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    spec = db.Column(db.String(50))
    unit = db.Column(db.String(20))
    category = db.Column(db.String(50))
    type = db.Column(db.Integer)
    # ... 其他字段

class InventoryBalance(db.Model):  # 库存余额模型
    balance_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False, default=0.0000)
    # ... 其他字段

class InventoryFlow(db.Model):  # 库存流水模型
    flow_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'), nullable=False)
    flow_type = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    # ... 其他字段
```

#### 3.2.5 核心业务逻辑
- 新增库存商品时自动创建初始库存记录
- 库存商品支持软删除
- 库存查询支持按商品编码和名称搜索

### 3.3 Assembly模块（组装订单管理）

#### 3.3.1 概述
Assembly模块负责管理企业的生产组装业务，实现了从组装订单创建到库存更新的完整流程。

#### 3.3.2 核心功能
- 组装订单管理（新增、列表、详情）
- 组装原材料验证
- 自动更新库存（原材料减少、成品增加）
- 组装订单查询

#### 3.3.3 关键路由
```python:e%3A%2FPYTHON%2FERP%2Fapp%2Fassembly%2Froutes.py
@assembly.route('/')  # 组装订单列表
@assembly.route('/add', methods=['GET', 'POST'])  # 新增组装订单
@assembly.route('/order/<int:order_id>')  # 组装订单详情
@assembly.route('/orders')  # 组装订单列表
@assembly.route('/order/search')  # 组装订单查询
@assembly.route('/finished-good/<int:item_id>')  # 获取成品详情（AJAX）
@assembly.route('/raw-material/<int:item_id>')  # 获取原材料详情（AJAX）
```

#### 3.3.4 数据模型
```python:e%3A%2FPYTHON%2FERP%2Fapp%2Fmodels.py
class BOM(db.Model):  # 物料清单模型
    bom_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    # ... 其他字段

class AssemblyOrder(db.Model):  # 组装订单模型
    order_id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(30), unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'), nullable=False)
    # ... 其他字段

class AssemblyOrderDetail(db.Model):  # 组装订单详情模型
    detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('assembly_orders.order_id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    # ... 其他字段
```

#### 3.3.5 核心业务逻辑
1. **库存验证**：组装前检查原材料库存是否充足
2. **订单处理**：
   - 创建组装订单
   - 生成组装原材料记录
3. **库存更新**：
   - 减少原材料库存
   - 增加成品库存
4. **数据一致性**：所有操作在一个事务中完成，确保数据一致性

## 4. 系统架构

### 4.1 技术栈
- **后端框架**：Flask
- **数据库**：SQLAlchemy (ORM)
- **用户认证**：Flask-Login
- **模板引擎**：Jinja2

### 4.2 数据流转
1. 用户通过前端页面发起请求
2. Flask路由处理请求
3. 业务逻辑层处理数据
4. 数据持久化到数据库
5. 返回响应给前端

## 5. 代码特点

### 5.1 模块化设计
各功能模块独立，降低耦合度，便于维护和扩展

### 5.2 分层架构
- 表现层：路由和模板
- 业务逻辑层：路由函数中的业务处理
- 数据访问层：模型类

### 5.3 事务处理
关键业务操作使用数据库事务，确保数据一致性

### 5.4 用户认证
使用Flask-Login实现用户认证和授权，保护敏感数据

## 6. 扩展建议

1. **增加权限控制**：实现基于角色的访问控制
2. **优化查询性能**：增加索引，优化复杂查询
3. **增加API接口**：提供RESTful API支持第三方系统集成
4. **数据备份与恢复**：实现定时数据备份和恢复功能
5. **报表功能**：增加各类业务报表生成功能

# 总结
该ERP系统通过模块化设计实现了企业核心业务流程的管理，代码结构清晰，业务逻辑完整，具有良好的可扩展性和维护性。