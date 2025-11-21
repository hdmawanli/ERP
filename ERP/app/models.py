from app import db
from datetime import datetime
from flask_login import UserMixin

# 基础数据模块
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def get_id(self):
        return str(self.user_id)

class Department(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    status = db.Column(db.Integer, nullable=False, default=1)
    
    parent = db.relationship('Department', remote_side=[department_id], backref='children')

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_code = db.Column(db.String(20), unique=True, nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    status = db.Column(db.Integer, nullable=False, default=1)

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    status = db.Column(db.Integer, nullable=False, default=1)

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    warehouse_id = db.Column(db.Integer, primary_key=True)
    warehouse_code = db.Column(db.String(20), unique=True, nullable=False)
    warehouse_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200))
    status = db.Column(db.Integer, nullable=False, default=1)

class Unit(db.Model):
    __tablename__ = 'units'
    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(50), nullable=False)
    unit_code = db.Column(db.String(20), nullable=False)

class Brand(db.Model):
    __tablename__ = 'brands'
    brand_id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(50), nullable=False)
    brand_code = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)

class Specification(db.Model):
    __tablename__ = 'specifications'
    spec_id = db.Column(db.Integer, primary_key=True)
    spec_name = db.Column(db.String(100), nullable=False)
    spec_code = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)

class Variety(db.Model):
    __tablename__ = 'varieties'
    variety_id = db.Column(db.Integer, primary_key=True)
    variety_name = db.Column(db.String(100), nullable=False)
    variety_code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    origin = db.Column(db.String(100))
    seed_type = db.Column(db.String(20))  # 种子类型：杂交种、常规种等
    status = db.Column(db.Integer, nullable=False, default=1)

# 银行模块
class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'
    account_id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(50), nullable=False)
    bank_name = db.Column(db.String(50), nullable=False)
    account_number = db.Column(db.String(30), nullable=False)
    balance = db.Column(db.DECIMAL(18, 2), nullable=False, default=0.00)
    status = db.Column(db.Integer, nullable=False, default=1)

class BankFlow(db.Model):
    __tablename__ = 'bank_flows'
    flow_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.account_id'), nullable=False)
    flow_date = db.Column(db.Date, nullable=False, default=datetime.today())
    type = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    summary = db.Column(db.String(100))
    related_type = db.Column(db.String(20))
    related_id = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    account = db.relationship('BankAccount', backref='flows')
    user = db.relationship('User', backref='bank_flows')

# 应收应付模块
class Receivable(db.Model):
    __tablename__ = 'receivables'
    receivable_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    received_amount = db.Column(db.DECIMAL(18, 2), nullable=False, default=0.00)
    balance = db.Column(db.DECIMAL(18, 2), nullable=False, default=0.00)
    due_date = db.Column(db.Date)
    status = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    customer = db.relationship('Customer', backref='receivables')

class Payable(db.Model):
    __tablename__ = 'payables'
    payable_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    paid_amount = db.Column(db.DECIMAL(18, 2), nullable=False, default=0.00)
    balance = db.Column(db.DECIMAL(18, 2), nullable=False, default=0.00)
    due_date = db.Column(db.Date)
    status = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    supplier = db.relationship('Supplier', backref='payables')

class Receipt(db.Model):
    __tablename__ = 'receipts'
    receipt_id = db.Column(db.Integer, primary_key=True)
    receivable_id = db.Column(db.Integer, db.ForeignKey('receivables.receivable_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    receipt_date = db.Column(db.Date, nullable=False, default=datetime.today())
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.account_id'), nullable=False)
    remark = db.Column(db.String(100))
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    receivable = db.relationship('Receivable', backref='receipts')
    customer = db.relationship('Customer', backref='receipts')
    account = db.relationship('BankAccount', backref='receipts')
    user = db.relationship('User', backref='receipts')

class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    payable_id = db.Column(db.Integer, db.ForeignKey('payables.payable_id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False, default=datetime.today())
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.account_id'), nullable=False)
    remark = db.Column(db.String(100))
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    payable = db.relationship('Payable', backref='payments')
    supplier = db.relationship('Supplier', backref='payments')
    account = db.relationship('BankAccount', backref='payments')
    user = db.relationship('User', backref='payments')

# 库存模块
class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('product_categories.category_id'))
    sort_order = db.Column(db.Integer)
    
    parent = db.relationship('ProductCategory', remote_side=[category_id], backref='children')

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(20), unique=True, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.category_id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.brand_id'))
    spec_id = db.Column(db.Integer, db.ForeignKey('specifications.spec_id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    variety_id = db.Column(db.Integer, db.ForeignKey('varieties.variety_id'))  # 种子品种
    purchase_price = db.Column(db.DECIMAL(18, 2))
    sale_price = db.Column(db.DECIMAL(18, 2), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    
    category = db.relationship('ProductCategory', backref='products')
    brand = db.relationship('Brand', backref='products')
    specification = db.relationship('Specification', backref='products')
    unit = db.relationship('Unit', backref='products')
    variety = db.relationship('Variety', backref='products')

class MaterialCategory(db.Model):
    __tablename__ = 'material_categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('material_categories.category_id'))
    sort_order = db.Column(db.Integer)
    
    parent = db.relationship('MaterialCategory', remote_side=[category_id], backref='children')

class Material(db.Model):
    __tablename__ = 'materials'
    material_id = db.Column(db.Integer, primary_key=True)
    material_code = db.Column(db.String(20), unique=True, nullable=False)
    material_name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('material_categories.category_id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    purchase_price = db.Column(db.DECIMAL(18, 2))
    status = db.Column(db.Integer, nullable=False, default=1)
    
    category = db.relationship('MaterialCategory', backref='materials')
    unit = db.relationship('Unit', backref='materials')

class InventoryFlow(db.Model):
    __tablename__ = 'inventory_flows'
    flow_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('seed_batches.batch_id'))  # 批次ID
    flow_type = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    cost_price = db.Column(db.DECIMAL(18, 2))
    amount = db.Column(db.DECIMAL(18, 2))
    related_type = db.Column(db.String(20))
    related_id = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    warehouse = db.relationship('Warehouse', backref='inventory_flows')
    user = db.relationship('User', backref='inventory_flows')
    batch = db.relationship('SeedBatch', backref='inventory_flows')

class InventoryBalance(db.Model):
    __tablename__ = 'inventory_balances'
    balance_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('seed_batches.batch_id'))  # 批次ID
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False, default=0.0000)
    cost_price = db.Column(db.DECIMAL(18, 2))
    amount = db.Column(db.DECIMAL(18, 2))
    
    warehouse = db.relationship('Warehouse', backref='inventory_balances')
    batch = db.relationship('SeedBatch', backref='inventory_balances')

# 采购模块
class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    order_id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(30), unique=True, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    order_date = db.Column(db.Date, nullable=False, default=datetime.today())
    total_amount = db.Column(db.DECIMAL(18, 2), nullable=False, default=0.00)
    status = db.Column(db.Integer, nullable=False, default=1)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    supplier = db.relationship('Supplier', backref='purchase_orders')
    user = db.relationship('User', backref='purchase_orders')

class PurchaseOrderDetail(db.Model):
    __tablename__ = 'purchase_order_details'
    detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.order_id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    price = db.Column(db.DECIMAL(18, 2), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    
    order = db.relationship('PurchaseOrder', backref='details')
    material = db.relationship('Material', backref='purchase_order_details')

class PurchaseInvoice(db.Model):
    __tablename__ = 'purchase_invoices'
    invoice_id = db.Column(db.Integer, primary_key=True)
    invoice_no = db.Column(db.String(30), unique=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.order_id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    invoice_date = db.Column(db.Date, nullable=False, default=datetime.today())
    total_amount = db.Column(db.DECIMAL(18, 2), nullable=False, default=0.00)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    order = db.relationship('PurchaseOrder', backref='invoices')
    supplier = db.relationship('Supplier', backref='purchase_invoices')
    user = db.relationship('User', backref='purchase_invoices')

class PurchaseInvoiceDetail(db.Model):
    __tablename__ = 'purchase_invoice_details'
    detail_id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('purchase_invoices.invoice_id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    price = db.Column(db.DECIMAL(18, 2), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    
    invoice = db.relationship('PurchaseInvoice', backref='details')
    material = db.relationship('Material', backref='purchase_invoice_details')
    warehouse = db.relationship('Warehouse', backref='purchase_invoice_details')

# 销售模块
class SalesOrder(db.Model):
    __tablename__ = 'sales_orders'
    order_id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(30), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'))
    order_date = db.Column(db.Date, nullable=False, default=datetime.today())
    total_amount = db.Column(db.DECIMAL(18, 2), nullable=False, default=0.00)
    status = db.Column(db.Integer, nullable=False, default=1)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ship_date = db.Column(db.Date)
    
    customer = db.relationship('Customer', backref='sales_orders')
    user = db.relationship('User', backref='sales_orders')
    warehouse = db.relationship('Warehouse', backref='sales_orders')

class SalesOrderDetail(db.Model):
    __tablename__ = 'sales_order_details'
    detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('sales_orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    price = db.Column(db.DECIMAL(18, 2), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    
    order = db.relationship('SalesOrder', backref='details')
    product = db.relationship('Product', backref='sales_order_details')

class SalesDeliveryNote(db.Model):
    __tablename__ = 'sales_delivery_notes'
    note_id = db.Column(db.Integer, primary_key=True)
    note_no = db.Column(db.String(30), unique=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('sales_orders.order_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False, default=datetime.today())
    total_amount = db.Column(db.DECIMAL(18, 2), nullable=False, default=0.00)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    order = db.relationship('SalesOrder', backref='delivery_notes')
    customer = db.relationship('Customer', backref='delivery_notes')
    user = db.relationship('User', backref='delivery_notes')

class SalesDeliveryNoteDetail(db.Model):
    __tablename__ = 'sales_delivery_note_details'
    detail_id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('sales_delivery_notes.note_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    price = db.Column(db.DECIMAL(18, 2), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    
    note = db.relationship('SalesDeliveryNote', backref='details')
    product = db.relationship('Product', backref='delivery_note_details')
    warehouse = db.relationship('Warehouse', backref='delivery_note_details')

# 组装拆卸模块
class BOM(db.Model):
    __tablename__ = 'bom'
    bom_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    
    product = db.relationship('Product', backref='bom')
    material = db.relationship('Material', backref='bom')
    unit = db.relationship('Unit', backref='bom')

class AssemblyOrder(db.Model):
    __tablename__ = 'assembly_orders'
    order_id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(30), unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    product = db.relationship('Product', backref='assembly_orders')
    warehouse = db.relationship('Warehouse', backref='assembly_orders')
    user = db.relationship('User', backref='assembly_orders')

class AssemblyOrderDetail(db.Model):
    __tablename__ = 'assembly_order_details'
    detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('assembly_orders.order_id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    cost_price = db.Column(db.DECIMAL(18, 2))
    amount = db.Column(db.DECIMAL(18, 2))
    
    order = db.relationship('AssemblyOrder', backref='details')
    material = db.relationship('Material', backref='assembly_order_details')

class DisassemblyOrder(db.Model):
    __tablename__ = 'disassembly_orders'
    order_id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(30), unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    product = db.relationship('Product', backref='disassembly_orders')
    warehouse = db.relationship('Warehouse', backref='disassembly_orders')
    user = db.relationship('User', backref='disassembly_orders')

class DisassemblyOrderDetail(db.Model):
    __tablename__ = 'disassembly_order_details'
    detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('disassembly_orders.order_id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    cost_price = db.Column(db.DECIMAL(18, 2))
    amount = db.Column(db.DECIMAL(18, 2))
    
    order = db.relationship('DisassemblyOrder', backref='details')
    material = db.relationship('Material', backref='disassembly_order_details')

# 费用模块
class ExpenseCategory(db.Model):
    __tablename__ = 'expense_categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('expense_categories.category_id'))
    
    parent = db.relationship('ExpenseCategory', remote_side=[category_id], backref='children')

class AccountingSubject(db.Model):
    __tablename__ = 'accounting_subjects'
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(20), unique=True, nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    subject_type = db.Column(db.String(20), nullable=False)  # 资产、负债、权益、成本、损益
    status = db.Column(db.Integer, nullable=False, default=1)

class Expense(db.Model):
    __tablename__ = 'expenses'
    expense_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('expense_categories.category_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('accounting_subjects.subject_id'), nullable=False)
    expense_date = db.Column(db.Date, nullable=False, default=datetime.today())
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    description = db.Column(db.String(200))
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    
    category = db.relationship('ExpenseCategory', backref='expenses')
    subject = db.relationship('AccountingSubject', backref='expenses')
    department = db.relationship('Department', backref='expenses')
    user = db.relationship('User', backref='expenses')

class ExpenseAllocation(db.Model):
    __tablename__ = 'expense_allocation'
    allocation_id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.expense_id'), nullable=False)
    allocation_type = db.Column(db.String(20), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    expense = db.relationship('Expense', backref='allocations')
    user = db.relationship('User', backref='expense_allocations')

# 期初余额模块
class OpeningBankBalance(db.Model):
    __tablename__ = 'opening_bank_balances'
    balance_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.account_id'), nullable=False)
    balance_date = db.Column(db.Date, nullable=False, default=datetime.today())
    balance = db.Column(db.DECIMAL(18, 2), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    account = db.relationship('BankAccount', backref='opening_balances')
    user = db.relationship('User', backref='opening_bank_balances')

class OpeningReceivable(db.Model):
    __tablename__ = 'opening_receivables'
    opening_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    due_date = db.Column(db.Date)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    customer = db.relationship('Customer', backref='opening_receivables')
    user = db.relationship('User', backref='opening_receivables')

class OpeningPayable(db.Model):
    __tablename__ = 'opening_payables'
    opening_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    due_date = db.Column(db.Date)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    supplier = db.relationship('Supplier', backref='opening_payables')
    user = db.relationship('User', backref='opening_payables')

class OpeningProductStock(db.Model):
    __tablename__ = 'opening_product_stock'
    opening_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    cost_price = db.Column(db.DECIMAL(18, 2), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    product = db.relationship('Product', backref='opening_stock')
    warehouse = db.relationship('Warehouse', backref='opening_product_stock')
    user = db.relationship('User', backref='opening_product_stock')

class OpeningMaterialStock(db.Model):
    __tablename__ = 'opening_material_stock'
    opening_id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'), nullable=False)
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    cost_price = db.Column(db.DECIMAL(18, 2), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    material = db.relationship('Material', backref='opening_stock')
    warehouse = db.relationship('Warehouse', backref='opening_material_stock')
    user = db.relationship('User', backref='opening_material_stock')

class OpeningBalanceInventory(db.Model):
    __tablename__ = 'opening_balance_inventory'
    balance_id = db.Column(db.Integer, primary_key=True)
    item_code = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    spec = db.Column(db.String(100))
    unit = db.Column(db.String(20))
    quantity = db.Column(db.DECIMAL(18, 4), nullable=False)
    unit_cost = db.Column(db.DECIMAL(18, 2), nullable=False)
    amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    opening_date = db.Column(db.Date, nullable=False, default=datetime.now().date())
    description = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    user = db.relationship('User', backref='opening_inventories')

# 系统模块
class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    module = db.Column(db.String(50))
    action = db.Column(db.String(50))
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    user = db.relationship('User', backref='system_logs')

class SystemDict(db.Model):
    __tablename__ = 'system_dict'
    dict_id = db.Column(db.Integer, primary_key=True)
    dict_type = db.Column(db.String(50), nullable=False)
    dict_code = db.Column(db.String(50), nullable=False)
    dict_value = db.Column(db.String(100), nullable=False)
    sort_order = db.Column(db.Integer)

# 种子批次管理模块
class SeedBatch(db.Model):
    __tablename__ = 'seed_batches'
    batch_id = db.Column(db.Integer, primary_key=True)
    batch_number = db.Column(db.String(30), unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    production_date = db.Column(db.Date, nullable=False)
    shelf_life = db.Column(db.Integer, nullable=False)  # 保质期（天）
    expiration_date = db.Column(db.Date, nullable=False)
    storage_conditions = db.Column(db.String(200))
    status = db.Column(db.Integer, nullable=False, default=1)  # 1: 正常, 2: 即将过期, 3: 已过期
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    product = db.relationship('Product', backref='seed_batches')

class SeedBatchTrace(db.Model):
    __tablename__ = 'seed_batch_traces'
    trace_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('seed_batches.batch_id'), nullable=False)
    trace_type = db.Column(db.String(20), nullable=False)  # production:生产, testing:检测, processing:加工, packaging:包装, sale:销售
    trace_date = db.Column(db.Date, nullable=False, default=datetime.today())
    description = db.Column(db.String(500))
    operator = db.Column(db.String(50))
    related_id = db.Column(db.Integer)  # 关联其他表ID
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    batch = db.relationship('SeedBatch', backref='traces')

# 质量控制管理模块
class QualityTest(db.Model):
    __tablename__ = 'quality_tests'
    test_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('seed_batches.batch_id'), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)  # 检测类型
    test_date = db.Column(db.Date, nullable=False, default=datetime.today())
    operator = db.Column(db.String(50), nullable=False)
    overall_result = db.Column(db.String(20))  # 整体结果
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    batch = db.relationship('SeedBatch', backref='quality_tests')

class QualityTestItem(db.Model):
    __tablename__ = 'quality_test_items'
    test_item_id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('quality_tests.test_id'), nullable=False)
    test_item_name = db.Column(db.String(50), nullable=False)  # 检测项目名称
    test_value = db.Column(db.String(20))  # 检测值
    unit = db.Column(db.String(20))  # 计量单位
    standard_value = db.Column(db.String(50))  # 标准值
    is_qualified = db.Column(db.Boolean, nullable=False, default=True)  # 是否合格
    
    test = db.relationship('QualityTest', backref='test_items')

# 生产管理模块
class BreedingPlan(db.Model):
    __tablename__ = 'breeding_plans'
    plan_id = db.Column(db.Integer, primary_key=True)
    plan_code = db.Column(db.String(30), unique=True, nullable=False)  # 计划编号
    crop_type = db.Column(db.String(50), nullable=False)  # 作物类型
    variety = db.Column(db.String(50), nullable=False)  # 品种
    planned_area = db.Column(db.Float, nullable=False)  # 计划面积
    planned_yield = db.Column(db.Float, nullable=False)  # 计划产量
    start_date = db.Column(db.Date, nullable=False)  # 开始日期
    end_date = db.Column(db.Date, nullable=False)  # 结束日期
    status = db.Column(db.String(20), nullable=False, default='draft')  # 状态: draft, implemented, completed, canceled
    operator = db.Column(db.String(50), nullable=False)  # 操作人
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新时间

class FieldManagement(db.Model):
    __tablename__ = 'field_management'
    field_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('breeding_plans.plan_id'), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)  # 田间名称
    area = db.Column(db.Float, nullable=False)  # 面积
    planting_date = db.Column(db.Date, nullable=False)  # 播种日期
    sowing_rate = db.Column(db.Float, nullable=False)  # 播种量
    fertilizer_usage = db.Column(db.String(200))  # 施肥记录
    pesticide_usage = db.Column(db.String(200))  # 农药使用记录
    irrigation_record = db.Column(db.String(200))  # 灌溉记录
    growth_stage = db.Column(db.String(50))  # 生长阶段
    inspection_date = db.Column(db.Date)  # 检查日期
    inspection_results = db.Column(db.String(500))  # 检查结果
    operator = db.Column(db.String(50), nullable=False)  # 操作人
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 创建时间
    
    plan = db.relationship('BreedingPlan', backref='field_records')

class HarvestManagement(db.Model):
    __tablename__ = 'harvest_management'
    harvest_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('breeding_plans.plan_id'), nullable=False)
    harvest_date = db.Column(db.Date, nullable=False, default=datetime.today())  # 收获日期
    actual_area = db.Column(db.Float, nullable=False)  # 实际收获面积
    actual_yield = db.Column(db.Float, nullable=False)  # 实际产量
    moisture_content = db.Column(db.Float)  # 水分含量
    impurity_rate = db.Column(db.Float)  # 杂质率
    batch_id = db.Column(db.Integer, db.ForeignKey('seed_batches.batch_id'))  # 关联种子批次
    operator = db.Column(db.String(50), nullable=False)  # 操作人
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 创建时间
    
    plan = db.relationship('BreedingPlan', backref='harvest_records')
    batch = db.relationship('SeedBatch', backref='harvest_info')

# 售后服务管理模块
class CustomerFeedback(db.Model):
    __tablename__ = 'customer_feedbacks'
    feedback_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    feedback_type = db.Column(db.String(20), nullable=False)  # 质量问题、技术咨询等
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)  # 1: 待处理, 2: 处理中, 3: 已解决
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    solve_time = db.Column(db.DateTime)
    solved_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    solution = db.Column(db.Text)
    
    customer = db.relationship('Customer', backref='feedbacks')
    product = db.relationship('Product', backref='feedbacks')
    user = db.relationship('User', backref='solved_feedbacks')

class TechnicalSupport(db.Model):
    __tablename__ = 'technical_supports'
    support_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    support_type = db.Column(db.String(20), nullable=False)  # 技术咨询、培训请求等
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)  # 1: 待处理, 2: 处理中, 3: 已完成
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    complete_time = db.Column(db.DateTime)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    solution = db.Column(db.Text)
    
    customer = db.relationship('Customer', backref='supports')
    product = db.relationship('Product', backref='supports')
    user = db.relationship('User', backref='assigned_supports')