from app import db
from datetime import datetime
from app.models import Customer, SeedBatch, User


class CustomerComplaint(db.Model):
    __tablename__ = 'customer_complaints'
    complaint_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('seed_batches.batch_id'), nullable=False)
    complaint_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    problem_description = db.Column(db.Text, nullable=False)
    complaint_type = db.Column(db.String(50))
    status = db.Column(db.Integer, nullable=False, default=0)  # 0: 未处理, 1: 已处理, 2: 已关闭
    processed_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    processed_date = db.Column(db.DateTime)
    solution = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationships
    customer = db.relationship('Customer', backref='complaints')
    batch = db.relationship('SeedBatch', backref='complaints')
    processor = db.relationship('User', foreign_keys=[processed_by], backref='processed_complaints')


class ComplaintReply(db.Model):
    __tablename__ = 'complaint_replies'
    reply_id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('customer_complaints.complaint_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    reply_content = db.Column(db.Text, nullable=False)
    reply_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # Relationships
    complaint = db.relationship('CustomerComplaint', backref='replies')
    user = db.relationship('User', backref='complaint_replies')