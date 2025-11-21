from flask import Blueprint

expense = Blueprint('expense', __name__)

from app.expense import routes
from app.expense.models import ExpenseType, ExpenseEntry, SupplierExpense