#!/usr/bin/env python3
import pytest
from flask import Flask
from app import create_app, db
from app.models import (BankAccount, BankFlow, ExpenseCategory, Expense, AccountingSubject, 
                       OpeningBankBalance, OpeningReceivable, OpeningPayable, 
                       OpeningProductStock, OpeningMaterialStock, Customer, Warehouse, Product, Unit, User)
from datetime import datetime

@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # 使用内存数据库
        "WTF_CSRF_ENABLED": False
    })
    return app

@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture
def database(app):
    """创建数据库表"""
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

# 测试银行管理模块
class TestBankModule:
    def test_bank_account_creation(self, app, database):
        """测试银行账户创建"""
        with app.app_context():
            # 创建银行账户
            account = BankAccount(
                account_name="测试账户",
                bank_name="测试银行",
                account_number="1234567890",
                balance=1000.00,
                status=1
            )
            database.session.add(account)
            database.session.commit()
            
            # 查询银行账户
            retrieved_account = BankAccount.query.filter_by(account_number="1234567890").first()
            assert retrieved_account is not None
            assert retrieved_account.account_name == "测试账户"
            assert retrieved_account.balance == 1000.00
            
            # 删除银行账户
            retrieved_account.status = 0
            database.session.commit()
            
            # 验证银行账户已被删除
            deleted_account = BankAccount.query.filter_by(account_number="1234567890").first()
            assert deleted_account.status == 0

    def test_bank_flow_creation(self, app, database):
        """测试银行流水创建"""
        with app.app_context():
            # 创建银行账户
            account = BankAccount(
                account_name="测试账户",
                bank_name="测试银行",
                account_number="1234567890",
                balance=1000.00,
                status=1
            )
            database.session.add(account)
            database.session.commit()
            
            # 创建银行流水
            flow = BankFlow(
                account_id=account.account_id,
                flow_date=datetime.today().date(),
                type=1,  # 收入
                amount=500.00,
                summary="测试收入",
                created_by=1
            )
            database.session.add(flow)
            database.session.commit()
            
            # 查询银行流水
            retrieved_flow = BankFlow.query.filter_by(flow_id=flow.flow_id).first()
            assert retrieved_flow is not None
            assert retrieved_flow.amount == 500.00
            assert retrieved_flow.summary == "测试收入"

# 测试费用管理模块
class TestExpenseModule:
    def test_expense_type_creation(self, app, database):
        """测试费用类型创建"""
        with app.app_context():
            # 创建费用类型
            expense_type = ExpenseCategory(
                category_name="办公费用"
            )
            database.session.add(expense_type)
            database.session.commit()
            
            # 查询费用类型
            retrieved_type = ExpenseCategory.query.filter_by(category_name="办公费用").first()
            assert retrieved_type is not None
            assert retrieved_type.category_name == "办公费用"

    def test_expense_entry_creation(self, app, database):
        """测试费用录入创建"""
        with app.app_context():
            # 创建费用类型
            expense_category = ExpenseCategory(
                category_name="办公费用"
            )
            database.session.add(expense_category)
            database.session.commit()
            
            # 创建会计科目
            accounting_subject = AccountingSubject(
                subject_code="6602",
                subject_name="管理费用",
                subject_type="损益"
            )
            database.session.add(accounting_subject)
            database.session.commit()
            
            # 创建费用录入
            expense = Expense(
                category_id=expense_category.category_id,
                subject_id=accounting_subject.subject_id,
                expense_date=datetime.today().date(),
                amount=200.00,
                description="购买纸张",
                department_id=1,
                created_by=1
            )
            database.session.add(expense)
            database.session.commit()
            
            # 查询费用录入
            retrieved_expense = Expense.query.filter_by(description="购买纸张").first()
            assert retrieved_expense is not None
            assert retrieved_expense.amount == 200.00
            assert retrieved_expense.category.category_name == "办公费用"
            assert retrieved_expense.subject.subject_name == "管理费用"

# 测试期初管理模块
class TestOpeningModule:
    def test_opening_bank_balance(self, app, database):
        """测试银行期初余额创建"""
        with app.app_context():
            # 确保用户表存在ID为1的用户
            user = User.query.get(1)
            if not user:
                user = User(
                    username="test_user",
                    password="test_pass",
                    email="test@example.com",
                    real_name="测试用户",
                    status=1
                )
                database.session.add(user)
                database.session.flush()

            # 创建银行账户
            bank_account = BankAccount(
                account_name="测试银行账户",
                bank_name="测试银行",
                account_number="1234567890",
                balance=0.00,
                status=1
            )
            database.session.add(bank_account)
            database.session.commit()
            
            # 创建银行期初余额
            opening_bank = OpeningBankBalance(
                account_id=bank_account.account_id,
                balance_date=datetime.today().date(),
                balance=5000.00,
                created_by=user.user_id
            )
            database.session.add(opening_bank)
            database.session.commit()
            
            # 查询银行期初余额
            retrieved_balance = OpeningBankBalance.query.filter_by(account_id=bank_account.account_id).first()
            assert retrieved_balance is not None
            assert retrieved_balance.balance == 5000.00
            assert retrieved_balance.balance_date == datetime.today().date()

    # 测试应收期初余额创建
    def test_opening_ar_balance(self, app, database):
        """测试应收期初余额创建"""
        with app.app_context():
            # 确保用户存在
            user = User.query.get(1)
            if not user:
                user = User(
                    username="test_user",
                    password="test_pass",
                    email="test@example.com",
                    real_name="测试用户",
                    status=1
                )
                database.session.add(user)
                database.session.flush()

            # 创建客户
            customer = Customer(
                customer_code="CUST001",
                customer_name="测试客户",
                contact_person="张三",
                phone="13800138000",
                status=1
            )
            database.session.add(customer)
            database.session.flush()

            # 创建应收期初余额
            opening_ar = OpeningReceivable(
                customer_id=customer.customer_id,
                amount=3000.00,
                due_date=datetime.today().date(),
                created_by=user.user_id
            )
            database.session.add(opening_ar)
            database.session.commit()

            # 查询应收期初余额
            retrieved_ar = OpeningReceivable.query.filter_by(customer_id=customer.customer_id).first()
            assert retrieved_ar is not None
            assert retrieved_ar.amount == 3000.00

    # 测试库存期初余额创建
    def test_opening_inventory(self, app, database):
        """测试库存期初余额创建"""
        with app.app_context():
            # 创建仓库
            warehouse = Warehouse(
                warehouse_code="WH001",
                warehouse_name="测试仓库",
                status=1
            )
            database.session.add(warehouse)
            database.session.flush()

            # 创建单位
            unit = Unit.query.filter_by(unit_name="个").first()
            if not unit:
                unit = Unit(unit_name="个", unit_code="PCS")
                database.session.add(unit)
                database.session.flush()

            # 创建产品
            product = Product(
                product_code="ITEM001",
                product_name="测试商品",
                sale_price=50.00,
                unit_id=unit.unit_id,
                status=1
            )
            database.session.add(product)
            database.session.flush()

            # 确保用户存在
            user = User.query.get(1)
            if not user:
                user = User(
                    username="test_user",
                    password="test_pass",
                    email="test@example.com",
                    real_name="测试用户",
                    status=1
                )
                database.session.add(user)
                database.session.flush()

            # 创建库存期初余额
            opening_inventory = OpeningProductStock(
                product_id=product.product_id,
                warehouse_id=warehouse.warehouse_id,
                quantity=100.00,
                cost_price=50.00,
                amount=5000.00,
                created_by=user.user_id
            )
            database.session.add(opening_inventory)
            database.session.commit()

            # 查询库存期初余额
            retrieved_inventory = OpeningProductStock.query.filter_by(product_id=product.product_id, warehouse_id=warehouse.warehouse_id).first()
            assert retrieved_inventory is not None
            assert retrieved_inventory.quantity == 100.00
            assert retrieved_inventory.amount == 5000.00

if __name__ == "__main__":
    pytest.main(["-v", "test_modules.py"])