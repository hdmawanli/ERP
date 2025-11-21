from app import db
from datetime import datetime

class ExpenseType(db.Model):
    __tablename__ = 'expense_types'
    
    expense_type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ExpenseType {self.type_name}>'

class ExpenseEntry(db.Model):
    __tablename__ = 'expense_entries'
    
    expense_entry_id = db.Column(db.Integer, primary_key=True)
    expense_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    expense_type_id = db.Column(db.Integer, db.ForeignKey('expense_types.expense_type_id'), nullable=False)
    amount = db.Column(db.Float(precision=2), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    expense_purpose = db.Column(db.String(100))
    expense_detail = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ExpenseEntry {self.expense_entry_id}>'

class SupplierExpense(db.Model):
    __tablename__ = 'supplier_expenses'
    
    supplier_expense_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    expense_entry_id = db.Column(db.Integer, db.ForeignKey('expense_entries.expense_entry_id'), nullable=False)
    amount = db.Column(db.Float(precision=2), nullable=False)
    note = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SupplierExpense {self.supplier_expense_id}>'